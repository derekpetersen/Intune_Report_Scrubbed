

![Fusable Logo](/Logos/Fusable_ElectricGreen_Horizontal_300px.png)

# Intune Reporting

---
## Scope

In this suite, you'll discover a range of carefully crafted scripts designed for efficient data collection and 
manipulation for Intune data. These scripts enhance the precision of the data retrieval process, 
focusing on generating detailed Intune reports. Whether streamlining data collection or refining manipulation techniques, 
this suite serves as a valuable toolkit for optimizing reporting capabilities in the Intune environment.



## Requirements
- Python 3.11
- Pandas library
- Beautiful Soup 4 Library

## Usage

### Find Devices Not In Intune

Running the `ui_visuals.py` file in the UI package will launch the Tkinter GUI, and start the application. 
This application take filepaths as the input, and can be gathered manually by typing in the filepath, or by using the 
browse button next to the text box. The `data_processing.py` file in the Data Processing package performs the data 
cleaning and analysis, then returns it to the UI to be displayed to the user.

### Find Users With A Device In Intune, But No License

This is solely handled by the `user_intune_license.py` file. To use, place your `Intune.csv` and 
`Intune_exportUsers_*DATE*.csv` into the `.csv` folder.

> **Note**: the `Intune_exportUsers_*DATE*.csv`, will need to reflect the correct date in both the .csv and the script. For 
> example, if your file is: `Intune_exportUsers_2024-1-29.csv` then this will need to be hard coded into the script in 
> the `intune_user_df` variable.

Once the correct `.csv` are in place, run the script, and it will return the users that have a device enrolled in Intune,
but do not have the appropriate licensing.

### Get User's Current Windows Version
This script, `windows_version_checks.py`, takes `Intune.csv` (devices in Intune), `windows_10_versions.csv`, and 
`windows_11_versions.csv` as inputs, and outputs `active_users_windows_version.csv`. The data processing in this script
takes all computer in Intune, and matches them with the release date, KB, and version of windows that machine is 
currently on

### Update Windows Version CSV Files
In the Data Scraping package, there is a file called `windows_versions.py`. This script scrapes the Microsoft current 
version page, collects the versions into a single dataframe, and exports them into their corresponding `.csv` file 
 (for example, `windows_10_versions.csv`). 



## Internal Python Packages
### Data Scraping
As suggested, the Data Scraping folder contains  scripts to scrape necessary data for the reports.

### Data Processing
This package undertakes the key task of loading, manipulating, and returning data necessary for the reports

### UI
The UI package contains the Tkinter app which presents the user facing GUI