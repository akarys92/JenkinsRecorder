from dataCollector import DataCollector
from xmlParser import XmlParser
from csvHandler import CsvHandler
from tableHandler import TableHandler
from logger import Logger
import json


class Main:

    def __init__(self, config):
        config = self.getConfig(config)

        self.params = config['Jenkins']['Params']

        self.logger = Logger(config['Logs']['relative_path'])
        self.dc = DataCollector(config['Jenkins']['Account'], config['Jenkins']['Key'], config['Jenkins']['base_url'])
        tree = self.dc.getFullTree()
        x = XmlParser(tree, self.params)
        self.csvHandler = CsvHandler('jenkinsdata.csv')
        self.tableHandler = TableHandler(config['TableStore']['Storage_Account'], config['TableStore']['Account_Key'], self.params, config['TableStore']['Table_Name'])
        self.data = x.getAllObjects()

    def getConfig(self, path):
        json_file = open(path)
        json_str = json_file.read()
        json_data = json.loads(json_str)
        return json_data

    def printData(self):
        self.tableHandler.addEntries(self.data)

    def updateData(self):
        self.logger.logRun()
        # get highest build number in table
        try:
            num_in_table = int(self.tableHandler.getHighestBuild())
        except IndexError:
            num_in_table = 0

        # get highest build number in Jenkins
        num_in_jenkins = self.dc.getLatestNum()
        if num_in_table != num_in_jenkins:
            # num_in_jenkins - num_in_table = num_2_get
            num_2_get = num_in_jenkins - num_in_table
            self.logger.logSuccess("Getting " + str(num_2_get) + "entries from Jenkins")
            # prarm is {0,num_2_get}
            tree = self.dc.getBuildsByNum(0, num_2_get)
            x = XmlParser(tree, self.params)
            self.data = x.getAllObjects()
            self.printData()
            self.logger.logSuccess("Update succeeded")
        else:
            self.logger.logSuccess("No entires to update.")
