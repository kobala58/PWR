use std::collections::HashMap;

use rand::distributions::{Distribution, Uniform};
struct StatisticalFeatures{
    avg: f32,
    std_dvr: f32, 
    max_val: f32, 
    min_val: f32, 
    median: f32,
    kurt: f32, 
}
struct Ex2Parameters{
    fractal_dim: f64,
    hurst_exp: f32,
    entrophy: f32,
}

struct WholeStatics {
    e1: StatisticalFeatures,
    e2: Ex2Parameters,
}

impl WholeStatics {
    fn print_info(&self) {
        println!("E1:");
        println!(" - avg: {}", self.e1.avg);
        println!(" - std_dvr: {}", self.e1.std_dvr);
        println!(" - max_val: {}", self.e1.max_val);
        println!(" - min_val: {}", self.e1.min_val);
        println!(" - median: {}", self.e1.median);
        println!(" - kurt: {}", self.e1.kurt);
        println!("E2:");
        println!(" - fractal_dim: {}", self.e2.fractal_dim);
        println!(" - hurst_exp: {}", self.e2.hurst_exp);
        println!(" - entrophy: {}", self.e2.entrophy);
    }
}


fn generate_time_series_data(size: usize) -> Vec<u8>{
    let range = Uniform::new(0,50);
    let mut rng = rand::thread_rng(); 
    let vals: Vec<u8> = range.sample_iter(&mut rng).take(size).map(|x| x as u8).collect();
    vals
}



fn ex1(time_series: &Vec<u8>) -> StatisticalFeatures{
    println!("Grabbed_data: \n{:?}", time_series);
    let min: f32 = f32::from(*time_series.iter().min().unwrap()); // find min 
    let max: f32 = f32::from(*time_series.iter().max().unwrap()); // find max
    let median: f32 = match time_series.len()%2 {
        0 => {
            let idx = time_series.len()/2;
            f32::from(time_series[idx] + time_series[idx+1])/2f32
        },
        1 => {
            f32::from(time_series[time_series.len()/2])
        },
        _ => unreachable!(),
    };

    let summary: f32 = time_series.iter().fold(0f32, |sum, i| sum + (*i as f32));
    let mean: f32 = summary / time_series.len() as f32;
    let sum: Vec<f32> = time_series.iter().map(
        |x| {
            f32::from(*x as f32-mean).powi(2)
        }
    ).collect::<Vec<f32>>();
    let std_var: f32 = f32::sqrt(sum.iter().sum::<f32>() / time_series.len() as f32); // std_var = sqrt(sum(x-mean)/len)
    let kurt = sum.iter().map(|x| x.powi(2)).fold(0f32, |sum, i| sum + i) / (time_series.len() as f32 * std_var.powi(4));

    StatisticalFeatures {avg: mean, std_dvr: std_var, max_val: max, min_val: min, median: median, kurt: kurt}
}

fn entrophy(time_series: &Vec<u8>) -> f32{
    let vec_len = time_series.len();
    let mut counts = HashMap::new(); // create hashmap to store val and its count
    for idx in 0..vec_len{
        *counts.entry(time_series[idx]).or_insert(0) += 1;
    }

    let mut entrophy = 0f32;
    for &count in counts.values(){
        let p = count as f32 / vec_len as f32;
        entrophy -= p * p.log2();
    }
    entrophy
}
/**
Najpierw musimy zdefiniować, jakie szeregi czasowe będą używane do obliczania wymiaru fraktalnego. 
Jedną z popularnych metod jest tzw. metoda skali i kroju, która polega na zmniejszaniu skali i obliczaniu liczby pudełek wymaganych do pokrycia fraktala przy każdej skali.

* */

fn fractal_dim(time_series: &Vec<u8>) -> f64 {
    let min_scale = 10; // minimalna skala
    let max_scale = time_series.len() / 5; // maksymalna skala, powinna być mniejsza niż połowa długości szeregu czasowego
    let scales = (min_scale..=max_scale).map(|s| s as f64).collect::<Vec<_>>();
    println!("{:?}", scales);
    let mut box_counts = vec![0.0; scales.len()];

    // dla każdej skali, obliczamy liczbę pudełek wymaganych do pokrycia fraktala
    for (i, &scale) in scales.iter().enumerate() {
        // let box_size = 1.0 / scale;
        let mut count = 0;

        // podział wektora na pudełka o rozmiarze box_size i zliczanie niepustych pudełek
        for j in 0..(time_series.len() - 1) {
            let box_index = (time_series[j] as f64 * scale) as usize;
            if box_index > count {
                count += 1;
            }
        }

        box_counts[i] = count as f64;
    }

    let log_scales = scales.iter().map(|&s| s.ln()).collect::<Vec<_>>();
    let log_counts = box_counts.iter().map(|&c| c.ln()).collect::<Vec<_>>();

    let slope = (log_counts.last().unwrap() - log_counts.first().unwrap())
        / (log_scales.last().unwrap() - log_scales.first().unwrap()) as f64;

    slope as f64
}

