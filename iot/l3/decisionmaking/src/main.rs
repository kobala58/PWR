use std::thread;
use std::time::Duration;
use serde_json;
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::Read;
use std::io;
use rocket;
use rocket::routes;
use paho_mqtt as mqtt;
use std::process;
use rocket::serde::json::Json;


#[derive(Serialize, Deserialize)]
struct Config {
    wattage: u32, 
    is_on: bool,
}

fn mqtt_publish(data: &str) -> () {
    // Create a client & define connect options
    let cli = mqtt::Client::new("tcp://localhost:1883").unwrap_or_else(|err| {
        println!("Error creating the client: {:?}", err);
        process::exit(1);
    });

    let conn_opts = mqtt::ConnectOptionsBuilder::new()
        .keep_alive_interval(Duration::from_secs(20))
        .clean_session(true)
        .finalize();

    // Connect and wait for it to complete or fail
    cli.connect(conn_opts);

    // Create a message and publish it
    let msg = mqtt::Message::new("/heater/temp", data, 0);
    let tok = cli.publish(msg);


    // Disconnect from the broker
    let tok = cli.disconnect(None);
    }

#[rocket::get("/")]
fn index() -> &'static str {
    "Hello, world!"
}

#[rocket::post("/config", format = "application/json", data = "<config>")]
fn config(config: Json<Config>) -> &'static str {
    // let mut file = File::create("config.json").expect("couldn't create file");
    println!("{}", config);
    "Data saved to file"
}

#[rocket::main]
async fn main() -> Result<(), rocket::Error> { 
    
    thread::spawn(move || {
        let outside: f64 = 10.0;
        let mut cycles_off: i32 = 0;
        let mut cycles_on: i32 = 0;
        let mut temp: f64 = outside as f64; 

        loop 
        {
            // Opening config file
            let mut file = File::open("config.json").unwrap();
            let mut buff = String::new();
            file.read_to_string(&mut buff).unwrap();
            let config: Config = serde_json::from_str(&buff).unwrap();
            //ACTUATOR 
            
            if config.is_on == true{ //if is power on turn on heating
                cycles_off = 0; // reset off counter
                if cycles_on >= 0 && cycles_on <= 5 {
                    // heating starts, temp raises a little
                    cycles_on += 1;
                    temp = temp + f64::from(0.001) * f64::from(config.wattage);
                }
                else
                {
                    temp = temp + f64::sqrt(f64::from(0.001) * f64::from(config.wattage)) as f64;
                }
            }
            else { //when config says false
                if cycles_off <= 5 {
                    cycles_on = 0;
                    cycles_off += 1;
                    temp -= f64::from(0.01) * f64::from(cycles_off);

                }
                else
                {
                    cycles_on = 0;
                    temp -= 0.1; //temp decline
                    if temp < outside{
                        temp = outside;
                    }         
                }
            }

            //TODO: mqtt sending
            mqtt_publish(&temp.to_string());
            thread::sleep(Duration::from_secs(5)); // sleep at the end of executing loop
        }});

    let _rocket = rocket::build()
        .mount("/hello", routes![index])
        .launch()
        .await?;
    
    Ok(())
}
