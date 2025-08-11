# TIMS CLI Tools

Home for some command line interface tools I'm building to help some folks streamline some repetitive adminstrative tasks.

## Using the Windows PowerShell Terminal

Open the terminal.

<p align="center"><img src="images/windows-terminal-launch.png" width="300" /></p>

Exit the terminal. Type "exit" and hit return.

<p align="center"><img src="images/windows-terminal-exit.png" width="400" /></p>

## Git Bash

You'll need git installed on your computer so we can download the program directly from GitHub versus me having to publish this package to the Python Package Index (PyPI). To get that done, we'll just choose the easiest way possible, and get an awesome Unix-y terminal with some cool/useful Unix commands in the process. That means you'll download and install Git Bash, running the installer and selecting all the default settings. Except, IF the choice to install a desktop icon isn't selected, select that during the install.

Get the Git Bash installer here: https://gitforwindows.org/.

Once Git Bash is installed, git will be installed and available, so if you don't want to learn some awesome Unix stuff, you can ignore it afterward.

## UV

### Install UV

You will need the UV Python package manager tool (https://github.com/astral-sh/uv) installed on your computer to install, update, and run the tools in this collection. You install uv using the PowerShell Terminal on Windows. Open the terminal and run the two commands below.

Run this command to install uv:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Run the below command to verify that uv is installed on your system. It just calls uv with the version argument, which simply causes uv to start, print out the installed verion, and quit. If it prints something like "uv 0.8.4" then you are good to go.

```bash
uv --version
```

### Update UV

```bash
uv self update
```

## TIMS CLI Tools

### Install TIMS CLI Tools

Using the PowerShell or Git Bash Terminal run this command at the shell prompt:

```bash
uv tool install https://github.com/cwkingjr/tims-cli-tools.git
```

Here's what the install looked like on my system:

<p align="center"><img src="images/uv-tool-install-from-github.png" width="400" /></p>

### Upgrade TIMS CLI Tools

This is typically only needed when the developer fixes bugs, adds features, or updates the program's dependencies. In any case, it doesn't hurt anything to run it just in case.

```bash
uv tool upgrade tims-cli-tools
```

### Uninstall TIMS CLI Tools

```bash
uv tool uninstall tims-cli-tools
```

## TIMS BU Info

### Description

This tool accepts a BU number as it's command line argument, looks in the master tracker spreadsheet to find that BU, grabs some of the info from that row, and prints it into the terminal screen. The idea behind this tool is to allow you to very quickly grab address and lat/long for a BU instead of having to pull up the spreadsheet and find it yourself.

### Set Up a Configuration File

This tool requires a configuration file in a hidden directory so it can read that file to discover where the master tracker spreadsheet is located.

Either grab the `tims_tools.toml` file from this repo or create one exactly like it from scratch with Notepad.

The file contents need to be exactly the same as the example in this repo, but with the path in quotes changed to reflect where the production master tracker spreadsheet lives.

This file must be in your home folder, under some additional folders, like this: `/Users/<your-user-name>/.config/tims_tools/tims_tools.toml`. That `.config` directory starts with a dot on purpose as thats a hidden folder (typically).

We're using this system of folders because that is convention for command line tool configs. That way, other tools can put their configs in `.config/` under a folder named for their tool, and can put whatever files they need under their folder.

If you are interested in using Git Bash, you can go into that terminal and run this command: `mkdir -p ~/.config/tims_tools/` to make those folders all at one time. Then place your modified tims_tools.toml file into that tims_tools directory/folder.

### Invoke TIMS BU Info

To run the tool, got to the Git Bash or PS Terminal and run (`<something>` inside angle brackets indicates this is something your are supposed to replace, replacing angles and all; meaning, leave out the angles.):

```bash
tims_bu_info <bu number>
tims_bu_info 4746458576
```

Example output:

<p align="center"><img src="images/bu_info_output.png" width="400" /></p>

## TIMS Invoice Transformer

The tims_invoice_transformer tool reads a spreadsheet extracted from the master tracing spreadsheet, grabs the columns it needs, and generates an output spreadsheet with the data transformed into the format required for pasting into a specific third party's invoice submission spreadsheet.

Invoke the tool and pass it the path as to the extract spreadsheet. You'll love your life more if you don't put spaces in your file names.

```bash
tims_invoice_transformer(.exe) <your_file_path.xlsx>
```

Unix/Linux Example:

```bash
tims_invoice_transformer Z:/invoice.xlsx
```

Windows Example:

```bash
tims_invoice_transformer.exe Z:/invoice.xlsx
```

If you are not very good at moving around the terminal yet, get yourself an intro over at https://github.com/cwkingjr/unix-command-intro-for-windows-folks or just grab the path to the file you want to process via the Windows File Explorer and paste it in after the program command and one space on the command line.

Grabbing the path via the Windows File Explorer:

<p align="center"><img src="images/windows-file-explorer-copy-as-path.png" width="400" /></p>

## Using a Windows BAT File

If you would like to use a Windows Batch file to allow file drag and drop from the Windows Explorer to a batch file, have a look over at `https://github.com/cwkingjr/windows-drag-to-app-with-args` to see how to set up a batch file.

Assuming `uv` installed this app on your system in the same general location as it did on mine, you can just copy the `invoice_transformer.bat` file in this repository onto your desktop and it should work. If using the one provided here doesn't work, you should be able to figure out the issue using that link provided just above.
