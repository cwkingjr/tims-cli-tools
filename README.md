# TIMS CLI Tools

Home for some command line interface tools I'm building to help some folks streamline some repetitive adminstrative tasks.

## Using the Windows PowerShell Terminal

Open the terminal.

<p align="center"><img src="images/windows-terminal-launch.png" width="300" /></p>

Exit the terminal. Type "exit" and hit return.

<p align="center"><img src="images/windows-terminal-exit.png" width="400" /></p>

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

If you are not very good at moving around the terminal yet, get your self an intro over at https://github.com/cwkingjr/unix-command-intro-for-windows-folks or just grab the path to the file you want to process via the Windows File Explorer and paste it in after the program command and one space on the command line.

Grabbing the path via the Windows File Explorer:

<p align="center"><img src="images/windows-file-explorer-copy-as-path.png" width="400" /></p>
