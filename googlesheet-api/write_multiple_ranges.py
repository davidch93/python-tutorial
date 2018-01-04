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
    range_name = 'Sheet1!A47:C49'

    values = [
        ['A1', 'B1', 'C1'],
        ['A2', 'B2', 'C2'],
        ['A3', 'B3', 'C3']
    ]
    data = [
        {
            'range': range_name,
            'values': values
        }
        # Additional ranges to update
    ]

    value_input_option = 'USER_ENTERED'
    body = {
        'valueInputOption': value_input_option,
        'data': data
    }

    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id, body=body).execute()
    print('Total {0} cells updated.'.format(result.get('totalUpdatedCells')))


if __name__ == '__main__':
    main()
