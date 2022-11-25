CREATE TABLE world.city(
    ID INT NOT NULL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL DEFAULT '',
    CountryCode CHAR(3) NOT NULL DEFAULT '',
    District VARCHAR(255) NOT NULL DEFAULT '',
    Info JSON DEFAULT NULL
);

CREATE TABLE world.city2(
    ID INT NOT NULL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL DEFAULT '',
    CountryCode CHAR(3) NOT NULL DEFAULT '',
    District VARCHAR(255) NOT NULL DEFAULT '',
    Info JSON
);

CREATE TABLE world.country(
Code CHAR(3) PRIMARY KEY CHECK (LENGTH(Code) >= 3),
Name VARCHAR(255) NOT NULL DEFAULT '',
Capital INT DEFAULT NULL,
Code2 CHAR(2) NOT NULL UNIQUE DEFAULT '',
FOREIGN KEY (Capital) REFERENCES world.city(ID)
);

CREATE TYPE tf AS ENUM(
'T',
'F'
);

CREATE TABLE world.countrylanguage(
CountryCode CHAR(3) NOT NULL DEFAULT '',
Language CHAR(30) NOT NULL DEFAULT '',
IsOfficial tf NOT NULL DEFAULT 'F',
Percentage DOUBLE PRECISION NOT NULL DEFAULT 0.0,
FOREIGN KEY (CountryCode) REFERENCES world.country(Code),
CONSTRAINT CountryLang PRIMARY KEY (CountryCode, Language)
);

CREATE INDEX idxcountrycode
ON world.countrylanguage (CountryCode);

CREATE SEQUENCE seqid;

CREATE TABLE world.countryinfo(
doc json,
_id varchar(32) NOT NULL PRIMARY KEY DEFAULT nextval('seqid')
);
