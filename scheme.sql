create table "category" (
    id serial primary key,
    category text not null
);

create table "user" (
    tg_user_id integer primary key,
    nickname text not null,
    username text,
    category_ids integer[]
);

create table "news" (
    id serial primary key,
    title text not null,
    description text,
    date
)