CREATE TYPE account_status AS ENUM ('banned', 'suspended', 'active', 'inactive')

CREATE TABLE QUESTS(
    q_name text,
    npc_name text,
    lvl int,
    map text,
    exp_reward int,
    PRIMARY KEY (q_name, lvl)
);

CREATE TABLE world(
    id INT PRIMARY KEY,
    name text UNIQUE,
    player_count int
);

CREATE TABLE clan(
    id INT PRIMARY KEY,
    name text UNIQUE,
    world text
);

CREATE TABLE character(
    id INT PRIMARY KEY,
    nick TEXT UNIQUE,
    lvl int,
    player_id int,
    clan_id int,

    CONSTRAINT fk_player
        FOREIGN KEY(player_id)
        REFERENCES clan(id),

    CONSTRAINT fk_clan
        FOREIGN KEY(clan_id)
        REFERENCES clan(id)
);

CREATE TABLE player(
    id INT PRIMARY KEY,
    nick TEXT UNIQUE,
    email TEXT UNIQUE,
    town text,
    street text,
    h_number text,
    zipcode text,
    status account_status
);