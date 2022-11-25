set search_path to world;

SELECT distinct doc->'government'->>'GovernmentForm' AS Forma
    FROM countryinfo;
    
SELECT doc->'geography'->>'Continent' AS Kontynent
    FROM countryinfo
    GROUP BY Kontynent
    ORDER BY count(doc->'geography'->>'Continent') DESC
    limit 1; 
    
SELECT doc->>'Name' AS Nazwa, doc->>'IndepYear' AS IndepYear
    FROM countryinfo
    WHERE (doc->>'IndepYear' IS NOT NULL)
    ORDER BY cast(doc->>'IndepYear' AS int) DESC;
   
SELECT Language, count(isofficial)
    FROM world.countrylanguage
    WHERE isofficial='T'
    group by Language
    ORDER BY count(isofficial) DESC;
    
SELECT Language, sum(countrylanguage.percentage*0.01*cast(doc->'demographics'->>'Population' AS int)) AS count_people
    FROM countrylanguage JOIN countryinfo on countrylanguage.countrycode=countryinfo.doc->>'_id'
    group by Language
    ORDER BY count_people DESC;

    
SELECT Nazwa
    FROM
    (SELECT doc->>'Name' AS Nazwa, cast(doc->'demographics'->>'LifeExpectancy' AS float) AS dlugosc_zycia
    FROM countryinfo ORDER BY dlugosc_zycia DESC nulls last limit 20) AS life
    JOIN
    (SELECT doc->>'Name' AS Nazwa_gnp, cast(doc->>'GNP' AS float) AS GNP
    FROM countryinfo ORDER BY GNP DESC nulls last limit 20) AS gnp
    on life.Nazwa=gnp.Nazwa_gnp;
    
-- 17l populacja, % ludzi, nazwa kraju, liczba ludzi posługująca się tym językiem

SELECT Language, count(isofficial)
    FROM world.countrylanguage
    WHERE isofficial='T'
    group by Language
    ORDER BY count(isofficial) DESC;

SELECT
    name,
    countrylanguage.language,
    countrylanguage.percentage,
    cast(countrylanguage.percentage*0.01*cast(doc->'demographics'->>'Population' AS int) as int) as sperakers,
    cast(doc->'demographics'->>'Population' AS int) as whole_population

from country
    join countrylanguage on country.code = countrylanguage.countrycode
    join countryinfo on countrylanguage.countrycode=countryinfo.doc->>'_id'

where
    (countrylanguage.language = (SELECT Language
                                FROM world.countrylanguage
                                WHERE isofficial='T'
                                group by Language ORDER BY count(isofficial) DESC LIMIT 1))

AND (percentage != 0) ORDER BY sperakers DESC

