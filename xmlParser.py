import xml.etree.ElementTree as ET


class XmlParser:

    def __init__(self, tree, params):
        self.tree = tree
        self.root = ET.fromstring(tree)
        self.params = params

    def getAllBuilds(self):
        builds = []
        for build in self.root.iter('build'):
            builds.append(build)
        return builds

    def builds2Objects(self, builds):
        objects = []
        for build in builds:
            obj = {}
            info_action = build.findall('action')[0]
            parameters = info_action.findall('parameter')
            for parameter in parameters:
                for p in self.params:
                    if parameter.find('name').text == p:
                        obj[p] = parameter.find('value').text 
                #if p.find('name').text == 'BranchName':
                #    obj['BranchName'] = p.find('value').text
                #if p.find('name').text == 'BuildNumber':
                #    obj['BuildNumber'] = p.find('value').text
            obj['Duration'] = build.find('duration').text
            obj['Job'] = build.find('number').text
            obj['Timestamp'] = build.find('timestamp').text
            obj['Url'] = build.find('url').text
            # skip if in progress
            try:
                obj['Status'] = build.find('result').text
                objects.append(obj)
            except:
                continue
        return objects

    def getAllObjects(self):
        builds = self.getAllBuilds()
        return self.builds2Objects(builds)
