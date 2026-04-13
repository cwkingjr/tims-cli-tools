## TIMS Invoice

The tims_invoice tool reads a spreadsheet extracted from the master tracing spreadsheet, grabs the columns it needs, and generates an output spreadsheet with the data transformed into the format required for pasting into a specific third party's invoice submission spreadsheet.

Invoke the tool with the `-i` flag and pass the path to the extract spreadsheet. You'll love your life more if you don't put spaces in your file names.

```bash
tims_invoice -i <your_file_path.xlsx>
```

Or using the long form:

```bash
tims_invoice --input-path <your_file_path.xlsx>
```

Example:

```bash
tims_invoice -i Z:/invoice.xlsx
```

If you want to set up a Windows batch file so you can drop a path onto an icon using Windows File Explorer, you can copy the `tims_invoice.bat` file in this repo to your desktop.
