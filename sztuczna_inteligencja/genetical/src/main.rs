use core::panic;
use std::usize;
use meval::{self};
use rand::Rng;
use plotters::prelude::*;
use dialog::DialogBox;

#[allow(dead_code)]
fn generate_population(population_size: i32, genoms_size: i32) -> Vec<Vec<bool>>{
    let mut rng = rand::thread_rng();
    (0..population_size).map(|_| (0..genoms_size).map(|__| rng.gen_range(0..2) == 1).collect()).collect()
}

//
// [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
// one sign bit, three bits to code int part and rest to code decimal part
//

fn read_value(code: &Vec<bool>) -> f64{
    let sign = match code[0] as u8 {
        0 => 1f64,
        1 => -1f64,
        _ => panic!("IDK"),
    };
    
    let int_part:f64 = (0..3).map(|idx| (2u8.pow(idx)*code[idx as usize + 1] as u8) as f64).sum();
    let dec_part:f64 = (0..code.len()-4).map(|idx| 2f64.powi(-(idx as i32 + 1))*code[idx+4] as i32 as f64).sum();
    (int_part+dec_part)*sign
}

fn grab_funtion_from_user(usr_str: &str) -> impl Fn(f64) -> f64{
    let expr: meval::Expr = usr_str.parse().unwrap();
    let func = expr.bind("x").unwrap();
    func
}

fn eval_population(func: impl Fn(f64) -> f64, population: &Vec<Vec<bool>>) -> Vec<f64> {
    population.iter().map(|single| func(read_value(&single))).collect()
}

fn segment_gen(val_vec: Vec<f64>) -> Vec<f64>{
     val_vec.iter().scan(0f64, |acc, &x|{
        *acc = *acc + x;
        Some(*acc)
    }).collect()
}


