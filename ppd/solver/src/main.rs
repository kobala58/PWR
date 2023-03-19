use serde::Deserialize;
use toml::value::Array;
use std::collections::HashMap;
use std::fs;
use std::process::exit;
use toml;

#[derive(Deserialize)]
struct Config {
    dvars: Dvars,
    target: Target, 
    subject: Subject,
}

#[derive(Deserialize)]
struct Dvars{
    var: Array,
    dvar_type: String,
}

#[derive(Deserialize)]
struct Target{
    opt_type: String,
    eq: String,
}

#[derive(Deserialize)]
struct Subject{
    data: Array,
}

fn main() {
    let path = std::path::Path::new("./data.toml");
    let content = match fs::read_to_string(path) {
        Ok(f) => f,
        Err(e) => panic!("{}", e),
    };


    let config: Config = match toml::from_str(&content){
        Ok(d) => d,
        Err(_) => {
            eprintln!("Chuj wi: {}", content);
            exit(1);
        }
    };

    println!("{}", config.dvars.var[1]);
    println!("{}", config.target.opt_type);
    println!("{}", config.subject.data[0]);
}
