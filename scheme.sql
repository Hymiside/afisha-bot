CREATE TABLE public.users (
    tg_user_id integer primary key,
    nickname character varying,
    username character varying,
    category_ids integer[],
    created_at date default now()
);

CREATE TABLE public.mailings (
    id integer NOT NULL,
    title character varying,
    description character varying,
    date timestamp without time zone,
    categories integer[],
    price integer,
    attachments character varying[],
    link character varying
);

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying
);

CREATE TABLE public.admins (
    id integer NOT NULL,
    login character varying NOT NULL,
    hashed_password character varying NOT NULL,
    name character varying NOT NULL
);
