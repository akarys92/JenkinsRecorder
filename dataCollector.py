from jenkinsAccess import JenkinsAccess
import xml.etree.ElementTree as ET


class DataCollector:

    def __init__(self, user, key, base_url):
        self.jenkins = JenkinsAccess(key, user, base_url)

    def getFullTree(self):
        data = self.jenkins.getJobsByOrder()
        return data

    def getBuilds(self):
        data = self.getFullTree()
        tree = ET.fromstring(data)
        builds = tree.findall('build')
        return builds

    def createBuildsNumsObj(self):
        builds = self.getBuilds()
        end = []
        for i in builds:
            end.append(i[0].text)
        return end

    def createBuildsObj(self):
        builds = self.createBuildsNumsObj()
        buildArr = []
        for i in builds:
            buildInfo = self.jenkins.getJobByNumber(i)
            buildArr.append(buildInfo)
        return buildArr

    def getBuildsByNum(self, start, end):
        return self.jenkins.getJobsByOrder(start, end)

    def getLatestNum(self):
        return self.jenkins.getLatestNum()
