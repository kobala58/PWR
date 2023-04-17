extern crate rplex;
use rplex::*;
use rand::distributions::{Distribution, Uniform};

fn main() {
    // create a CPLEX environment
    let env = Env::new().unwrap();
    // populate it with a problem
    let mut prob = Problem::new(&env, "lpex1").unwrap();
    // maximize the objective
    prob.set_objective_type(ObjectiveType::Maximize).unwrap();
    // create our variables
    let x1 = prob.add_variable(var!(0.0 <= "x1" <= 40.0 -> 1.0)).unwrap();
    let x2 = prob.add_variable(var!("x2" -> 2.0)).unwrap();
    let x3 = prob.add_variable(var!("x3" -> 3.0)).unwrap();
    println!("{} {} {}", x1, x2, x3);

    // add our constraints
    prob.add_constraint(con!("c1": 20.0 >= (-1.0) x1 + 1.0 x2 + 1.0 x3)).unwrap();
    prob.add_constraint(con!("c2": 30.0 >= 1.0 x1 + (-3.0) x2 + 1.0 x3)).unwrap();

    // solve the problem
    let sol = prob.solve().unwrap();
    println!("{:?}", sol);
    // values taken from the output of `lpex1.c`
    assert!(sol.objective == 202.5);
    assert!(sol.variables == vec![VariableValue::Continuous(40.0),
                                    VariableValue::Continuous(17.5),
                                    VariableValue::Continuous(42.5)]);

    // ex1();
}


// fn generate_data_vec(size: usize) -> Vec<u8>{
//     let range = Uniform::new(0,50);
//     let mut rng = rand::thread_rng(); 
//     let vals: Vec<u8> = range.sample_iter(&mut rng).take(size).map(|x| x as u8).collect();
//     vals
// }

// fn ex1() {
//     let env = Env::new().unwrap();
//     let mut prob = Problem::new(&env, "Problem trojpodzialu").unwrap();
//     prob.set_objective_type(ObjectiveType::Maximize).unwrap();
//     let numbers: Vec<u8>=  generate_data_vec(10*3);

// }
