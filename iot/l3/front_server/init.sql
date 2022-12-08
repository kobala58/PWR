CREATE TYPE method AS ENUM ('REST', "MQTT");

Create Table send_configs(
  id uuid,
  name char(30) NOT NULL UNIQUE,
  method method,
  PORT int,
  channel char(30),
  server char(30)
);

CREATE TABLE presets (
  name char(32),
  interval int,
  method method,
  valor char(32),
);

CREATE TABLE data(
  id uuid,
  valor char(30),
  date_start date,
  interval int,
  open float8,
  high float8,
  low float8,
  close float8,
  average float8
);

CREATE TABLE configs(
  id char(30),
  name char(30),
  ip_port int,
  config 
)
