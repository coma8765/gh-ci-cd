create table if not exists users
(
    id              serial
        constraint users_pk
            primary key,
    email           varchar(100)            not null,
    hashed_password varchar(60)             not null,
    email_confirm bool default False        not null,
    create_date     timestamp default now() not null
);

create unique index if not exists users_email_uindex
    on users (email);

create unique index if not exists users_id_uindex
    on users (id);

