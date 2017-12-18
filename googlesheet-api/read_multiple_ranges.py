import httplib2
import googlesheet_credentials

from apiclient import discovery


def main():
    """Shows basic usage of the Sheets API.
    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/${spreadsheet_id}/edit
    """
    credentials = googlesheet_credentials.get_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = 'https://sheets.googleapis.com/$discovery/rest?' \
                    'version=v4'
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discovery_url)

    spreadsheet_id = "1wUkMMADvniH31gFWHYVCr397ZkZobvyxd1pXbksIe1s"
    range_name = ['Sheet1!A4:C18', 'Sheet1!A20:C45']
    result = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheet_id, ranges=range_name).execute()
    value_ranges = result.get('valueRanges')

    if not value_ranges:
        print('No data found.')
    else:
        for valueRange in value_ranges:
            print('-----Value Range: {0}'.format(valueRange))
            for row in valueRange['values']:
                print('{0}, {1}'.format(row[0], row[1]))


if __name__ == '__main__':
    main()
