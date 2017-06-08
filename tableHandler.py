from azure.storage.table import TableService, Entity
import datetime

class TableHandler:
    def __init__(self, account, key, params, table=""):
        self.table_service = TableService(account_name=account, account_key=key)
        self.table = table
        self.PartitionKey = 'jenkinsdata3'
        self.params = params

    def addTable(self, name):
        if self.table_service.create_table(name):
            self.table = name
            return True
        return False

    def addEntry(self, objects):
        print objects
        jobnumber = objects['Job']
        try:
            date = datetime.datetime.fromtimestamp(float(objects['Timestamp'])/1000).strftime('%Y-%m-%d %H:%M:%S')
        except:
            date = "N/A"
        #this will break at >100,000 jobs...
        key = str(float(1)/ float(jobnumber))
        entry = {
            'PartitionKey': self.PartitionKey,
            'DateStarted': date,
            'RowKey': key,
            'JobNumber': objects['Job'],
            'Status': objects['Status'],
            'url': objects['Url'],
            'duration': objects['Duration'],
            #'branch': objects['BranchName'],
            #'buildnumber': objects['BuildNumber']
            }
        for param in self.params:
            #print "Objects are"
            #print objects
            try:
                entry[param] = objects[param]
            except:
                print "Failed to find param " + str(param) + " for entry: " + str(entry)

        try:
            self.table_service.insert_entity(self.table, entry)
        except:
            print "Failed for "
            print(entry)

    def addEntries(self, entries):
        for entry in entries:
            self.addEntry(entry)

    def getHighestBuild(self):
        entry = self.table_service.query_entities(self.table, filter="PartitionKey eq '" + self.PartitionKey + "'", top='1')
        return entry[0].JobNumber



'''
Test Data:
entry = {'Timestamp': '1907983', 'Job': '12', 'Status': 'SUCCESS', 'Url': 'https://azjenkinscore.corp.microsoft.com:8080/job/engsys/job/devservices/job/engpipe/job/workflows/job/cloudvault/job/launchdownloadbuilds/130/', 'duration': '1466040000000', 'BranchName':'rd_store_stable', 'RowKey': '130', 'Duration': '1466040000000', 'BuildNumber': '49.2.6898.226.amd64fre.rd_store_stable.160612-2224'}

entry = {'PartitionKey':'jenkinsdata', 'Timestamp': '1907983', 'Job': '1', 'Status': 'SUCCESS', 'Url': 'https://azjenkinscore.corp.microsoft.com:8080/job/engsys/job/devservices/job/engpipe/job/workflows/job/cloudvault/job/launchdownloadbuilds/130/', 'duration': '1466040000000', 'BranchName':'rd_store_stable', 'RowKey': '.130', 'Duration': '1466040000000', 'BuildNumber': '49.2.6898.226.amd64fre.rd_store_stable.160612-2224'}
'''
