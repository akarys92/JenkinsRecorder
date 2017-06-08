import csv


class CsvHandler:

    def __init__(self, file_name):
        self.file_name = file_name
        self.fieldnames = ['Status', 'Url', 'Timestamp',
                           'BuildNumber', 'Job', 'Duration', 'BranchName']

    def writeObject(self, object):
        with open(self.file_name, 'wb') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerow(object)

    def writeObjects(self, objects):
        with open(self.file_name, 'wb') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            for object in objects:
                writer.writerow(object)

    def addObjects(self, objects):
        with open(self.file_name, 'ab') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            for object in objects:
                writer.writerow(object)

    def getHighestBuild(self):
        high = 0
        with open(self.file_name, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                num = int(row[4])
                if num > high:
                    high = num
            return high
