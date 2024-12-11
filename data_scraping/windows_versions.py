import pandas as pd

w11_url = "https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information"
w10_url = "https://learn.microsoft.com/en-us/windows/release-health/release-information"

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def insert_columns(df, df_number, version, windows):
    """
    This insert 2 new columns in the DataFrame that specify versioning info for Windows.
    :param df: DataFrame
    :param df_number: Index of Dataframe (sub-DataFrame)
    :param version: Sub-Version (ie 22H2)
    :param windows: Windows main version (ie Windows 10)
    :return:
    """
    df[df_number].insert(4, 'Version', version, True)
    df[df_number].insert(5, 'Windows', windows, True)


def add_version_prefix(df):
    """
    Adds the '10.0.' prefix to all the entries in the Data Frame. This is to create consistency with reports from other
    platforms
    :param df: DataFrame
    :return:
    """
    df['Build'] = df['Build'].apply(lambda x: '10.0.' + str(x))


def check_fix_length(df):
    """
    Some Trailing Zeros have been dropped during processing. This function checks the length and adds trailing zeros
    accordingly.
    :param df: DataFrame
    :return:
    """
    for index, build in enumerate(df['Build']):
        while len(build) < 15:
            build += '0'
            df.at[index, 'Build'] = build


def process_w11():
    """
    Takes the Windows 11 version URL, scrapes the data, transforms it, then  outputs it to a .csv
    :return:
    """
    w11_data = pd.read_html(w11_url)

    insert_columns(w11_data, 1, '23H2', '11')
    insert_columns(w11_data, 2, '22H2', '11')
    insert_columns(w11_data, 3, '21H2', '11')

    all_w11_versions = [w11_data[1], w11_data[2], w11_data[3]]

    all_w11 = pd.DataFrame(pd.concat(all_w11_versions))

    add_version_prefix(all_w11)

    all_w11.reset_index(drop=True, inplace=True)

    check_fix_length(all_w11)
    all_w11.to_csv('../csv/outputs/windows_11_versions.csv')


def process_w10():
    """
    Takes the Windows 10 version URL, scrapes the data, transforms it, then  outputs it to a .csv
    :return:
    """
    w10_data = pd.read_html(w10_url)

    insert_columns(w10_data, 2, '22H2', '10')
    insert_columns(w10_data, 3, '21H2', '10')

    all_w10_versions = [w10_data[2], w10_data[3]]
    all_w10 = pd.DataFrame(pd.concat(all_w10_versions))

    add_version_prefix(all_w10)

    all_w10.reset_index(drop=True, inplace=True)

    check_fix_length(all_w10)

    all_w10.to_csv('../csv/outputs/windows_10_versions.csv')


process_w10()
process_w11()
