use rand::Rng;

#[allow(dead_code)]
fn generate_population(population_size: &u8, genoms_size: &u8) -> Vec<Vec<u8>>{
    let mut rng = rand::thread_rng();
    (0..*population_size).map(|_| (0..*genoms_size).map(|__| rng.gen_range(0..2)).collect()).collect()
}

fn translate(num: &Vec<u8>) -> u8{
    // check if len is correct
    let sign: u8 = num[0];
    sign
}

fn convert_to_vec(num: f32) -> Vec<u8> {
    let bits: Vec<u8> = num.to_le_bytes().to_vec();
    println!("{:?}", bits);
    bits
}

fn main() {
    let num = vec![1,0,0,0,1,1,0];
    let test = translate(&num);
    let translated = convert_to_vec(-3.44232f32);


    println!("{:?}", translated)
}
