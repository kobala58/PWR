use std::thread;
use std::time::Duration;
use serde_json;
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::Read;
use std::io;
use rumqttc::{Client, MqttOptions, QoS};
use rumqttc::mqttbytes::v4::ConnectReturnCode;

// config.json serializer
#[derive(Serialize, Deserialize)]
struct Config {
    wattage: u32, 
    is_on: bool,
}



fn mqtt_publish(data: &str) -> Result<(), io::Error> {
    let topic = String::from("/act");
    let server = String::from("localhost");
    let mqtt_options = MqttOptions::new("RustPublisher", server, 1883);
    let (mut mqtt_client, notifications) = Client::new(mqtt_options, 10);

    mqtt_client.subscribe(topic, QoS::AtLeastOnce).unwrap();

    let result = mqtt_client.publish(topic, QoS::AtLeastOnce, false, data.as_bytes()).unwrap();

    match result {
        ConnectReturnCode::Success => println!("Data: {} was sent to topic: {}", data, topic),
        _ => println!("Error occured while sending data"),
    }

    for notification in notifications {
        match notification {
            _ => (),
        }
    }
    Ok(())
}

fn main() {

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
        }

    });
    loop {
        thread::sleep(Duration::from_secs(5));
    }
}
