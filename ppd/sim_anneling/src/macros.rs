#![macro_use]

use rand::distributions::{Distribution, Uniform};


#[macro_export]
macro_rules! generate_points {
    ($low:expr, $high:expr, $typ:ty, $cnt:expr) => {
    let range = Uniform::new($low,$high);
    let mut rng = rand::thread_rng(); 
    let vals: Vec<u8> = range.sample_iter(&mut rng).take($cnt).map(|x| x as $typ).collect();
    vals
    }
}
