use serde::Deserialize;
use toml::value::Array;

#[derive(Deserialize)]
pub struct Config {
    pub dvars: Dvars,
    pub target: Target, 
    pub subject: Subject,
}

#[derive(Deserialize)]
pub struct Dvars{
    pub var: Array,
    pub dvar_type: String,
}

#[derive(Deserialize)]
pub struct Target{
    pub opt_type: String,
    pub eq: String,
}

#[derive(Deserialize)]
pub struct Subject{
    pub data: Array,
    pub sign: Array,
    pub vals: Array,
}

