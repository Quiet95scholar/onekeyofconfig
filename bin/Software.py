import os


class Software(object):

    def __init__(self, path):
        self.path = path
        self.THREAD = 1
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
        os.system('make -j '+str(self.THREAD)+' && make install')
        os.chdir(old_work_space)
        return 0

    def uninstall(self):
        self.path = self.path
        return 0

    def add_option(self, option):
        self.option += " "+option+' '
        return self

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