
    let mut tmp: Vec<f32> = Vec::new(); //temp vec fot storing calculated after activation
    for (idx,w) in weights.iter().enumerate(){ // calc for each node
        let node_calc = inputs.iter().enumerate().map(|(i,x)| x*w[i]).sum::<f32>() + bias[idx]; //for each weight multiply it by every input 
        // println!("Primitive: {}", node_calc_primitive);
        // println!("Functional: {}", node_calc);
        tmp.push(sigmoid(node_calc));
    }
    let output: f32 = sigmoid(calc_node(&tmp, &out_weights) + bias[2]);
    let error: f32 = target - output;

    println!("{:?}", tmp);