/**
Jedną z popularnych metod obliczania wykładnika Hursta jest tzw. metoda przesuwającego się okna, 
która polega na dzieleniu szeregu czasowego na mniejsze podzbiory o równej długości i obliczaniu średniego odchylenia standardowego dla każdego z tych podzbiorów. 
Wykładnik Hursta jest następnie obliczany jako logarytm naturalny średniego odchylenia standardowego podzielonego przez logarytm długości podzbioru.
**/

fn hurst_exponent(time_series: &Vec<u8>) -> f32 {
    let min_window = 10; // minimalna długość okna
    let max_window = time_series.len() / 2; // maksymalna długość okna, powinna być mniejsza niż połowa długości szeregu czasowego
    let windows = (min_window..=max_window).collect::<Vec<_>>();

    let mut log_stddevs = vec![0.0; windows.len()];

    // dla każdej długości okna, obliczamy średnie odchylenie standardowe dla każdego podzbioru
    for (i, &window_size) in windows.iter().enumerate() {
        let mut std_devs = Vec::new();

        for chunk in time_series.chunks(window_size) {
            // let mean = chunk.iter().sum::<u8>() as f64 / chunk.len() as f64;
            let mean = chunk.iter().map(|&x| x as f64).sum::<f64>() / chunk.len() as f64;
            let std_dev = (chunk.iter().map(|&x| (x as f64 - mean).powi(2)).sum::<f64>() / chunk.len() as f64).sqrt();
            std_devs.push(std_dev);
        }

        // obliczamy średnie odchylenie standardowe dla podzbiorów
        let avg_stddev = std_devs.iter().sum::<f64>() / std_devs.len() as f64;

        log_stddevs[i] = avg_stddev.ln();
    }

    // obliczamy współczynnik kierunkowy regresji liniowej w skali-logarytmicznej
    let log_windows = windows.iter().map(|&w| w as f64).collect::<Vec<_>>();

    let slope = (log_stddevs.last().unwrap() - log_stddevs.first().unwrap())
        / (log_windows.last().unwrap() - log_windows.first().unwrap());

    slope as f32 / 2.0 // wykładnik Hursta jest połową współczynnika kierunkowego
}

fn ex2(time_series: &Vec<u8>) -> Ex2Parameters{
    Ex2Parameters{
        fractal_dim: fractal_dim(time_series),
        hurst_exp: hurst_exponent(time_series),
        entrophy: entrophy(&time_series),
    } 
} 

fn moving_window(time_series: &Vec<u8>, windows_size: usize) -> Vec<WholeStatics>{
    let vec_len = time_series.len();
    let mut results: Vec<WholeStatics> = Vec::new();
    let mut mark:usize = 0;
    while mark+windows_size <= vec_len{
        let s_ex1 = ex1(&time_series[mark..mark+windows_size].to_vec()); // split to size and then run ex1 on this
        let s_ex2 = ex2(&time_series[mark..mark+windows_size].to_vec()); // split to size and then run ex1 on this
        results.push(WholeStatics{e1: s_ex1, e2: s_ex2});
        mark = mark + windows_size;
    };
    if mark < vec_len{
        
        let s_ex1 = ex1(&time_series[mark..vec_len].to_vec()); // split to size and then run ex1 on this
        let s_ex2 = ex2(&time_series[mark..vec_len].to_vec()); // split to size and then run ex1 on this
        results.push(WholeStatics{e1: s_ex1, e2: s_ex2});
    }
    results
}

fn main() {
    const SAMPLE_SIZE: usize = 1500;
    let sample_data = generate_time_series_data(SAMPLE_SIZE);
    println!("{:?}", sample_data);
    let wind = moving_window(&sample_data, 100);
    for x in wind{
        x.print_info();
    }
}
