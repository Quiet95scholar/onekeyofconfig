import os
try:
    import json
except ModuleNotFoundError:
    os.system('pip install json')
    import json
try:
    import platform
except ModuleNotFoundError:
    os.system('pip install platform')
    import platform
try:
    import multiprocessing
except ModuleNotFoundError:
    os.system('pip install multiprocessing')
    import multiprocessing
try:
    import requests
except ModuleNotFoundError:
    os.system('pip install requests')


class Drive(object):

    def __init__(self):
        self.system_name = platform.system()
        self.cpu_counts = multiprocessing.cpu_count()
        self.system_size = platform.machine().find('64') > 0 and 64 or 32
        self.abbr = self.network
        if self.system_name == 'Linux':
            self.system_branch_name = self.get_linux_branch_name
            self.version = self.get_linux_version
            self.big_version = self.version.split('.')[0]
            self.is_wsl = self.check_is_wsl
        elif self.system_name == 'Windows':
            self.version = platform.version()
            self.big_version = self.version.split('.')[0]
            self.system_branch_name = platform.system() + self.big_version

    @property
    def get_linux_branch_name(self):
        """
        返回当前系统的linux分支名称ubuntu/centos/debain
        :return:
        """
        name = 'other'
        if len(os.popen('which lsb_release').read()) > 0:
            name = os.popen('lsb_release -is').read().strip('\n')
        elif self.install_lsb == 0:
            name = os.popen('lsb_release -is').read().strip('\n')
        return name

    @property
    def get_linux_version(self):
        """
        返回当前系统的linux分支版本
        :return:
        """
        version = 0
        if len(os.popen('which lsb_release').read()) > 0:
            version = os.popen('lsb_release -sr').read().strip('\n')
        elif self.install_lsb == 0:
            version = os.popen('lsb_release -sr').read().strip('\n')
        return version

    @property
    def check_is_wsl(self):
        """
        返回当前系统是否是WSL系统
        :return:
        """
        system = os.popen("uname -r | awk -F- '{print $3}'").read()
        if system == 'Microsoft':
            return True
        else:
            return False

    @property
    def install_lsb(self):
        if len(os.popen('which yum').read()) > 0:
            order = 'yum'
            return os.system(order + ' install -y redhat-lsb')
        elif len(os.popen('which apt-get').read()) > 0:
            order = 'apt-get'
            return os.system(order + ' install -y lsb-release')

    @property
    def network(self):
        # noinspection PyBroadException
        try:
            url = 'http://ip.taobao.com/service/getIpInfo.php?ip=myip'
            country_id = json.loads(requests.get(url, timeout=5, allow_redirects=True).text)['data']['country_id']
        except BaseException:
            country_id = 'ALL'
        return country_id
