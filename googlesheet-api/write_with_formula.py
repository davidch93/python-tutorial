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
    range_name = 'Sheet1!A47:D49'

    values = [
        ['A1', 100, 400, '=ABS(B47-C47)'],
        ['A2', 200, 100, '=ABS(B48-C48)'],
        ['A3', 300, 500, '=ABS(B49-C49)']
    ]
    value_input_option = 'USER_ENTERED'
    body = {
        'values': values
    }

    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


if __name__ == '__main__':
    main()
