#[macro_use]
extern crate log;
#[macro_use]
extern crate clap;

mod settings;

use std::{env, str, fs};
use clap::{App, Arg, ArgMatches, SubCommand};
use std::path::Path;


enum ReturnCode {
	Success, 
	Unknown, 
}

fn main() {
    
	env::set_var("RUST_LOG", "debug");
	env_logger::init();

	//コマンドライン引数をパース
    let app = App::new(crate_name!())
        .version(crate_version!())
        .author(crate_authors!())
		.about(crate_description!())
        .subcommand(SubCommand::with_name("new")
            .about("generate template settings.")
            .arg(Arg::with_name("settings")
                .help("settings name.")
				.required(true)
            )
            .arg(Arg::with_name("dir")
				.help("working directory.")
				.short("d")
				.long("dir")
				.takes_value(true)
            )
		)
        .subcommand(SubCommand::with_name("exec")
            .about("auto execute cui tools.")
            .arg(Arg::with_name("settings")
                .help("settings name.")
				.required(true)
            )
            .arg(Arg::with_name("dir")
				.help("working directory.")
				.short("d")
				.long("dir")
				.takes_value(true)
            )
		);
	let matches = app.get_matches();

	//exeのディレクトリ
	//let current_dir: String = format!("{}", env::current_exe().unwrap().parent().unwrap().display());

    let mut is_success = false;
    
	if let Some(sub_matches) = matches.subcommand_matches("new") {
		let mut dir = ".";
		if let Some(value) = sub_matches.value_of("dir") {
			dir = value.trim_end_matches('/').trim_end_matches('\\');
		}
		if let Some(name) = sub_matches.value_of("settings") {
            new(dir, name).unwrap_or_else(|e|{
                error!("[new] command failed: {}", e);
            });
            is_success = true;
		}
    }
	if let Some(sub_matches) = matches.subcommand_matches("exec") {
		let mut dir = ".";
		if let Some(value) = sub_matches.value_of("dir") {
			dir = value.trim_end_matches('/').trim_end_matches('\\');
		}
		if let Some(name) = sub_matches.value_of("settings") {
            exec(dir, name).unwrap_or_else(|e|{
                error!("[exec] command failed: {}", e);
            });
            is_success = true;
		}
    }

    if is_success {
        info!("successful");
        std::process::exit(ReturnCode::Success as i32);
    } else {
        error!("unknown failed");
        std::process::exit(ReturnCode::Unknown as i32);
    }
}


fn new(dir: &str, name: &str) -> Result<(), failure::Error> {
    let settings = settings::Settings::default();
    fs::create_dir_all(dir)?;
    settings::write_settings(&format!("{}/{}.toml", dir, name), &settings)
}

fn exec(dir: &str, name: &str) -> Result<(), failure::Error> {
    let settings = settings::Settings::new(&format!("{}/{}.toml", dir, name))?;
    settings::exec_command(&settings)
}
