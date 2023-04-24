use std::fmt::format;


fn generate_dvars_vec(n: u32, p: u32) -> Vec<Vec<char>>{
    // generate Vector of vectors with contains all combination of
    // possible shop placements
    // Params:
    //      n: number of all possible places to choose from
    //      p: number of shops that needs to be assigned
    //
    // in fact we only need to iterate from 2^p - 1 to (2^n - 2^(n-p))
    let low_bound: i32 = 2i32.pow(p)-1i32;
    let high_bound: i32 = 2i32.pow(n) - 2i32.pow(n-p);
    
    let data = (low_bound..high_bound).filter(|x| x.count_ones() == 3).map(|x| format!("{:b}", x).chars().collect()).collect();

    data
}

fn eval_set() -> f32{

    42f32
}

fn main() {
    // let data = generate_points!(7, )
    const PLACES: u32 = 15;
    const SHOPS: u32 = 8;
    


    println!("Hello, world!");
}


#[macro_export]
// maco for generaitng points 
macro_rules! generate_points {
    ($low:expr, $high:expr, $typ:ty, $cnt:expr) => {
    let range = Uniform::new($low,$high);
    let mut rng = rand::thread_rng(); 
    let vals: Vec<u8> = range.sample_iter(&mut rng).take($cnt).map(|x| x as $typ).collect();
    vals
    }
}
