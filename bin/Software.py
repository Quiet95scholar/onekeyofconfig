import os
import bin.Drive


class Software(object):

    def __init__(self, path):
        self.drive = bin.Drive.Drive()
        self.path = path
        self.option = ''
        self.dirPath = path
        self.dirName = os.path.split(self.path)[1]
        self.check_path()

    def check_path(self):
        if not os.path.isdir(self.path):
            return 1

    def install(self):
        old_work_space = os.getcwd()
        os.chdir(self.path)
        os.system('make -j '+str(self.drive.cpu_counts)+' && make install')
        os.chdir(old_work_space)
        return 0

    def uninstall(self):
        self.path = self.path
        return 0

    def add_option(self, option):
        self.option += " "+option+' '
        return self

    def unzip(self, file_name):
        path_name = ""
        return path_name

    def prefix(self, path):
        self.option += " --prefix="+path+' '
        return self

    def configure(self):
        old_work_space = os.getcwd()
        os.chdir(self.path)
        os.system('make distclean')
        os.system('./config'+self.option)
        os.chdir(old_work_space)
        return self
