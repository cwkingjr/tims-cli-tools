# TIMS CLI Tools

Home for some command line interface tools I'm building to help some folks streamline some repetitive adminstrative tasks.

## Using the Windows PowerShell Terminal

Open the terminal.

<p align="center"><img src="images/windows-terminal-launch.png" width="300" /></p>

Exit the terminal. Type "exit" and hit return.

<p align="center"><img src="images/windows-terminal-exit.png" width="400" /></p>

## Install uv

You will need the UV Python package manager tool (https://github.com/astral-sh/uv) installed on your computer to install, update, and run the tools in this collection. You install uv using the PowerShell Terminal on Windows. Open the terminal and run the two commands below.

Run this command to install uv:

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Run the below command to verify that uv is installed on your system. It just calls uv with the version argument, which simply causes uv to start, print out the installed verion, and quit. If it prints something like "uv 0.8.4" then you are good to go.

```
uv --version
```

## TIMS Invoice Transformer

The tims_invoice_transformer tool reads a spreadsheet extracted from the master tracing spreadsheet, grabs the columns it needs, and generates an output spreadsheet with the data transformed and formatted in a way that is required for pasting into a specific third party's invoice submission spreadsheet.

### Installation

Using the PowerShell or Git Bash Terminal run this command at the shell prompt:

```
uv tool install https://github.com/cwkingjr/tims-cli-tools.git
```

### Use

Invoke the tool and pass it the input (master extract) spreadsheet path as an argument. You'll love your life more if you don't put spaces in your file name.

```
tims_invoice_transformer Z:/invoice.xlsx
```
