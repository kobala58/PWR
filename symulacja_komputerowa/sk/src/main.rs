#![allow(unused)]

use clap::Parser;

#[derive(Parser)]
struct Cli {
    distrib_type: String,
    pattern: String,
    path: std::path::PathBuf,
}

fn main() {
    let args = Cli::parse();
    println!("{}", args.distrib_type);
}
