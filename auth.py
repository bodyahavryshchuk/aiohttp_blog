import sqlalchemy as sa

from aiohttp_security.abc import AbstractAuthorizationPolicy
from passlib.hash import sha256_crypt

import models


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, dbengine):
        self.dbengine = dbengine

    async def authorized_userid(self, identity):
        async with self.dbengine.acquire() as conn:
            where = sa.and_(models.Users.c.login == identity,
                            sa.not_(models.Users.c.disabled))
            query = models.Users.select().where(where)
            ret = await conn.fetch(query)
            if ret:
                return identity
            else:
                return None

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False

        async with self.dbengine.acquire() as conn:
            where = sa.and_(models.Users.c.login == identity,
                            sa.not_(models.Users.c.disabled))
            query = models.Users.select().where(where)
            ret = await conn.execute(query)
            user = await ret.fetchone()
            if user is not None:
                user_id = user['id']
                is_superuser = user['is_superuser']
                if is_superuser:
                    return True

                where = models.Permissions.c.user_id == user_id
                query = models.Permissions.select().where(where)
                ret = await conn.execute(query)
                result = await ret.fetchall()
                if ret is not None:
                    for record in result:
                        if record.perm_name == permission:
                            return True

            return False


async def check_credentials(db_engine, username, password):
    async with db_engine.acquire() as conn:
        where = sa.and_(models.Users.c.login == username,
                        sa.not_(models.Users.c.disabled))
        query = models.Users.select().where(where)
        user = await conn.fetchrow(query)
        # ret = await conn.execute(query)
        # user = await ret.fetchone()
        if user is not None:
            hashed = user['passwd']
            return sha256_crypt.verify(password, hashed)
    return False
