import csv


def read(filepath, delimiter, quotechar):
    with open(filepath, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=delimiter, quotechar=quotechar)
        for row in reader:
            print(', '.join(row))


def write(filepath, delimiter, quotechar, data):
    with open(filepath, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar)
        writer.writerows(data)


if __name__ == '__main__':
    filepath = 'dump.csv'
    delimiter = ','
    quotechar = '"'

    data = [[1, 'ok'], [2, 'yes']]
    write(filepath, delimiter, quotechar, data)

    read(filepath, delimiter, quotechar)
