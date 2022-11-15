SET search_path TO world;
-- EX1
SELECT country.name
    ,city.name
    ,CAST(doc->>'GNP' AS float) as gnp

FROM world.country JOIN world.city ON country.capital=city.id
JOIN world.countryinfo ON world.country.code=world.countryinfo.doc->>'_id'
ORDER BY gnp DESC LIMIT 1;

-- EX2

SELECT
    doc->'geography'->>'Continent' AS Continent
    ,MIN(CAST(doc->>'GNP' AS float)) as minimum
    ,MAX(CAST(doc->>'GNP' AS float)) as maximum
    ,ROUND(AVG(CAST(doc->>'GNP' AS float))::numeric, 4) as avg

FROM world.countryinfo
GROUP BY Continent;

-- EX3

SELECT name
    FROM world.city JOIN world.countryinfo ON world.city.countrycode=world.countryinfo.doc->>'_id'
    WHERE doc->'geography'->>'Continent'='North America';

-- EX4

SELECT doc->>'Name' AS Name
    FROM world.countryinfo
    WHERE doc->'government'->>'HeadOfState' LIKE '%Elisabeth%';

-- EX5

SELECT
    doc->'geography'->>'Continent' AS Continent
    ,COUNT(doc->>'Name')

    FROM world.countryinfo
    GROUP BY doc->'geography'->>'Continent';
--     LAST
    (SELECT
        doc->>'Name' AS Country
        ,ROUND(CAST(doc->'demographics'->>'LifeExpectancy' AS float)::numeric, 2) AS LE
    FROM world.countryinfo
    ORDER BY LE
    LIMIT 10)
UNION
    (SELECT
        doc->>'Name' AS Country
        ,ROUND(CAST(doc->'demographics'->>'LifeExpectancy' AS float)::numeric, 3) AS LE
    FROM world.countryinfo
    ORDER BY LE desc NULLS LAST
    LIMIT 10)
    ORDER BY LE;
