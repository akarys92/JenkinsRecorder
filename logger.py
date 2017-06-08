from datetime import datetime

class Logger:
    def __init__(self, relative_path):
        logfile_loc = relative_path

        self.logfile = open(logfile_loc, 'a')
        self.now = datetime.now().isoformat()

    def logRun(self):
        self.logfile.write("<Beginning run at " + self.now +" > \n")

    def logSuccess(self, input="No comment"):
        self.logfile.write("\t Run success: " + input + "\n")

    def logFailure(self, input="No Comment"):
        self.logfile.write("\t Iteration fail: " + input + "\n")

    def close(self):
        self.logfile.close()
