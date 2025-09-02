## TIMS Payroll

### Description

This tool accepts a file path to an input data spreadsheet as it's command line argument and generates a consolidated payroll spreadsheet along with individual payee spreadsheets for each crew member found in the input spreadsheet. It drops these generated spreadsheets into the user's Document folder.

The tool also requires a configuration file that includes information about all the crew leads, crew seconds, pay rates, and additional pay rates. The data from this config file is used by the application to do all the pay calculations and determine how many spreadsheets are created.

### Set Up a Configuration File

This tool requires a configuration file in a hidden directory so it can read that file to discover the crew and pay rate data.

Either grab the `tims_payroll_example.toml` file from this repo or create one exactly like it from scratch with Notepad. The production configuration file must be names `tims_payroll.toml`.

The file contents need to be exactly the same as the example in this repo, but with the data changed to accurately reflect pay rates and crews.

This file must be in your home folder, under some additional folders, like this: `/Users/<your-user-name>/.config/tims_tools/tims_payroll.toml`. That `.config` directory starts with a dot on purpose as thats a hidden folder (typically).

On Windows it's something like this: `%HOMEDRIVE%%HOMEPATH%\.config\tims_tools\tims_payroll.toml`.

We're using this system of folders because that is convention for command line tool configs. That way, other tools can put their configs in `.config/` under a folder named for their tool, and can put whatever files they need under their folder.

If you are interested in using Git Bash, you can go into that terminal and run this command: `mkdir -p ~/.config/tims_tools/` to make those folders all at one time. Then place your modified `tims_payroll.toml` file into that tims_tools directory/folder.

### Invoke TIMS Payroll

To run the tool, go to the Git Bash Terminal and run (`<something>` inside angle brackets indicates this is something your are supposed to replace, replacing angles and all; meaning, leave out the angles.):

```bash
# Mac/Linux
tims_payroll -i <path-to-input-spreadsheet>
tims_payroll --input-path <path-to-input-spreadsheet>
tims_payroll --help

# Windows
tims_payroll.exe -i <path-to-input-spreadsheet>
tims_payroll.exe --input-path <path-to-input-spreadsheet>
tims_payroll.exe --help
```

If you want to set up a Windows batch file so you can drop a path onto an icon using Windows File Explorer, you can copy the `tims_payroll.bat` file in this repo to your desktop.
