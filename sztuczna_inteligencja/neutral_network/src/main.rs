use std::i8;

use rand::{Rng, seq::SliceRandom, thread_rng};

fn sigmoid(x: f32) -> f32{
    1f32/(1f32+f32::exp(-x)) // 1/(1-e^-x)
}

fn sigmoid_deriative(x: f32) -> f32{
    f32::exp(x)/((1f32+f32::exp(x)).powi(2))
}

#[allow(dead_code)]
fn calc_node(params: &Vec<f32>, weights: &Vec<f32>) -> f32 {
    params.iter().zip(weights.iter()).map(|(x, y)| x * y).sum()  // techinicznie może da się to zrobić lepiej ale ja na ten moment tego nie postrafie
}

#[allow(dead_code)]
#[allow(unused_variables)]

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
    
    let o_errors: Vec<f32> = target.iter().zip(o.iter()).map(|(tar, pred)| {
        tar - pred
    }).collect(); 
    let dz: Vec<f32> = o_errors.iter().zip(o).map(|(err, out)|{
        err*sigmoid_deriative(out)
    }).collect();

    //
    //--v
    //          out_a -> wynik
    //(z2 | a2)-()-^
    //
    let error: f32 = 0.0;
    while true{
        for (inp, out) in inputs.iter().zip(target){
            let z1: f32 = calc_node(inp, &weights[0]) + bias[0];
            let z2: f32 = calc_node(inp, &weights[1]) + bias[1];
            let pred: f32 = activator(z1) * out_weights[0] + activator(z2) * out_weights[1] + bias[3];
            let error: f32 = out - activator(pred);
            let errorw: f32 = dactivator(error.powi(2));

            if momentum == true{
            weights.iter().map(|w|{
                    w[0]+
                })
            }
            else{
            
            }


            }
    }
}

#[allow(dead_code)]
fn main() {
    let mut rng = rand::thread_rng();

    // declaring constans to adjust later
    const VARIANCE_W: f32 = 0.5f32;
    const EPOCHS: usize = 2;
    
    // declaring random weights for inputs nodes
    // [[w11,w12], [w21,w22], [b1,b2]]
    let mut weights: Vec<Vec<f32>> = vec![
                                        vec![rng.gen::<f32>(),rng.gen::<f32>()], // w11, w12,
                                        vec![rng.gen::<f32>(),rng.gen::<f32>()], // w21, w22
    ];
    let mut bias =  vec![rng.gen::<f32>(),rng.gen::<f32>(), rng.gen::<f32>()]; // b1 b2 b3

    let mut output_weights: Vec<f32> = vec![rng.gen::<f32>(),rng.gen::<f32>()]; //o1 o2
    
    let inputs: Vec<Vec<f32>> = vec![
        vec![0f32,0f32],
        vec![0f32,1f32],
        vec![1f32,0.0],
        vec![1.0,1.0]
    ];
    
    let outputs: Vec<f32> = vec![0.0,1.0,1.0,0.0];
    
     
    let val:f32 = sigmoid(1f32);


    learn(&inputs, &outputs, &mut weights, &mut bias, &mut output_weights, sigmoid, EPOCHS);

    println!("{}", val);
}
