import json
import os
import bin.Drive
import bin.Tools
import platform
import multiprocessing

import requests


class Config(object):

    def __init__(self):
        self.all_config = self.all
        self.drive = bin.Drive.Drive()
        self.Tools = bin.Tools.Tools()
        self.config['work_space'] = os.getcwd()

    @property
    def all(self):
        config_file = open('config.json', 'r')
        config = json.load(config_file)
        config_file.close()
        return config

    @property
    def config(self):
        return self.all_config['config']

    @property
    def supported(self):
        return self.all_config['supported']

    @property
    def status(self):
        return self.all_config['status']

    def check_download(self, module=''):
        old_work_space = os.getcwd()
        download_path = self.config['download_path']
        if not os.path.isdir(download_path):
            os.makedirs(download_path)
        os.chdir(download_path)
        for module, module_info in self.supported.items():
            info_p = {}
            if 'info' in module_info:
                info_p = module_info['info']
            if 'default' in module_info:
                version = module_info['version']
                info = info_p
                if module_info['will_install'] == 1:
                    download_url = (info['download_url'][self.drive.abbr] if self.drive.abbr in info['download_url'] else info['download_url']['ALL']).replace('{version}', version)
                    self.Tools.download_file(download_url, info['file_name'].replace('{version}', version))
            if 'children' in module_info:
                for child, child_info in module_info['children'].items():
                    version = child_info['version']
                    info = info_p
                    if 'info' in child_info:
                        for info_k, info_v in child_info['info'].items():
                            info[info_k] = info_v
                    if child_info['will_install'] == 1:
                        download_url = (info['download_url'][self.drive.abbr] if self.drive.abbr in info['download_url'] else info['download_url']['ALL']).replace('{version}', version)
                        self.Tools.download_file(download_url, info['file_name'].replace('{version}', version))
        os.chdir(old_work_space)
        return True

    def write_config(self):
        config = self.all_config
        config_file = open('config.json', 'w')
        json.dump(config, config_file, skipkeys=True, indent=4)
        config_file.close()
