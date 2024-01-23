use core::panic;

use plotters::{prelude::*, style::full_palette::{RED, PURPLE, BLUE}};
use rand::Rng;

fn sigmoid(x: f32) -> f32{
    1f32/(1f32+f32::exp(-x)) // 1/(1-e^-x)
}

fn sigmoid_deriative(x: f32) -> f32{
    f32::exp(x)/((1f32+f32::exp(x)).powi(2))
}

fn hyp_tan(x: f32) -> f32{
    f32::tanh(x)
}

fn hyp_tan_deriative(x: f32) -> f32{
    1f32 - f32::tanh(x).powi(2)
}

fn relu(x: f32) -> f32{
    x.max(0f32)
}

fn relu_deriative(x: f32) -> f32{
    match x {
        x if x < 0f32  => {
            0f32
        },
        x if x > 0f32 => {
            1f32
        }
        _ => {
            // panic!("ReLu equals 0")
            0.01f32
        }
    }
}

fn leaky_relu(x: f32) -> f32{
    match x{
        x if x <= 0f32 => 0.1f32*x,
        x if x > 0f32 => x,
        _ => panic!("Idk")
    }
}

fn leaky_relu_deriative(x: f32) -> f32{
    match x{
        x if x <= 0f32 => 0.01f32,
        x if x > 0f32 => 1f32,
        _ => panic!("IDK loose relu deriative")
    }
}

#[allow(dead_code)]
fn calc_node(params: &Vec<f32>, weights: &Vec<f32>) -> f32 {
    params.iter().zip(weights.iter()).map(|(x, y)| x * y).sum()  // techinicznie może da się to zrobić lepiej ale ja na ten moment tego nie postrafie
}


