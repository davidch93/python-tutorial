from pyhive import presto

configPr = {
    'host': 'localhost',
    'port': '8080'
}

def main():
    cursor = presto.connect(**configPr).cursor()
    cursor.execute('show tables')
    for row in cursor.fetchall():
        print(row[0])
    cursor.close()

if __name__ == '__main__':
    main()