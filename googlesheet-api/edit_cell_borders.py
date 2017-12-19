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
            'updateBorders': {
                'range': my_range,
                'top': {
                    'style': 'SOLID',
                    'width': 1,
                    'color': {
                        'blue': 1.0
                    },
                },
                'bottom': {
                    'style': 'SOLID',
                    'width': 1,
                    'color': {
                        'blue': 1.0
                    },
                },
                'left': {
                    'style': 'SOLID',
                    'width': 1,
                    'color': {
                        'blue': 1.0
                    },
                },
                'right': {
                    'style': 'SOLID',
                    'width': 1,
                    'color': {
                        'blue': 1.0
                    },
                },
                'innerHorizontal': {
                    'style': 'SOLID',
                    'width': 1,
                    'color': {
                        'blue': 1.0
                    },
                },
                'innerVertical': {
                    'style': 'SOLID',
                    'width': 1,
                    'color': {
                        'blue': 1.0
                    },
                },
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
