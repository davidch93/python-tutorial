from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery


json_key_file_name = '{0}'.format('key-file.json')


class API:
    def __init__(self, credentials):
        self._credentials = credentials

    def build(self, service, version):
        return discovery.build(service, version, credentials=self._credentials)

    def get_api_kwargs(self):
        return {'credentials': self._credentials}


class Spreadsheet(API):
    def __init__(self, info, **kwargs):
        self._info = info
        super().__init__(**kwargs)

    @property
    def id(self):
        return self._info['spreadsheetId']

    @property
    def permissions(self):
        permissions = self._get_permissions()
        anyone = None
        writers = []
        readers = []
        for permission in permissions:
            # 'user', 'anyone', 'group', 'domain'
            permission_type = permission['type']
            # 'owner', 'commenter', 'reader', 'writer'
            permission_role = permission['role']
            if permission_type == 'anyone':
                if permission_role in ['owner', 'writer']:
                    anyone = 'write'
                elif permission_role in ['reader']:
                    anyone = 'read'
                elif permission_role in ['commenter']:
                    anyone = 'comment'
            elif permission_type == 'user':
                permission = self._get_permission(permission['id'])
                if permission_role in ['owner', 'writer']:
                    lst = writers
                elif permission_role in ['reader', 'commenter']:
                    lst = readers
                else:
                    raise RuntimeError('Protocol role unknown!')
                lst.append(permission['emailAddress'])
        return {
            'anyone': anyone,
            'writers': writers,
            'readers': readers,
        }

    def set_permissions(self, anyone=None, writers=None, readers=None):
        assert anyone in [None, 'writer', 'write',
                          'reader', 'read', 'w', 'r'], 'not in ["r", "w"]'

        drive = self.build('drive', 'v3')
        if anyone:
            role = {
                'r': 'reader',
                'read': 'reader',
                'reader': 'reader',
                'w': 'writer',
                'write': 'writer',
                'writer': 'writer',
            }
            body = {
                'role': role[anyone],
                'type': 'anyone',
            }
            drive.permissions().create(fileId=self.id, body=body).execute()
        if writers:
            body = {
                'role': 'writer',
                'type': 'user',
                'emailAddress': writers,
            }
            drive.permissions().create(fileId=self.id, body=body).execute()
        if readers:
            body = {
                'role': 'reader',
                'type': 'user',
                'emailAddress': readers,
            }
            drive.permissions().create(fileId=self.id, body=body).execute()

    def _get_permissions(self):
        drive = self.build('drive', 'v3')
        r = drive.permissions().list(fileId=self.id).execute()
        permissions = r.get('permissions', [])
        return permissions

    def _get_permission(self, permission_id):
        drive = self.build('drive', 'v3')
        fields = 'allowFileDiscovery,displayName,domain,emailAddress,' \
                 'expirationTime,id,kind,photoLink,role,type'
        permission = drive.permissions().get(
            fileId=self.id, permissionId=permission_id, fields=fields)
        return permission.execute()

    def __str__(self):
        return "Sheet(%s)" % self.id


class SpreadsheetService(API):
    def create(self, title, anyone=None, writers=None, readers=None):
        assert anyone in [None, 'write', 'read', 'comment', 'w', 'r', 'c'], \
            'not in ["r", "w", "c"]'
        sheets = self.build('sheets', 'v4')
        body = {'properties': {'title': title}}
        result = sheets.spreadsheets().create(body=body).execute()
        spreadsheet = Spreadsheet(result, **self.get_api_kwargs())
        spreadsheet.set_permissions(anyone=anyone, writers=writers,
                                    readers=readers)
        return spreadsheet.id

    def write(self, spreadsheet_id, range_name, body):
        sheets = self.build('sheets', 'v4')
        result = sheets.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))


def get_credentials(scopes: list) -> ServiceAccountCredentials:
    credential = ServiceAccountCredentials.from_json_keyfile_name(json_key_file_name, scopes)
    return credential


def create_example():
    credentials = get_credentials([
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/spreadsheets'])
    api = SpreadsheetService(credentials=credentials)
    return api.create('test1', writers=['david.christianto@mail.com'])


def write_data_example(spreadsheet_id):
    credentials = get_credentials([
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/spreadsheets'])
    api = SpreadsheetService(credentials=credentials)
    range_name = 'Sheet1!A1:C3'
    body = {
        'values': [
            ['A1', 'B1', 'C1'],
            ['A2', 'B2', 'C2'],
            ['A3', 'B3', 'C3']
        ]
    }
    api.write(spreadsheet_id, range_name, body)


if __name__ == '__main__':
    spreadsheet_id = create_example()
    write_data_example(spreadsheet_id)
