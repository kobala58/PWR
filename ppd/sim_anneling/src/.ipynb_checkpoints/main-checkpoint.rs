


fn generate_dvars_vec(n: u32, p: u32) -> Vec<Vec<u32>>{
    // generate Vector of vectors with contains all combination of
    // possible shop placements
    // Params:
    //      n: number of all possible places to choose from
    //      p: number of shops that needs to be assigned
    //
    // in fact we only need to iterate from 2^p - 1 to (2^n - 2^(n-p))
    let low_bound: i32 = 2i32.pow(p)-1i32;
    println!("LB: {}", low_bound);
    let high_bound: i32 = 2i32.pow(n) - 2i32.pow(n-p);
    println!("UB: {}", high_bound);
    // rust format! macro cant take variable as a size: format("{:0VARb}",x , VAR=10) is not a
    // valid rust code, so i set it to CONST in code and not bother about it till future
    let data = (low_bound..=high_bound).filter(|x| x.count_ones() == p).map(|x| format!("{:015b}", x).chars().map(|y| y.to_digit(10).unwrap()).collect()).collect();
    data
}

fn eval_set(setup: Vec<char>, points: Vec) -> f32{

 42f32
}

fn main() {
    // let data = generate_points!(7, )
    const PLACES: u32 = 15; // Remebrer about size in generate_dvars_vec in format! macro
    const SHOPS: u32 = 8;
    let dvars = generate_dvars_vec(PLACES, SHOPS);
    let points = generate_points!(1, 100, )
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
