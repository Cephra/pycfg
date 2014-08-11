import os.path
import os
import shutil

class CfgBuilder:
    fnum = -1
    fnames = list()
    files = list()

    def __init__(self, name, wait=200):
        self.name = name
        self.wait = wait
        return

    def appendLine(self, line):
        if (self.fnum == -1):
            self.newFile()
        subfile = self.files[self.fnum]
        subfile.append(line+os.linesep)
        return

    def newFile(self):
        self.files.append(list())
        self.fnum += 1
        return

    def rawCmd(self, cmd):
        self.appendLine(cmd)
        return

    def build(self):
        self._cfilenum = 0
        def filename():
            fname = "{0}/gen{1}.cfg".format(self.name, self._cfilenum)
            self.fnames.append(fname)
            self._cfilenum += 1
            return fname

        if not os.path.exists(self.name):
            os.makedirs(self.name)
        else:
            shutil.rmtree("{0}".format(self.name), True)
            os.makedirs(self.name)

        # walk through all the files and write their contents
        for fnum, cfile in enumerate(self.files):
            f = open(filename(), "w")
            for line in cfile:
                f.write(line)
            f.close()

        wait = 0
        f = open("pycfg_{0}.cfg".format(self.name), "w")
        for name in self.fnames:
            f.write("wait {0}; exec {1}\n".format(wait, name))
            wait += self.wait
        f.write("wait {0}; echo done!\n".format(wait))
        f.close()
        return