#[allow(unused_variables)]
fn main() -> Result<(), Box<dyn std::error::Error>> {
    
    // CONSTS
    const EPOCHS: i32 = 40;
    const POPULATION_SIZE: i32 = 80;
    const GENOMS_SIZE: i32 = 12;
    const PC: f32 = 0.5;
    const PM: f32 = 0.005;
    const DRAW_GIF: bool = true;

    let input = dialog::Input::new("Please enter your function")
    .title("Funkcja")
    .show()
    .expect("Could not display dialog box").unwrap();

    let function = grab_funtion_from_user(input.trim());
    let mut population = generate_population(POPULATION_SIZE, GENOMS_SIZE);
    let mut eval_pop = eval_population(&function, &population);
    
    // STATS GATHER 
    let mut fit_history: Vec<f64> = Vec::new();
    let mut best_history: Vec<f64> = Vec::new();
    let root = BitMapBackend::gif("out.gif", (800, 600), EPOCHS as u32)?.into_drawing_area();
 
    // println!("{:?}", eval_pop);
    for idx in 0..EPOCHS{
        let abs_max = eval_pop.iter().fold(f64::NAN, |a, &b| (a.abs()).max(b.abs()));
        let eval_f: Vec<f64> = eval_pop.iter().map(|val| abs_max-val).collect();
        let eval_sum: f64 = eval_f.iter().sum();
        fit_history.push(eval_sum.clone());
        let best_fit = eval_f.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        best_history.push(best_fit);
        let eval_f_norm: Vec<f64> = eval_f.iter().map(|val| val/eval_sum).collect();
        let ranges = segment_gen(eval_f_norm);
        let mut chosen: Vec<Vec<bool>> = Vec::new(); 
        // Roulette 
        for _ in 0..POPULATION_SIZE{
            let mut rng = rand::thread_rng();
            let d = rng.gen_range(0.0..1.0);
            if 0f64 <= d && d < ranges[0]{
                chosen.push(population[0].clone())

            }
            for x in 0..(POPULATION_SIZE-1) as usize{
                if ranges[x] <= d && d < ranges[x+1] {
                    chosen.push(population[x+1].clone())
                }
            }
        }

        // BREEDING 
        let mut babies: Vec<Vec<bool>> = chosen.clone();
        // println!("babies: {:?}", &babies);

        for _ in 0..POPULATION_SIZE/2{
            let mut rng = rand::thread_rng();
            let two_idx = rand::seq::index::sample(&mut rng, POPULATION_SIZE as usize, 2).into_vec();
            let d = rng.gen_range(0.0..1.0);

            if d <= PC{
                // println!("cros");
                let mut rng = rand::thread_rng();
                let r = rng.gen_range(1..GENOMS_SIZE) as usize;


                let baby1 = [&chosen[two_idx[0]][..r], &chosen[two_idx[1]][r..]].concat();
                let baby2 = [&chosen[two_idx[1]][..r], &chosen[two_idx[0]][r..]].concat();

                babies[two_idx[0]] = baby1;
                babies[two_idx[1]] = baby2;

            }
        }
        // println!("After {:?}", &babies);
        
        // MUTATIONS

        for k in 0..POPULATION_SIZE as usize{
            for m in 0..GENOMS_SIZE as usize{
                let mut rng = rand::thread_rng();
                let d = rng.gen_range(0.0..1.0);
                if d <= PM{
                    babies[k][m] = !babies[k][m];
                }
            } 
        } 
        population = babies;
        eval_pop = eval_population(&function, &population);
        
        // GIF DRAWING
        if DRAW_GIF{
        root.fill(&WHITE)?;
        

        let x_axis = (-8f64..8f64).step(0.1);

        let mut cc = ChartBuilder::on(&root)
            .margin(5)
            .set_all_label_area_size(50)
            .caption(format!("Algorytm genetyczne generacja: {}", idx), ("sans-serif", 40))
            .build_cartesian_2d(-8f64..8f64, -0f64..100f64)?;

        cc.configure_mesh()
            .x_labels(20)
            .x_desc("X")
            .y_labels(10)
            .y_desc("Wartosc funkcji")
            .disable_mesh()
            .x_label_formatter(&|v| format!("{:.1}", v))
            .y_label_formatter(&|v| format!("{:.1}", v))
            .draw()?;

        cc.draw_series(LineSeries::new(x_axis.values().map(|x| (x, function(x))), &RED))?
            .label(format!("Funkcja minimalizowana: {}", input))
            .legend(|(x, y)| PathElement::new(vec![(x, y), (x+20 , y)], RED));


        cc.configure_series_labels().border_style(BLACK).draw()?;


        // Otherwise you can use a function to construct your pointing element yourself
        cc.draw_series(PointSeries::of_element(
            population.iter().map(|x| (read_value(&x), function(read_value(&x)))),
            5,
            ShapeStyle::from(&RED).filled(),
            &|coord, size, style| {
                EmptyElement::at(coord)
                    + Circle::new((0, 0), size, style)
                    // + Text::new(format!("{:?}", coord), (0, 15), ("sans-serif", 15))
            },
        ))?;


        root.present()?;
        }


    }

    
    let root_area = BitMapBackend::new("sample.png", (1024, 768)).into_drawing_area();

    root_area.fill(&WHITE)?;

    let root_area = root_area.titled("Algorytm genetyczny", ("sans-serif", 60))?;

    let (upper, lower) = root_area.split_vertically(512);

    let x_axis = (-8f64..8f64).step(0.1);

    let mut cc = ChartBuilder::on(&upper)
        .margin(5)
        .set_all_label_area_size(50)
        .caption(format!("Osobniki: {}, Generacje: {}, najlepszy osobnik ", POPULATION_SIZE, EPOCHS), ("sans-serif", 40))
        .build_cartesian_2d(-8f64..8f64, -0f64..100f64)?;

    cc.configure_mesh()
        .x_labels(20)
        .x_desc("X")
        .y_labels(10)
        .y_desc("Wartosc funkcji")
        .disable_mesh()
        .x_label_formatter(&|v| format!("{:.1}", v))
        .y_label_formatter(&|v| format!("{:.1}", v))
        .draw()?;

    cc.draw_series(LineSeries::new(x_axis.values().map(|x| (x, function(x))), &RED))?
        .label(format!("Funkcja minimalizowana: {}", input))
        .legend(|(x, y)| PathElement::new(vec![(x, y), (x+20 , y)], RED));


    cc.configure_series_labels().border_style(BLACK).draw()?;


    // Otherwise you can use a function to construct your pointing element yourself
    cc.draw_series(PointSeries::of_element(
        population.iter().map(|x| (read_value(&x), function(read_value(&x)))),
        5,
        ShapeStyle::from(&RED).filled(),
        &|coord, size, style| {
            EmptyElement::at(coord)
                + Circle::new((0, 0), size, style)
                // + Text::new(format!("{:?}", coord), (0, 15), ("sans-serif", 15))
        },
    ))?;

    let drawing_areas = lower.split_evenly((1, 2));

    let mut cc = ChartBuilder::on(&drawing_areas[0])
            .x_label_area_size(30)
            .y_label_area_size(30)
            .margin_right(20)
            .caption(format!("Avg fit",), ("sans-serif", 40))
            .build_cartesian_2d(0f64..EPOCHS as f64, 0f64..50f64)?;
        cc.configure_mesh()
            .x_labels(5)
            .y_labels(3)
            .max_light_lines(4)
            .draw()?;

        cc.draw_series(LineSeries::new(
            (0..EPOCHS as usize)
                .map(|x| (x as f64, fit_history[x]/POPULATION_SIZE as f64)),
            &BLUE,
        ))?;
    
    let mut cc = ChartBuilder::on(&drawing_areas[1])
            .x_label_area_size(30)
            .y_label_area_size(30)
            .margin_right(20)
            .caption(format!("Best fit", ), ("sans-serif", 40))
            .build_cartesian_2d(0f64..EPOCHS as f64, 0f64..90f64)?;
        cc.configure_mesh()
            .x_labels(5)
            .y_labels(3)
            .max_light_lines(4)
            .draw()?;

        cc.draw_series(LineSeries::new(
            (0..EPOCHS as usize)
                .map(|x| (x as f64, best_history[x])),
            &BLUE,
        ))?;


    // To avoid the IO failure being ignored silently, we manually call the present function
    root_area.present().expect("Unable to write result to file, please make sure 'plotters-doc-data' dir exists under current dir");
    Ok(())
}

