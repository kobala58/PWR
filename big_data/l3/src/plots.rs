use plotters::prelude::*;

pub fn test_draw() -> Result<(), Box<dyn std::error::Error>> {
    let root = BitMapBackend::new("images/0.png", (640, 480)).into_drawing_area();
    root.fill(&WHITE)?;
    let mut chart = ChartBuilder::on(&root)
        .caption("y=x^2", ("sans-serif", 50).into_font())
        .margin(5)
        .x_label_area_size(30)
        .y_label_area_size(30)
        .build_cartesian_2d(-1f32..1f32, -0.1f32..1f32)?;

    chart.configure_mesh().draw()?;

    chart
        .draw_series(LineSeries::new(
            (-50..=50).map(|x| x as f32 / 50.0).map(|x| (x, x * x)),
            &RED,
        ))?
        .label("y = x^2")
        .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &RED));

    chart
        .configure_series_labels()
        .background_style(&WHITE.mix(0.8))
        .border_style(&BLACK)
        .draw()?;

    root.present()?;

    Ok(())
}

pub fn draw_plots(data: &[Vec<f32>; 4], size: f32) -> Result<(), Box<dyn std::error::Error>>{

    let ranges: [[std::ops::Range<f32>; 2]; 4] = [[0f32..size, -1f32..50f32],[0f32..size, -0.5f32..1.5f32],[0f32..size, -2f32..2f32],[0f32..size, 0.5f32..3.5f32]]; // ranges of plots
    let labels: [&str; 4] = ["Generated data", "Min-Max Normalization", "Standarized", "Rescaled"]; 
    let root = BitMapBackend::new("images/l3.png", (500, 1000)).into_drawing_area();
    root.fill(&WHITE)?;
    let root = root.titled("L3 plots", ("sans-serif", 60))?;

    // divide areas
    let areas = root.split_evenly((4,1));
    for (area, idx) in areas.iter().zip(1..){
        let mut cc = ChartBuilder::on(&area)
            .x_label_area_size(30)
            .y_label_area_size(30)
            .margin_right(20)
            .caption(format!("{}",labels[idx-1]), ("sans-serif", 40))
            .build_cartesian_2d(0i32..size as i32, ranges[idx-1][1].clone())?;
        cc.configure_mesh()
            .x_labels(5)
            .y_labels(3)
            .max_light_lines(4)
            .draw()?;
        cc.draw_series(LineSeries::new(
            data[idx-1].iter() 
                .enumerate()
                .map(|(i, &y)| (i as i32, y)),
            &BLUE,
        ))?;
    }
    root.present().expect("Nwm");
    Ok(())

}