fn learn(inputs: &Vec<Vec<f32>>, target: &Vec<f32>,
        weights: &mut Vec<Vec<f32>>, bias: &mut Vec<f32>,
        out_weights: &mut Vec<f32>, activator: fn(f32) -> f32, dactivator: fn(f32),epochs: usize) {
    // main function for learing 
    let err: f32 = 0.0;
    let n: f32 = 1.0;
    // here we can implement loop

    // TODO: TEMP SOLUTION. MAKE AVIABLE TO SWITCH ACTIVATORS
    let z1: Vec<f32> = inputs.iter().map(|inp| {
        calc_node(inp, &weights[0]) + bias[0]
    }).collect(); // all inputs 
    let z2: Vec<f32> = inputs.iter().map(|inp| {
        calc_node(inp, &weights[1]) + bias[1]
    }).collect();
    let o: Vec<f32> = z1.iter().zip(z2.iter()).map(|(res1, res2)| {
        sigmoid(sigmoid(*res1)*out_weights[0] + sigmoid(*res2)*out_weights[1] + bias[2])
    }).collect();
    
    let mut wm: Vec<f32> = out_weights.iter().map(|_x|{1f32}).collect();

    let mut history: Vec<f32> = vec![];
    let mut iter = 0;
    let mut error: f32 = 10000000.0;
    println!("{:?}", weights);
    while iter<epochs{
        error = 0.0;


        for (inp, out) in inputs.iter().zip(target){
            let h1: f32 = calc_node(inp, &weights[0]);
            let y1: f32 = activator(h1);
            let h2: f32 = calc_node(inp, &weights[1]);
            let y2: f32 = activator(h2);
            let pred: f32 = activator(h1) * out_weights[0] + activator(h2) * out_weights[1] - out_weights[2]; // before
            let pred_out: f32 = activator(pred); // network output after activation
            // activation

            error = error + 0.5*(out - pred_out).powi(2); //
            
            let deltaz: f32 = (out-pred_out)*activator_deriative(pred_out);
            let deltay1: f32 = activator_deriative(h1)*deltaz*out_weights[0];
            let deltay2: f32 = activator_deriative(h2)*deltaz*out_weights[1];
            
            if momentum == true {

                // Output layer
                out_weights[0] += n*deltaz*y1+alpha*wm[0];
                wm[0] = n*deltaz*y1;
                out_weights[1] += n*deltaz*y2+alpha*wm[1];
                wm[1] = n*deltaz*y2;
                out_weights[2] -= n*deltaz+alpha*wm[2];
                wm[2] = n*deltaz;


                // hidden layers
                weights[0][0] += n*deltay1*inp[0] + alpha*vm[0][0]; // w11 == w00 
                vm[0][0] = n*deltay1*inp[0]; 
                weights[0][1] += n*deltay1*inp[1] + alpha*vm[0][1]; // w12 == w01
                vm[0][1] = n*deltay1*inp[1];
                weights[0][2] += inp[2]*n*deltay1 + alpha*vm[0][1]; // w13 == w02
                vm[0][2] = n*deltay1;
                
                weights[1][0] += n*deltay2*inp[0] + alpha*vm[1][0]; // w21 == w10
                vm[1][0] = n*deltay2*inp[0]; 
                weights[1][1] += n*deltay2*inp[1] + alpha*vm[1][1]; // w22 == w11
                vm[1][1] = n*deltay2*inp[1];
                weights[1][2] += inp[2]*n*deltay2 + alpha*vm[0][1]; // w13 == w02
                vm[1][2] = n*deltay2;
            }
            else {

                out_weights[0] += n*deltaz*y1;
                out_weights[1] += n*deltaz*y2;
                out_weights[2] -= n*deltaz;

                weights[0][0] += n*deltay1*inp[0]; // w11 == w00 
                weights[0][1] += n*deltay1*inp[1]; // w12 == w01
                weights[0][2] += n*deltay1*inp[2]; // w13 == w02 bias
                weights[1][0] += n*deltay2*inp[0]; // w21 == w10
                weights[1][1] += n*deltay2*inp[1]; // w22 == w11
                weights[1][2] += n*deltay2*inp[2]; // w23 == w12 bias
                
            }

            }
        iter += 1;
        history.push(error);
            // println!("Iter {}: error: {}",iter,error);

    }
            println!("Iter {}: error: {}",iter,error);

    history
}
#[allow(unused_mut)]
#[allow(dead_code)]

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut rng = rand::thread_rng();

    // declaring constans to adjust later
    const VARIANCE_W: f32 = 0.5f32;
    const EPOCHS: usize = 8000;
    
    // declaring random weights for inputs nodes
    let mut weights: Vec<Vec<f32>> = vec![
                                        vec![rng.gen::<f32>(),rng.gen::<f32>(),rng.gen::<f32>()], // w11, w12, w13
                                        vec![rng.gen::<f32>(),rng.gen::<f32>(),rng.gen::<f32>()], // w21, w22, w23
    ];
    
    // declaring output_weights
    let mut output_weights: Vec<f32> = vec![rng.gen::<f32>(),rng.gen::<f32>(),rng.gen::<f32>()]; //o1 o2 o3

    let inputs: Vec<Vec<f32>> = vec![
        vec![0f32,0f32, -1f32],
        vec![0f32,1f32, -1f32],
        vec![1f32,0.0, -1f32],
        vec![1.0,1.0, -1f32]
    ];
    
    let outputs: Vec<f32> = vec![0.0,1.0,1.0,0.0];
    
     
    let root = BitMapBackend::new("res2.png", (2000, 1000)).into_drawing_area();
    root.fill(&WHITE).unwrap();
    let mut chart = ChartBuilder::on(&root)
        .caption("Różne dostępne aktywatory", ("sans-serif", 50).into_font())
        .margin(5)
        .x_label_area_size(30)
        .y_label_area_size(30)
        .build_cartesian_2d(0f32..EPOCHS as f32, 0f32..0.6f32).unwrap();
    chart.configure_mesh().draw().unwrap();

    let mut idx = 0; 
    for (actv, dactv, name, color) in vec![(sigmoid as fn(f32) -> f32, sigmoid_deriative as fn(f32) -> f32, "Sigmoid", RED),
        (hyp_tan as fn(f32) -> f32, hyp_tan_deriative as fn(f32) -> f32, "Hyperbolic tan", GREEN), 
        (relu as fn(f32) -> f32, relu_deriative as fn(f32) -> f32, "ReLU", PURPLE),
    (leaky_relu, leaky_relu_deriative, "Leaky ReLU", BLUE)]
        {
        let mut vtemp = weights.clone();
        let mut wtemp = output_weights.clone();
        let learn_res = learn(
            &inputs,
            &outputs,
            &mut vtemp,  
            &mut wtemp, 
            actv,
            dactv,
            true,
            EPOCHS,
            0.5,
            0.9
            );
        let points: Vec<(f32, f32)> = (0..=learn_res.len()).zip(learn_res.iter()).map(|(x,y)| (x as f32, *y)).collect();
        let mut rng = rand::thread_rng();
        // let color = RGBColor(
        //     rng.gen_range(0..255), 
        //     rng.gen_range(0..255), 
        //     rng.gen_range(0..255)
        //     );
        let color = Palette99::pick(idx).mix(0.9);
        idx += 1;
        chart.draw_series(LineSeries::new(
            points, color.stroke_width(1)
        ))?
        .label(name)
        .legend(move |(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], color.filled()));
        
        }
    // let steps: Vec<f32> = (1..=9).map(|i| i as f32 * 0.1).collect();

    // for step in steps
    //         {
    //     let mut vtemp = weights.clone();
    //     let mut wtemp = output_weights.clone();
    //     let learn_res = learn(
    //         &inputs,
    //         &outputs,
    //         &mut vtemp,  
    //         &mut wtemp, 
    //         sigmoid,
    //         sigmoid_deriative,
    //         true,
    //         EPOCHS,
    //         step,
    //         0.9
    //         );
    //     let points: Vec<(f32, f32)> = (0..=learn_res.len()).zip(learn_res.iter()).map(|(x,y)| (x as f32, *y)).collect();
    //     let color = Palette99::pick(idx).mix(0.9);
    //     idx += 1;
    //     chart.draw_series(LineSeries::new(
    //         points, color.stroke_width(1)
    //     ))?
    //     .label(step.to_string())
    //     .legend(move |(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], color.filled()));
    //     
    //     }



    
    chart.configure_series_labels()
        .background_style(&WHITE.mix(0.8))
        .border_style(&BLACK)
        .draw().unwrap();

    Ok(())
}
