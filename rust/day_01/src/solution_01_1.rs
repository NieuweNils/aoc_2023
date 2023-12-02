use std::env;

use dotenv::dotenv;
use regex::Regex;

static DAY: &'static str = "1";

#[tokio::main]
async fn main() {
    // Load session cookie from .env file
    dotenv().ok();
    let session_cookie = env::var("SESSION_COOKIE").expect("Environment variable $SESSION_COOKIE is necessary but not set.");
    let request_header_session_cookie = format!("session={}", session_cookie);

    // call AoC API for data
    let url = format!("https://adventofcode.com/2023/day/{}/input", DAY);
    let client = reqwest::Client::new();
    let data = client
        .get(url)
        .header("Cookie", request_header_session_cookie)
        .send()
        .await
        .unwrap().text()
        .await
        .unwrap()
        ;
    let lines = data.split_whitespace();

    // unpack data
    let calibration_vector = lines.collect::<Vec<&str>>(); //

    // unpack further into a 2D vector, filter for digits with a regex
    let re = Regex::new(r"\d").unwrap();
    let mut numbers: Vec<Vec<&str>> = Vec::new();

    for entry in calibration_vector {
        let regex_hits: Vec<_> = re.find_iter(entry)
            .map(|digits| digits.as_str())
            .collect();
        numbers.push(regex_hits);
    }

    // combine first and last digits to final number
    let mut cleaned_calibration_vector = vec![];
    let mut counter = 0;
    for vector in &numbers {
        counter += 1;
        if counter == 1001 {
            print!("{:?}", cleaned_calibration_vector);
        }
        let first_number = vector.first().unwrap();
        let last_number: &str = vector.last().unwrap();

        let mut total_number: String = "".to_owned();
        total_number.push_str(first_number);
        total_number.push_str(last_number);
        let total_int: i64 = total_number.parse().unwrap();
        cleaned_calibration_vector.push(total_int);
    }
    let answer: i64 = cleaned_calibration_vector.iter().sum();
    println!("{}", answer);
}