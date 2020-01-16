use std::fs::File;
use std::io::Write;
use std::{fs};
use serde_derive::{Serialize, Deserialize};
use failure;
use std::process::{Command, Stdio};
use std::path::Path;


#[derive(Serialize, Deserialize)]
pub struct Settings {
    work_dir: String,
    terminal: String, 

    command: String, 
    inputs: Vec<String>, 
    result: i32, 

    chain_settings: String, 

    failed_command: String, 
}

impl Settings {
    pub fn new(path: &str) -> Result<Self, failure::Error> {
        let text = fs::read_to_string(&path)?;
        let settings = toml::from_str(&text)?;
        Ok(settings)
    }

    pub fn default() -> Self {
        Settings{
            work_dir: ".".to_string(), 
            terminal: "".to_string(), 

            command: "".to_string(), 
            inputs: Vec::new(), 
            result: 0, 

            chain_settings: "".to_string(), 
            
            failed_command: "".to_string(), 
        }
    }
}

pub fn write_settings(path: &str, settings: &Settings) -> Result<(), failure::Error> {
    let mut file = File::create(path)?;
    let text = toml::to_string(settings)?;
    write!(&mut file, "{}", text)?;
    Ok(())
}

pub fn exec_command(settings: &Settings) -> Result<(), failure::Error> {
    match _exec_command(&settings.terminal, &settings.work_dir, &settings.command, &settings.inputs, settings.result, true) {
        Ok(()) => {
            if Path::new(&settings.chain_settings).exists() {
                let chain_settings = Settings::new(&settings.chain_settings)?;
                return exec_command(&chain_settings);
            }
        }, 
        Err(e) => {
            return _exec_command(&settings.terminal, &settings.work_dir, &settings.failed_command, &Vec::new(), 0, false);
        }
    }

    Ok(())
}

fn _exec_command(terminal: &str, work_dir: &str, command: &str, inputs: &Vec<String>, result: i32, is_check_result: bool) -> Result<(), failure::Error> {
    let mut process;

    //入力が指定されていれば入力
    if inputs.len() > 0 {
        process = Command::new(terminal).current_dir(work_dir).arg(command).stdin(Stdio::piped()).spawn()?;
        match process.stdin.as_mut() {
            Some(console) => {
                console.write_all((inputs.join("\n") + "\n").as_bytes())?;
            }
            None => {
                return Err(failure::err_msg("mut console get failed."));
            },
        }
    } else {
        process = Command::new(terminal).current_dir(work_dir).arg(command).spawn()?;
    }

    if is_check_result && result != process.wait()?.code().unwrap_or(result + 1) {
		return Err(failure::err_msg("execute failed."));
    }

    Ok(())
}