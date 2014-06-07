import os.path
import shutil

class CfgBuilder:
    fnum = 0
    fnames = list()
    lines = list()

    def __init__(self, name, wait=200):
        self.name = name
        self.wait = wait
        return

    def appendLine(self, line):
        self.lines.append(line+"\n")
        return

    def rawCmd(self, cmd):
        self.appendLine(cmd)
        return

    def build(self):
        def filename():
            fname = "{0}/gen{1}.cfg".format(self.name, self.fnum)
            self.fnames.append(fname)
            return fname

        if not os.path.exists(self.name):
            os.makedirs(self.name)
        else:
            shutil.rmtree("{0}/".format(self.name), True)
            os.makedirs(self.name)

        f = open(filename(), "w")

        for lc, line in enumerate(self.lines):
            # if 30 lines were read, open new file for writing
            if ((lc+1)%30 == 0):
                f.close()
                self.fnum += 1
                f = open(filename(), "w")

            # write line to file
            f.write(line)

        wait = 0
        f = open("pycfg_{0}.cfg".format(self.name), "w")
        for name in self.fnames:
            f.write("wait {0}; exec {1}\n".format(wait, name))
            wait += self.wait
        f.write("wait {0}; echo done!\n".format(wait))
        f.close()
        return
