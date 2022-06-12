create table if not exists files
(
    id       serial
        constraint files_pk
            primary key,
    filename varchar(100),
    mimetype varchar(120) default 'unknown'::character varying
);

create unique index if not exists files_id_uindex
    on files (id);
