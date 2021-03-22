CREATE TABLE IF NOT EXISTS users
(
  id serial NOT NULL,
  login character varying(256) NOT NULL,
  passwd character varying(256) NOT NULL,
  is_superuser boolean NOT NULL DEFAULT false,
  disabled boolean NOT NULL DEFAULT false,
  CONSTRAINT user_pkey PRIMARY KEY (id),
  CONSTRAINT user_login_key UNIQUE (login)
);

CREATE TABLE permissions
(
  id serial NOT NULL,
  user_id integer NOT NULL,
  perm_name character varying(64) NOT NULL,
  CONSTRAINT permission_pkey PRIMARY KEY (id),
  CONSTRAINT user_permission_fkey FOREIGN KEY (user_id)
      REFERENCES users (id)
);

CREATE TABLE category (
    id serial primary key,
    name varchar(50) not null
);

CREATE TABLE post (
    id serial primary key,
    author int,
    category int,
    name varchar(50) not null,
    description varchar(500) not null,
    price int not null,
    available bool not null,
    created date,
    FOREIGN KEY (category)  REFERENCES category (id) ON DELETE CASCADE,
    FOREIGN KEY (author)  REFERENCES users (id) ON DELETE CASCADE
);

insert into category (name) values ('category2');
insert into category (name) values ('category1');
insert into post (category, name, description, price, available) values (1, 'post1', 'descr', 124, True)
insert into post (author, category, name, description, price, available) values (1, 1, 'post2', 'descr', 122, True)


INSERT INTO users(login, passwd, is_superuser, disabled)
VALUES ('user', 'c1594d99d2873c2df4bdab116bb21d55f026078c0f4397469559daf8af6fdca2', false, false);
INSERT INTO users(login, passwd, is_superuser, disabled)
VALUES ('admin', '$5$rounds=535000$9b6.nBT6OFc5fra6$Xg.qCp3M1bhER071Y21lQ/7/gNrBjfGiSTu9XdQaBvD', true, false);

INSERT INTO permissions(id, user_id, perm_name)
VALUES (2, 2, 'protected');
INSERT INTO permissions(id, user_id, perm_name)
VALUES (1, 2, 'public');
