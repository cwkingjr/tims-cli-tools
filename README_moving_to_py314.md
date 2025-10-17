## Moving to Python version 3.14

Prior to 2025-10-16, these tools ran on Python v3.13, but were updated to Python v3.14 on 2025-10-16.

Therefore, since Windows folks likely don't have the newer Python version installed, some steps are needed to upgrade the tools to the latest version.

To update/upgrade, make these changes on your Windows system using the Git Bash terminal.

```bash
uv self update
uv tool uninstall tims-cli-tools
uv python install 3.14
```

This next step will install the updated tims-cli-tools. Since uv will need to recompile all the dependencies to work with Python v3.14 (only required during install), this will take a good long while. You will likely think something is broken and will be tempted to cancel/quit. Don't do it. Just let it run and it will eventually complete.

```bash
uv tool install https://github.com/cwkingjr/tims-cli-tools.git
```

When the above completes, it will install the tims\_\* tools onto your system and you'll be able to use them as you did previously. No functionality of tools was changed during this upgrade. The upgrade is purely to move us to the most current (and a bit faster) version of Python and to update all the dependencies to the latest versions. We do this to get all the latest bug fixes and to make sure we don't get too far behind the current versions of tools.

## New version

Also note that the fist time you run Python against a new version of tools, Python has to parse all the tool files (that I wrote) and create compiled versions. This can take a minute/so, but only has to be done once per changed file. So, the next time your run the tool, it'll just read the already compiled files.

To see this, once you install the new tools, just run the help on a tool and that will cause Python to perform this compile.

For example:

```bash
tims_payroll --help
```

That will take a minute, but if you run it again a second time, right after the first run finishes, it'll be faster.
