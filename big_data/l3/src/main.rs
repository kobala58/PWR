use rand::distributions::{Distribution, Uniform};
pub mod plots;

fn generate_time_series_data(size: usize) -> Vec<u8>{
    let range = Uniform::new(0,50);
    let mut rng = rand::thread_rng(); 
    let vals: Vec<u8> = range.sample_iter(&mut rng).take(size).map(|x| x as u8).collect();
    vals
}

fn normalize_vec(data: &Vec<u8>) -> Vec<f32>{ //min-max normalization 
    let min: f32 = f32::from(*data.iter().min().unwrap()); // find min 
    let max: f32 = f32::from(*data.iter().max().unwrap()); // find max
    let norm = data.iter()
        .map(|x|{
            (f32::from(*x)-min)/(max+min) // y = (x-min)/max-min
        }).collect::<Vec<f32>>();
    norm
}

fn standard_vec(data: &Vec<u8>) -> Vec<f32> {
    let vec_len: i32 = data.len() as i32;
    let summary: f32 = data.iter().fold(0f32, |sum, i| sum + (*i as f32));
    let mean: f32 = summary / vec_len as f32 ;
    let sum: Vec<f32> = data.iter().map(
        |x| {
            f32::from(*x as f32-mean).powi(2)
        }
    ).collect::<Vec<f32>>();
    let std_var: f32 = f32::sqrt(sum.iter().sum::<f32>() / vec_len as f32); // std_var = sqrt(sum(x-mean)/len)
    let std_var_vec: Vec<f32> = data.iter().map(  // (x-mean)/std_var
        |x| {
            (*x as f32 - mean)/std_var
        }
    ).collect::<Vec<f32>>();
    std_var_vec
}

fn rescale_to_range(data: &Vec<u8>, down: u8, up: u8) -> Vec<f32>{
    let min: f32 = f32::from(*data.iter().min().unwrap()); // find min 
    let max: f32 = f32::from(*data.iter().max().unwrap()); // find max
    let rescaled = data.iter().map(|x|{
        down as f32 + (((*x as f32 - min)*(up-down) as f32)/(max - min)) // y = down + (x-min)(up-down)/(max-min)
    }).collect::<Vec<f32>>();
    rescaled
}

fn main() {
    const SAMPLE_SIZE: usize = 250; 
    println!("Hello, world!");
    let data = generate_time_series_data(SAMPLE_SIZE);
    let data_norm: Vec<f32> = normalize_vec(&data);
    let data_std: Vec<f32> = standard_vec(&data);
    let data_scaled: Vec<f32> = rescale_to_range(&data, 1, 3);
    println!("Generated:\n{:?}", data);
    println!("Normalized:\n{:?}", data_norm);
    println!("Standarised:\n{:?}", data_std);
    println!("Rescaled:\n{:?}", data_scaled);
    println!("\n\n\n");
    let dataf32 = data.iter().map(|x| *x as f32).collect::<Vec<f32>>(); 
    let arr: [Vec<f32>; 4] = [dataf32, data_norm, data_std, data_scaled];  
    plots::test_draw().unwrap();
    plots::draw_plots(&arr, SAMPLE_SIZE as f32).unwrap();
}
