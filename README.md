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
