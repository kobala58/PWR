#![allow(dead_code, unused)]
use std::fmt;

#[derive(Debug, Clone)]
pub struct ParseError;

pub impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result{
    write!(f, "cannot parse this shit")
} 
}

