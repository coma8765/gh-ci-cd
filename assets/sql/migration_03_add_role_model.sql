CREATE TYPE user_role AS ENUM ('meta-admin', 'admin', 'teacher', 'methodist', 'student');

create table if not exists roles
(
    id      serial
        constraint roles_pk
            primary key,
    user_id integer                 not null
        constraint roles_users_id_fk
            references users
            on delete cascade,
    role    user_role               not null,
    date    timestamp default now() not null
);

create unique index if not exists roles_id_uindex
    on roles (id);

create index if not exists roles_user_id_role_index
    on roles (user_id, role);
