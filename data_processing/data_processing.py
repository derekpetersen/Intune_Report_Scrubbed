import pandas as pd

# Use for running this file
# import computer_name_patterns

# Use for running UI
from data_processing import computer_name_patterns


def intune_data_cleaning(intune_raw):
    """
    For the Intune CSV. Cleans up unneeded rows from the CSV. Also removes all but the Asset Tag number from the
    device name.
    :return:
    """
    intune_df = pd.read_csv(intune_raw)

    remove_columns = ['Device ID', 'Managed by', 'OS', 'Last check-in', 'Ownership', 'Compliance', 'OS version']
    intune_df.drop(remove_columns, inplace=True, axis=1)

    for device in computer_name_patterns.data:
        intune_df['Device name'] = intune_df['Device name'].str.replace(device, "", regex=True)

    intune_df['Device name'] = intune_df['Device name'].str.upper()
    return intune_df


def sd_data_cleaning(sd_raw):
    """
      For the SD CSV. Cleans up unneeded rows from the CSV. Also removes all but the Asset Tag number from the
      device name.
      :return:
      """
    sd_df = pd.read_csv(sd_raw)

    remove_columns = ['OS', 'Org Serial Number', 'Asset State', ]
    sd_df.drop(remove_columns, inplace=True, axis=1)

    for device in computer_name_patterns.data:
        sd_df['Machine Name'] = sd_df['Machine Name'].str.replace(device, "", regex=True)

    sd_df['Machine Name'] = sd_df['Machine Name'].str.upper()
    return sd_df


def filter_disabled_accounts(not_in_intune_csv):
    """
    NOT CURRENTLY USED

    Takes the "Disabled Users" report from AD Manager, and then compares it to the Not in Intune report.

    :param not_in_intune_csv: Processed data of devices not in Intune
    :return:
    """
    disabled_accounts = pd.read_csv("../csv/raw_data/disabled_users.csv")
    merge = pd.merge(not_in_intune_csv, disabled_accounts, how='left', left_on='User', right_on='Display Name',
                     indicator=True)
    filtered = merge[merge['_merge'] == 'left_only']
    print(filtered)


def check_devices_not_in_intune(intune_df, sd_df):
    """
    Compares the SD and Intune CSVs and returns the devices not in Intune.
    :return:
    """
    # Creates merge/join of the two reports and matches them
    compare_devices = pd.merge(sd_df, intune_df, how='left', left_on='Machine Name', right_on='Device name',
                               indicator=True)
    compare_devices = compare_devices[compare_devices['User'] != "Not Assigned"]
    devices_not_in_intune = compare_devices[compare_devices['_merge'] == 'left_only']

    # Makes new DataFrame with the data from the above merge
    results = pd.DataFrame(devices_not_in_intune)
    unneeded_columns = ['Device name', 'Primary user UPN', '_merge']
    results.drop(unneeded_columns, inplace=True, axis=1)
    results.to_csv('../csv/outputs/devices_not_in_intune.csv')
    return results


# Makes sure the terminal output shows all columns and rows
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Runs the CSV data cleaning operation

if __name__ == "__main__":

    intune_dataframe = intune_data_cleaning('../csv/Intune.csv')
    sd_dataframe = sd_data_cleaning('../csv/SD.csv')

    not_in_intune = check_devices_not_in_intune(intune_dataframe, sd_dataframe)
    print(not_in_intune)

# ~~~~ Testing ~~~
# print(intune_df['Device name'])
# print(sd_df['Machine Name'])
# print(intune_df['Device name'])
