CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.genre (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

INSERT INTO content.genre (id, name, description)
VALUES
  (uuid_generate_v4(), 'Action', 'Action movies'),
  (uuid_generate_v4(), 'Drama', 'Drama movies'),
  (uuid_generate_v4(), 'Comedy', 'Comedy movies');
CREATE TABLE IF NOT EXISTS content.person (
    id UUID PRIMARY KEY,
    full_name TEXT NOT NULL
);

INSERT INTO content.person (id, full_name)
VALUES
  (uuid_generate_v4(), 'Quentin Tarantino'),
  (uuid_generate_v4(), 'Christopher Nolan'),
  (uuid_generate_v4(), 'Leonardo DiCaprio');
CREATE TABLE IF NOT EXISTS content.film_work (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    rating FLOAT,
    creation_date DATE
);

INSERT INTO content.film_work (id, title, description, rating, creation_date)
VALUES
  (uuid_generate_v4(), 'Inception', 'Dreams inside dreams', 8.8, '2010-07-16'),
  (uuid_generate_v4(), 'Pulp Fiction', 'Crime stories', 8.9, '1994-10-14'),
  (uuid_generate_v4(), 'Django Unchained', 'Western revenge', 8.4, '2012-12-25');
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id UUID PRIMARY KEY,
    film_work_id UUID NOT NULL,
    genre_id UUID NOT NULL
);
CREATE TABLE IF NOT EXISTS content.person_film_work (
    id UUID PRIMARY KEY,
    film_work_id UUID NOT NULL,
    person_id UUID NOT NULL,
    role TEXT
);
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE SCHEMA IF NOT EXISTS content;
