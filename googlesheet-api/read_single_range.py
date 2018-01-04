import googlesheet_credentials
import httplib2
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

    spreadsheet_id = '1wUkMMADvniH31gFWHYVCr397ZkZobvyxd1pXbksIe1s'
    range_name = 'Sheet1!A4:E14'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values')

    if not values:
        print('No data found.')
    else:
        for row in values:
            # Print columns A, B, C
            print('{0}, {1}, {2}'.format(row[0], row[1], row[2]))


if __name__ == '__main__':
    main()
