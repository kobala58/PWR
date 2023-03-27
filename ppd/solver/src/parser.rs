#![allow(dead_code, unused)]

use std::collections::HashMap;

pub fn extract_coefficients(equation: &str, variables: &Vec<&str>) -> HashMap<&str, i32> {
    let mut coefficients: HashMap<&str, i32> = HashMap::new();
    
    for variable in variables {
        let term = format!("{}*", variable);
        let start_index = equation.find(&term).unwrap();
        let end_index = if let Some(i) = equation[start_index + term.len()..].find(|c: char| !c.is_digit(10)) {
            start_index + term.len() + i
        } else {
            equation.len()
        };
        let coefficient = equation[start_index + term.len()..end_index].parse::<i32>().unwrap_or(1);
        coefficients.insert(variable, coefficient);
    }
    
    coefficients
}
