import urllib2
import base64
import ast

class JenkinsAccess:
    # make token and username input parameters

    def __init__(self, token, username, base_url):
        self.base_url = base_url
        self.api_string = 'api/xml?'
        self.token = token
        self.username = username

    def getAllJobs(self):
        url = self.base_url + self.api_string
        return self.runQuery(url)

    def generateAuthHeader(self):
        return 'Basic ' + base64.b64encode(self.username + ':' + self.token)

    def getJobByNumber(self, job):
        url = self.base_url + str(job) + '/' + self.api_string
        return self.runQuery(url)

    def getJobsByOrder(self, start=0, end=0):
        url = self.base_url + self.api_string + 'tree=builds[number,url,duration,result,timestamp,actions[parameters[*]]]'
        if start > 0 or end > 0:
            if end > start:
                url = url + '{' + str(start) + ',' + str(end) + '}'
        return self.runQuery(url)

    def runQuery(self, url):
        authHeader = self.generateAuthHeader()
        req = urllib2.Request(url)
        req.add_header('Authorization', authHeader)
        resp = urllib2.urlopen(req)
        content = resp.read()
        return content

    def getLatestNum(self):
        url = self.base_url + 'lastBuild/api/json?tree=number'
        out = self.runQuery(url)
        o = ast.literal_eval(out)
        return o['number']
