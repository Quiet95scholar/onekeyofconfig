import copy
import json
import os

import bin.Drive
import bin.Tools
import re
import bin.Tools as Tools


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

    def check_download(self):
        old_work_space = os.getcwd()
        download_path = self.config['download_path']
        if not os.path.isdir(download_path):
            os.makedirs(download_path)
        os.chdir(download_path)
        for module, module_info in copy.deepcopy(self.supported).items():
            info_p = {}
            if 'info' in module_info:
                info_p = module_info['info']
            if 'children' not in module_info:
                version = module_info['version']
                info = copy.deepcopy(info_p)
                if "will_install" in module_info and module_info['will_install'] == 1:
                    self.download(version, info)
            if 'children' in module_info:
                for child, child_info in module_info['children'].items():
                    version = child_info['version']
                    info = copy.deepcopy(info_p)
                    if 'info' in child_info:
                        for info_k, info_v in child_info['info'].items():
                            info[info_k] = info_v
                    if "will_install" in child_info and child_info['will_install'] == 1:
                        self.download(version, info)
        os.chdir(old_work_space)
        return True

    def install(self):
        for module, module_info in copy.deepcopy(self.supported).items():
            info_p = {}
            if 'info' in module_info:
                info_p = module_info['info']
            if 'children' not in module_info:
                info = copy.deepcopy(info_p)
                if "will_install" in module_info and module_info['will_install'] == 1:
                    parameter = module_info
                    parameter['info'] = info
                    bin.Software.Software(module, '', parameter,
                                          self).child_class.default_install()
            if 'children' in module_info:
                for child, child_info in module_info['children'].items():
                    info = copy.deepcopy(info_p)
                    if 'info' in child_info:
                        for info_k, info_v in child_info['info'].items():
                            info[info_k] = info_v
                    if "will_install" in child_info and child_info['will_install'] == 1:
                        parameter = child_info
                        parameter['info'] = info
                        bin.Software.Software(module, child, parameter,
                                              self).child_class.default_install()
        return True

    def write_config(self):
        for module, module_info in self.supported.items():
            if 'children' in module_info:
                for child, child_info in module_info['children'].items():
                    if "will_install" in child_info:
                        del child_info['will_install']
            else:
                if "will_install" in module_info:
                    del module_info['will_install']
        config = self.all_config
        config_file = open('config.json', 'w')
        json.dump(config, config_file, skipkeys=True, indent=4)
        config_file.close()

    def download(self, father_version, father_info):
        download_url = (
            father_info['download_url'][self.drive.abbr] if self.drive.abbr in father_info['download_url'] else
            father_info['download_url']['ALL']).replace('{version}', father_version)
        self.Tools.download_file(download_url, father_info['file_name'].replace('{version}', father_version))
        if "relies" in father_info:
            for expansion in father_info['relies']:
                info = {}
                if type(expansion) == list:
                    module = expansion[0]
                    child = expansion[1]
                    module_info = self.supported[module]
                    child_info = module_info['children'][child]
                    if 'info' in module_info:
                        info = module_info['info']
                    if 'info' in child_info:
                        for info_k, info_v in child_info['info'].items():
                            info[info_k] = info_v
                    version = child_info['version']
                else:
                    module_info = self.supported[expansion]
                    if 'info' in module_info:
                        info = module_info['info']
                    version = module_info['version']
                self.download(version, info)
        if "expansion" in father_info:
            for expansion in father_info['expansion']:
                info = {}
                if type(expansion) == list:
                    module = expansion[0]
                    child = expansion[1]
                    module_info = self.supported[module]
                    child_info = module_info['children'][child]
                    if 'info' in module_info:
                        info = module_info['info']
                    if 'info' in child_info:
                        for info_k, info_v in child_info['info'].items():
                            info[info_k] = info_v
                    version = child_info['version']
                else:
                    module_info = self.supported[expansion]
                    if 'info' in module_info:
                        info = module_info['info']
                    version = module_info['version']
                self.download(version, info)

    def installed(self, module='', child=''):
        if module in self.supported.items():
            if child == "":
                if 'installed' in self.supported[module] and self.supported[module]['installed'] == 1:
                    return True
                if 'will_install' in self.supported[module] and self.supported[module]['will_install'] == 1:
                    return True
            else:
                if 'children' in self.supported[module]:
                    if 'installed' in self.supported[module]['children'][child] and \
                            self.supported[module]['children'][child]['installed'] == 1:
                        return True
                    if 'will_install' in self.supported[module]['children'][child] and \
                            self.supported[module]['children'][child]['will_install'] == 1:
                        return True
        return False

    def rewrite_config(self):
        tools = Tools.Tools()
        if self.status == "config":
            for module, module_info in self.supported.items():
                want = 'n'
                if 'children' in module_info:
                    for child, child_info in module_info['children'].items():
                        child_info['will_install'] = 0
                        if 'default' in child_info:
                            if child_info['default'] == 1:
                                want = 'y'
                else:
                    module_info['will_install'] = 0
                    if 'default' in module_info:
                        if module_info['default'] == 1:
                            want = 'y'
                want = tools.input_re('\rWant to install ' +
                                      module +
                                      ' ? please input y/n ( default "' +
                                      want +
                                      '" ): ', want,
                                      r'^[\s]*[YN]?[\s]*$', re.IGNORECASE)
                if want == 'y':
                    info_p = {}
                    if 'info' in module_info:
                        info_p = module_info['info']
                    if 'default' in module_info:
                        module_info['will_install'] = 1
                    if 'children' in module_info:
                        print("\tplease select " + module + " version :")
                        children_list = list(module_info['children'].keys())
                        children_size = str(len(children_list))
                        default_0 = " ( * ) "
                        want_child = "0"
                        for i in children_list:
                            default = ''
                            if module_info['children'][i]['default'] == 1:
                                default = " ( * ) "
                                default_0 = ''
                                if want_child == '0':
                                    want_child = str(children_list.index(i) + 1)
                                else:
                                    want_child += " " + str(children_list.index(i) + 1)
                            print("\t\t" + str(children_list.index(i) + 1) + " : " + module + " - " + i + " - " +
                                  module_info['children'][i]['version'] + default)
                        print("\t\t0 : not install" + default_0)
                        want_child = tools.input_re(
                            '\r\tPlease select the option value , input [0-' +
                            children_size + '] ( default "' + want_child + '" ): ',
                            want_child, r'^([\s]*[0][\s]*)$|^(([\s]*[1-' + children_size + '])' +
                            (('([\s]+[0-' + children_size + '][\s]*)*')
                             if 'can_coexist' in info_p and info_p['can_coexist'] == 1 else '[\s]*') + ')?$',
                            re.IGNORECASE, 1)
                        for want_id in want_child:
                            module_info['children'][children_list[int(want_id) - 1]]['will_install'] = 1
                else:
                    if 'default' in module_info:
                        module_info['will_install'] = 0
                    if 'children' in module_info:
                        for child, child_info in module_info['children'].items():
                            child_info['will_install'] = 0
        else:
            for module, module_info in self.supported.items():
                if 'children' in module_info:
                    for child, child_info in module_info['children'].items():
                        if 'default' in child_info:
                            child_info['will_install'] = 0
                            if child_info['default'] == 1:
                                child_info['will_install'] = 1
                else:
                    if 'default' in module_info:
                        module_info['will_install'] = 0
                        if module_info['default'] == 1:
                            module_info['will_install'] = 1
        return self
