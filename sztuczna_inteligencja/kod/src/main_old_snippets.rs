
    // let mut tmp: Vec<f32> = Vec::new(); //temp vec fot storing calculated after activation
    // for (idx,w) in weights.iter().enumerate(){ // calc for each node
    //     let node_calc = inputs.iter().enumerate().map(|(i,x)| x*w[i]).sum::<f32>() + bias[idx]; //for each weight multiply it by every input 
    //     // println!("Primitive: {}", node_calc_primitive);
    //     // println!("Functional: {}", node_calc);
    //     tmp.push(sigmoid(node_calc));
    // }
    // let output: f32 = sigmoid(calc_node(&tmp, &out_weights) + bias[2]);
    // let error: f32 = target - output;

    // println!("{:?}", tmp);


    // let h1: Vec<f32> = inputs.iter().map(|inp| {
    //     calc_node(inp, &weights[0]) + bias[0]
    // }).collect(); // all inputs 
    // let h2: Vec<f32> = inputs.iter().map(|inp| {
    //     calc_node(inp, &weights[1]) + bias[1]
    // }).collect();
    // let o: Vec<f32> = h1.iter().zip(h2.iter()).map(|(res1, res2)| {
    //     sigmoid(sigmoid(*res1)*out_weights[0] + sigmoid(*res2)*out_weights[1] + bias[2])
    // }).collect();
    // 
    // let o_errors: Vec<f32> = target.iter().zip(o.iter()).map(|(tar, pred)| {
    //     tar - pred
    // }).collect(); 
    // let dz: Vec<f32> = o_errors.iter().zip(o).map(|(err, out)|{
    //     err*sigmoid_deriative(out)
    // }).collect();
    //
    //     // let val:f32 = sigmoid(1f32);

    // let sigmoidd = learn(
    //     &inputs,
    //     &outputs,
    //     &mut weights,  
    //     &mut output_weights, 
    //     sigmoid,
    //     sigmoid_deriative,
    //     false,
    //     EPOCHS,
    //     0.5,
    //     0.9
    // );
    // let s_points: Vec<(f32, f32)> = (0..=sigmoid_false.len()).zip(sigmoid_false.iter()).map(|(x,y)| (x as f32, *y)).collect();
    // let tan: Vec<f32> = learn(
    //     &inputs,
    //     &outputs,
    //     &mut weights2,  
    //     &mut output_weights2, 
    //     hyp_tan,
    //     hyp_tan_deriative,
    //     true,
    //     EPOCHS,
    //     0.5,
    //     0.9
    // );
    
    // let tan: Vec<(f32, f32)> = (0..=tan.len()).zip(sigmoid_true.iter()).map(|(x,y)| (x as f32, *y)).collect();


