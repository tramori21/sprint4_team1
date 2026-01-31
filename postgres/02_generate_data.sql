-- 100 жанров
INSERT INTO content.genre (id, name, description)
SELECT
    uuid_generate_v4(),
    'Genre ' || g,
    'Description ' || g
FROM generate_series(1, 100) g
ON CONFLICT DO NOTHING;

-- 10 000 персон
INSERT INTO content.person (id, full_name)
SELECT
    uuid_generate_v4(),
    'Person ' || p
FROM generate_series(1, 10000) p
ON CONFLICT DO NOTHING;

-- 200 000 фильмов
INSERT INTO content.film_work (id, title, description, rating, creation_date)
SELECT
    uuid_generate_v4(),
    'Movie ' || f,
    'Description ' || f,
    (random() * 10)::numeric(3,1),
    NOW()::date
FROM generate_series(1, 200000) f
ON CONFLICT DO NOTHING;

-- связи фильм-жанр
INSERT INTO content.genre_film_work (id, film_work_id, genre_id)
SELECT
    uuid_generate_v4(),
    fw.id,
    g.id
FROM content.film_work fw
JOIN LATERAL (
    SELECT id FROM content.genre ORDER BY random() LIMIT 2
) g ON true
ON CONFLICT DO NOTHING;

-- связи фильм-персона
INSERT INTO content.person_film_work (id, film_work_id, person_id, role)
SELECT
    uuid_generate_v4(),
    fw.id,
    p.id,
    'actor'
FROM content.film_work fw
JOIN LATERAL (
    SELECT id FROM content.person ORDER BY random() LIMIT 3
) p ON true
ON CONFLICT DO NOTHING;
