use rand::Rng;

fn sigmoid(x: f32) -> f32{
    1f32/(1f32+f32::exp(-x)) // 1/(1-e^-x)
}

#[allow(dead_code)]
fn calc_node(params: Vec<f32>, weights: Vec<f32>) -> f32 {
    params.iter().zip(weights.iter()).map(|(x, y)| x * y).sum() // techinicznie może da się to zrobić lepiej ale ja na ten moment tego nie postrafie
}

#[allow(dead_code)]
#[allow(unused_variables)]
fn learn(epochs: i32, inputs: &Vec<Vec<f32>>,
        outputs: &Vec<f32>, weights: &mut Vec<Vec<f32>>, bias: &mut Vec<f32>, out_weights: &mut Vec<f32>, alpha: f32) {
    let mut tmp: Vec<f32> = Vec::new();
    for (idx,w) in weights.iter().enumerate(){ // calc for each node
        println!("w: {:?}", w);
        tmp.push(inputs.iter().map(|x| x[0]*w[0]+x[1]*w[1]).sum());
        
    }
    println!("{:?}", tmp);



}

#[allow(dead_code)]
fn main() {
    let mut rng = rand::thread_rng();

    // declaring constans to adjust later
    const VARIANCE_W: f32 = 0.5f32;
    const EPOCHS: i32 = 10000;
    
    // declaring random weights for inputs nodes
    // [[w11,w12], [w21,w22], [b1,b2]]
    let mut weights: Vec<Vec<f32>> = vec![
                                        vec![rng.gen::<f32>(),rng.gen::<f32>()], // w11, w12,
                                        vec![rng.gen::<f32>(),rng.gen::<f32>()], // w21, w22
    ];
    let mut bias =  vec![rng.gen::<f32>(),rng.gen::<f32>()];

    let mut output_weights: Vec<f32> = vec![rng.gen::<f32>(),rng.gen::<f32>()];
    
    let inputs: Vec<Vec<f32>> = vec![
        vec![0f32,0f32],
        vec![0f32,1f32],
        vec![1f32,0.0],
        vec![1.0,1.0]
    ];
    
    let outputs: Vec<f32> = vec![0.0,1.0,1.0,0.0];
    
     
    let val:f32 = sigmoid(1f32);

    learn(EPOCHS, &inputs, &outputs, &mut weights, &mut bias, &mut output_weights, 0.5f32);

    println!("Hello, world! {}", val);
}
