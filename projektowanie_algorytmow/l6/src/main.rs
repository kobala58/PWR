use std::time::Instant;
use plotters::prelude::*;
use rand::{Rng, SeedableRng};
use rand::rngs::StdRng;

fn generate_key_pair(p: u64, q: u64) -> (u64, u64, u64) {
    let n = p * q;
    let phi = (p - 1) * (q - 1);

    let mut rng = StdRng::from_entropy();
    let mut e = rng.gen_range(2..phi);
    while gcd(e, phi) != 1 {
        e = rng.gen_range(2..phi);
    }

    let d = mod_inv(e, phi);

    (n, e, d)
}

fn gcd(a: u64, b: u64) -> u64 {
    if b == 0 {
        a
    } else {
        gcd(b, a % b)
    }
}

fn mod_inv(a: u64, m: u64) -> u64 {
    let mut a = a as i64;
    let mut m = m as i64;

    let mut x = 0;
    let mut y = 1;
    let mut u = 1;
    let mut v = 0;

    while a != 0 {
        let q = m / a;
        let r = m % a;
        let m1 = x - u * q;
        let m2 = y - v * q;

        m = a;
        a = r;
        x = u;
        y = v;
        u = m1;
        v = m2;
    }

    while x < 0 {
        x += m;
    }

    x as u64
}

fn encrypt(message: &str, n: u64, e: u64) -> Vec<u64> {
    let mut ciphertext = Vec::new();
    let block_size = ((n as f64).log2() / 8.0).floor() as usize;

    for chunk in message.as_bytes().chunks(block_size) {
        let mut num = 0;
        for &byte in chunk {
            num = (num << 8) | byte as u64;
        }
        let encrypted = pow_mod(num, e, n);
        ciphertext.push(encrypted);
    }

    ciphertext
}

fn decrypt(ciphertext: &[u64], n: u64, d: u64) -> String {
    let mut message = String::new();
    let block_size = ((n as f64).log2() / 8.0).floor() as usize;

    for &num in ciphertext {
        let mut decrypted = pow_mod(num, d, n);
        let mut bytes = vec![0; block_size];
        for i in (0..block_size).rev() {
            bytes[i] = (decrypted & 0xff) as u8;
            decrypted >>= 8;
        }
        message.push_str(std::str::from_utf8(&bytes).unwrap());
    }

    message
}

fn pow_mod(base: u64, exponent: u64, modulus: u64) -> u64 {
    let mut result = 1;
    let mut base = base % modulus;

    let mut exponent = exponent;
    while exponent > 0 {
        if exponent % 2 == 1 {
            result = (result * base) % modulus;
        }

        exponent >>= 1;
        base = (base * base) % modulus;
    }

    result
}

fn fermat_test(n: u64, k: usize) -> bool {
    if n <= 1 || n == 4 {
        return false;
    }

    if n <= 3 {
        return true;
    }

    let mut rng = StdRng::from_entropy();
    for _ in 0..k {
        let a = rng.gen_range(2..n-1);
        if pow_mod(a, n-1, n) != 1 {
            return false;
        }
    }

    true
}

fn miller_rabin_test(n: u64, k: usize) -> bool {
    if n <= 1 || n == 4 {
        return false;
    }

    if n <= 3 {
        return true;
    }

    let mut rng = StdRng::from_entropy();
    let mut d = n - 1;
    while d % 2 == 0 {
        d /= 2;
    }

    for _ in 0..k {
        let mut a = rng.gen_range(2..n-1);
        let mut x = pow_mod(a, d, n);

        if x == 1 || x == n - 1 {
            continue;
        }

        let mut i = 0;
        while i < (n - 1) / 2 {
            x = (x * x) % n;

            if x == 1 {
                return false;
            }

            if x == n - 1 {
                break;
            }

            i += 1;
        }

        if x != n - 1 {
            return false;
        }
    }

    true
}

