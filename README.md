# TIMS CLI Tools

Home for some custom command line interface (CLI) tools I'm building to help some folks streamline some repetitive adminstrative tasks.

## Using the Windows PowerShell Terminal

Open the terminal by right-clicking on the Windows Start icon and choosing Terminal.

<p align="center"><img src="images/windows-terminal-launch.png" width="150" /></p>

Exit the terminal. Type "exit" and hit return.

<p align="center"><img src="images/windows-terminal-exit.png" width="400" /></p>

## Install Git Bash and UV and Verify Installations

You'll need git and uv installed on your computer. To get those, head over to https://github.com/cwkingjr/windows-install-gitbash-and-uv and install Git Bash and UV, then complete the verification steps there.

## Update UV

Update `uv` pretty often as it's under continous improvement development.

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

Or, you can just upgrade all the tools managed by uv at once:

```bash
# to see all the tools you have installed that are managed by uv
uv tool list

# to upgrade all the installed tools
uv tool upgrade --all
```

### Uninstall TIMS CLI Tools

```bash
uv tool uninstall tims-cli-tools
```

# Applications Included

## TIMS Invoice

See `README_tims_invoice.md` in this repo for information on setup and use. The application will be installed, updated, and removed as part of tims_cli_tools.

## TIMS Payroll

See `README_tims_payroll.md` in this repo for information on setup and use. The application will be installed, updated, and removed as part of tims_cli_tools.

# Extras

## Moving Around in the Git Bash Terminal

If you are not very good at moving around the terminal yet, get yourself an intro over at https://github.com/cwkingjr/unix-command-intro-for-windows-folks or just grab the path to the file you want to process via the Windows File Explorer and paste it in after the program command and one space on the command line.

Grabbing the path via the Windows File Explorer:

<p align="center"><img src="images/windows-file-explorer-copy-as-path.png" width="400" /></p>

## Using a Windows BAT File

If you would like to use a Windows Batch file to allow file drag and drop from the Windows Explorer to a batch file, have a look over at `https://github.com/cwkingjr/windows-drag-to-app-with-args` to see how to set up a batch file.
