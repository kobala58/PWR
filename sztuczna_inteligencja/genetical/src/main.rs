use rand::Rng;

fn generate_population(population_size: &u8, genoms_size: &u8) -> Vec<Vec<>>{
    let mut rng = rand::thread_rng();
    (0..population_size).map(|_| (0..genoms_size).map(|__| rng.gen_range(0..2)).collect()).collect()
}
fn main() {
    println!("Hello, world!");
}
