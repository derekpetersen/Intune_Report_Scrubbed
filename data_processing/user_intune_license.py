import pandas as pd

intune_machine_df = pd.read_csv('../csv/raw_data/Intune.csv')
intune_user_df = pd.read_csv("../csv/raw_data/Intune_exportUsers_2024-1-29.csv")

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def find_users_without_license():
    merged = pd.merge(intune_machine_df, intune_user_df, how='left', left_on='Primary user UPN',
                      right_on='userPrincipalName', indicator=True)
    no_intune_license = merged[merged['_merge'] == 'left_only']
    no_intune_license = pd.DataFrame(no_intune_license)

    remove_columns = ['Device ID', 'Managed by', 'Ownership', 'Compliance', 'OS', 'OS version', 'Last check-in',
                      'surname', 'mail', 'givenName', 'id', 'userType', 'jobTitle', 'department', 'usageLocation',
                      'streetAddress', 'state', 'country', 'city', 'postalCode', 'telephoneNumber', 'mobilePhone',
                      'alternateEmailAddress', 'ageGroup', 'consentProvidedForMinor', 'legalAgeGroupClassification',
                      'companyName', 'creationType', 'directorySynced', 'invitationState', 'identityIssuer',
                      'createdDateTime', 'userPrincipalName', 'displayName', 'accountEnabled', 'officeLocation',
                      '_merge']

    no_intune_license.drop(remove_columns, inplace=True, axis=1)
    result = pd.DataFrame(no_intune_license)
    result.to_csv('../csv/outputs/no_intune_license.csv')


find_users_without_license()
