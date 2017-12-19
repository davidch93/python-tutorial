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

    spreadsheet_id = '13GwLnie990w-mkR4d8x0yeFvCa-o1Tp7Ro8gE4Ag-d0'
    my_range = {
        'sheetId': 0,
        'startRowIndex': 1,
        'endRowIndex': 10,
        'startColumnIndex': 0,
        'endColumnIndex': 4,
    }
    requests = [
        {
            'repeatCell': {
                'range': my_range,
                'cell': {
                    'userEnteredFormat': {
                        'numberFormat': {
                            'type': 'DATE',
                            'pattern': 'yyyy-mm-dd hh:mm:ss'
                        }
                    }
                },
                'fields': 'userEnteredFormat.numberFormat'
            }
        }
    ]
    body = {
        'requests': requests
    }

    result = service.spreadsheets() \
        .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
    print('{0} cells updated.'.format(len(result.get('replies'))))


if __name__ == '__main__':
    main()
