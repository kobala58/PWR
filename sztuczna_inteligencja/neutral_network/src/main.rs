use std::i8;

use rand::{Rng, seq::SliceRandom, thread_rng};

fn sigmoid(x: f32) -> f32{
    1f32/(1f32+f32::exp(-x)) // 1/(1-e^-x)
}

#[allow(dead_code)]
fn calc_node(params: &Vec<f32>, weights: &Vec<f32>) -> f32 {
    params.iter().zip(weights.iter()).map(|(x, y)| x * y).sum() // techinicznie może da się to zrobić lepiej ale ja na ten moment tego nie postrafie
}

#[allow(dead_code)]
#[allow(unused_variables)]
fn learn(inputs: &Vec<f32>,
        target: &f32, weights: &mut Vec<Vec<f32>>, bias: &mut Vec<f32>, out_weights: &mut Vec<f32>) {
    // przygotuj 
    
    // let s1 = inputs[0]*weights[0][0]+inputs[1]*weights

    let mut tmp: Vec<f32> = Vec::new(); //temp vec fot storing calculated after activation
    for (idx,w) in weights.iter().enumerate(){ // calc for each node
        // println!("--------------------------");
        // println!("Input: {:?}", inputs);
        // println!("");
        // println!("w{}: {:?}", idx+1,w);
        // let node_calc_primitive = inputs[0]*w[0]+inputs[1]*w[1]+bias[idx];
        let node_calc = inputs.iter().enumerate().map(|(i,x)| x*w[i]).sum::<f32>() + bias[idx]; //for each weight multiply it by every input 
        // println!("Primitive: {}", node_calc_primitive);
        // println!("Functional: {}", node_calc);
        tmp.push(sigmoid(node_calc));
    }
    let output: f32 = sigmoid(calc_node(&tmp, &out_weights) + bias[2]);
    let error: f32 = target - output;
    let derror: f32 =

    println!("{:?}", tmp);



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

    for _ in 1..EPOCHS{
        let mut rnd_vec: Vec<usize> = (0..4).collect();
        rnd_vec.shuffle(&mut thread_rng());
        for idx in rnd_vec.into_iter(){
            learn(&inputs[idx], &outputs[idx], &mut weights, &mut bias, &mut output_weights);
        }
    }

    // learn(EPOCHS, &inputs, &outputs, &mut weights, &mut bias, &mut output_weights, 0.5f32);

    println!("{}", val);
}
