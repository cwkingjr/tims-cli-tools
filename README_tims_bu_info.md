## TIMS BU Info

### Description

This tool accepts a BU number as it's command line argument, looks in the master tracker spreadsheet to find that BU, grabs some of the info from that row, and prints it into the terminal screen. The idea behind this tool is to allow you to very quickly grab address and lat/long for a BU instead of having to pull up the spreadsheet and find it yourself.

### Set Up a Configuration File

This tool requires a configuration file in a hidden directory so it can read that file to discover where the master tracker spreadsheet is located.

Either grab the `tims_bu_info.toml` file from this repo or create one exactly like it from scratch with Notepad.

The file contents need to be exactly the same as the example in this repo, but with the path in quotes changed to reflect where the production master tracker spreadsheet lives.

This file must be in your home folder, under some additional folders, like this: `/Users/<your-user-name>/.config/tims_tools/tims_bu_info.toml`. That `.config` directory starts with a dot on purpose as thats a hidden folder (typically).

On Windows it's something like this: `%HOMEDRIVE%%HOMEPATH%\.config\tims_tools\tims_bu_info.toml`.

We're using this system of folders because that is convention for command line tool configs. That way, other tools can put their configs in `.config/` under a folder named for their tool, and can put whatever files they need under their folder.

If you are interested in using Git Bash, you can go into that terminal and run this command: `mkdir -p ~/.config/tims_tools/` to make those folders all at one time. Then place your modified `tims_bu_info.toml` file into that tims_tools directory/folder.

### Invoke TIMS BU Info

To run the tool, go to the Git Bash Terminal and run (`<something>` inside angle brackets indicates this is something your are supposed to replace, replacing angles and all; meaning, leave out the angles.):

```bash
tims_bu_info <bu number>
tims_bu_info 4746458576
```

Example output:

<p align="center"><img src="images/bu_info_output.png" width="400" /></p>
