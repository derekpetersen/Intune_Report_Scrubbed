import pandas as pd

# Makes sure the terminal output shows all columns and rows
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

windows10 = pd.read_csv("../csv/outputs/windows_10_versions.csv")
windows11 = pd.read_csv("../csv/outputs/windows_11_versions.csv")
intune = pd.read_csv("../csv/raw_data/Intune.csv")


def version_check(v10, v11, intune_df):
    windows_versions = [v10, v11]
    all_windows_versions = pd.concat(windows_versions)
    merge = pd.merge(intune_df, all_windows_versions, how="left", left_on="OS version", right_on="Build")
    version_match = pd.DataFrame(merge)
    version_match = version_match.astype({'Windows': 'object'})
    return version_match


matched = version_check(windows10, windows11, intune)

matched.to_csv(path_or_buf="../csv/outputs/active_users_windows_version.csv")
