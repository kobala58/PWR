use std::{thread, time, time::Duration};


fn eq(prev: f32, is_on: bool) -> f32{
    let temp_delta: f32 = 0.1;
    if is_on {
        // temp goes up!
        let val = prev + prev * temp_delta; 
        return val;
    }
    else{
        let val = prev + prev * (0.1);
        return val;
    }

}

fn simulation() -> i8 {
    let eq = 2;
    eq
}

fn main() {
    let start = 23.0;
    let outside = 0; // temperatura na zewnatrz
    let current: f32; // temperatura pokoju
    let mut index = 0;
    let mut val: f32;
    val = eq(start, true);
    while index < 10{
        val = eq(val, true);
        println!("Iter: {index}, val: {}", val);
        index += 1;
        thread::sleep(Duration::from_secs(5))
    }

    let sample = eq(1000.0, true);
    println!("Temp: {}", sample);
    simulation();
}