fn ex3_2() {
    let a = 123456789;
    let m = 100;
    let mut euclid_times: Vec<u128> = Vec::new();
    let mut factorization_times: Vec<u128> = Vec::new();

    for b in 1..=m {
        let start_euclid = Instant::now();
        let _ = gcd_euclid(a, b);
        let end_euclid = Instant::now();
        euclid_times.push(end_euclid.duration_since(start_euclid).as_micros());

        let start_factorization = Instant::now();
        let _ = gcd_factorization(a, b);
        let end_factorization = Instant::now();
        factorization_times.push(end_factorization.duration_since(start_factorization).as_micros());
    }

    // wyświetlanie wykresu
    let root = BitMapBackend::new("gcd_plot.png", (640, 480)).into_drawing_area();
    root.fill(&WHITE).unwrap();

    let max_time = euclid_times.iter().max().unwrap();
    let max_b = m as u128;
    let mut chart = ChartBuilder::on(&root)
        .caption("Czas działania funkcji gcd dla a=123456789", ("sans-serif", 20).into_font())
        .margin(10)
        .x_label_area_size(30)
        .y_label_area_size(40)
        .build_cartesian_2d(0..max_b, 0..*max_time)
        .unwrap();

    chart.configure_mesh().draw().unwrap();
    let points: Vec<(u128, u128)> = (1..=m).zip(euclid_times.iter().map(|t| *t as f32)).map(|(x,y)| (x as u128,y as u128)).collect();

    chart.draw_series(LineSeries::new(
        points,
        &BLUE,
    )).unwrap()
    .label("Algorytm Euklidesa")
    .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &BLUE));
    let fact_times_vec: Vec<(u128, u128)> = (1..=m).zip(factorization_times.iter().map(|t| *t as f32)).map(|(x,y)| (x as u128, y as u128)).collect();
 
    chart.draw_series(LineSeries::new(
        fact_times_vec,
        &RED,
    )).unwrap()
    .label("Algorytm faktoryzacyjny")
    .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &RED));

    chart.configure_series_labels()
        .background_style(&WHITE.mix(0.8))
        .border_style(&BLACK)
        .draw().unwrap();
}

fn prime_factors(n: u64) -> Vec<u64> {
    let mut factors = Vec::new();

    for i in 2..=n {
        if n % i == 0 {
            factors.push(i);
            factors.extend(prime_factors(n / i));
            break;
        }
    }

    factors
}

fn sieve_of_eratosthenes(p: u32) -> Vec<u32> {
    let mut primes = vec![true; (p+1) as usize];
    primes[0] = false;
    primes[1] = false;

    for i in 2..=(p as f64).sqrt() as u32 {
        if primes[i as usize] {
            let mut j = i*i;
            while j <= p {
                primes[j as usize] = false;
                j += i;
            }
        }
    }

    primes.iter()
        .enumerate()
        .filter(|(_, &is_prime)| is_prime)
        .map(|(prime, _)| prime as u32)
        .collect()
}

fn gcd_euclid(mut a: u64, mut b: u64) -> u64 {
    while b != 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    a
}

fn gcd_factorization(mut a: u64, mut b: u64) -> u64 {
    let mut factors_a: Vec<u64> = Vec::new();
    let mut factors_b: Vec<u64> = Vec::new();
    let mut i = 2;

    // znajdujemy czynniki pierwsze liczby a
    while i <= a {
        if a % i == 0 {
            factors_a.push(i);
            a /= i;
        } else {
            i += 1;
        }
    }

    i = 2;

    // znajdujemy czynniki pierwsze liczby b
    while i <= b {
        if b % i == 0 {
            factors_b.push(i);
            b /= i;
        } else {
            i += 1;
        }
    }

    // znajdujemy wspólne czynniki
    let mut gcd = 1;
    for factor in factors_a.iter() {
        if factors_b.contains(factor) {
            gcd *= factor;
            factors_b.remove(factors_b.iter().position(|&x| x == *factor).unwrap());
        }
    }

    gcd
}

fn ex4(){
    // Wybieramy liczby p i q
    let p: u64 = 881;
    let q: u64 = 883;
   
    let (n, e, d) = generate_key_pair(p, q);

    // Tekst, który chcemy zaszyfrować
    let plaintext = "Tajna wiadomość";

    // Szyfrowanie
    let ciphertext = encrypt(plaintext, e, n);
    println!("Zaszyfrowana wiadomość: {:?}", ciphertext);

    // Odszyfrowanie
    let decrypted_plaintext = decrypt(&ciphertext, d, n);
    println!("Odszyfrowana wiadomość: {:?}", String::from_utf8_lossy(&decrypted_plaintext.as_bytes()));
}

fn main() {
    let n = 192;
    let factors = prime_factors(n);
    println!("Czynniki pierwsze liczby {}: {:?}", n, factors);

    let p = 30;
    let primes = sieve_of_eratosthenes(p);
    println!("Liczby pierwsze mniejsze lub równe {}: {:?}", p, primes);

    ex4();
}
