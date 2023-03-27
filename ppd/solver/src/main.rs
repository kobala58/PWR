#![allow(dead_code, unused)]

use std::fs;
use std::process::exit;
use toml;
extern crate meval; 
pub mod models;
pub mod parser;

fn main() {
    let path = std::path::Path::new("./data.toml");
    let content = match fs::read_to_string(path) {
        Ok(f) => f,
        Err(e) => panic!("{}", e),
    };


    let config: models::Config = match toml::from_str(&content){
        Ok(d) => d,
        Err(_) => {
            eprintln!("Chuj wi: {}", content);
            exit(1);
        }
    };
    
    println!("{:?}", config.dvars.var);
    println!("{}", config.target.opt_type);
    println!("{}", config.subject.data[0]);
    let coef: Vec<&str> = config.dvars.var.to_vec();
    let data = parser::extract_coefficients(config.target.eq.as_str(), &coef);

    println!("{:?}", data);
    // println!("{}", config.target.opt_type);
    // println!("{}", config.subject.data[0]);
    // bind variables to  
}
