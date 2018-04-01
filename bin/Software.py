import os
import bin.Drive
import shutil
import bin.SoftwareChild
import copy


class Software(object):

    def __init__(self, module, child, parameter, config, parent_class=object):
        self.zip_file_name = parameter['info']['file_name'].replace('{version}', parameter['version'])
        self.zip_file_path = config.config['download_path'] + os.sep + self.zip_file_name
        self.source_dir_path = config.config['source_path'] + os.sep + self.zip_file_name.replace(
            parameter['info']['ext_name'],
            '')

        self.source_ok = False
        self.drive = bin.Drive.Drive()
        self.module = str(module)
        self.child = str(child)
        self.parameter = parameter
        self.config = config
        if self.child != "":
            self.config_parameter = config.supported[module]['children'][child]
        else:
            self.config_parameter = config.supported[module]
        self.option = ''
        self.install_module_name = self.module
        self.install_child_name = self.child
        if not ('can_coexist' in self.parameter['info'] and self.parameter['info']['can_coexist'] == 1):
            self.install_child_name = ""
        if 'install_dir_name' in self.parameter['info']:
            self.install_module_name = self.parameter['info']['install_dir_name']
        self.install_dir_path = self.config.config['install_path'] + os.sep + self.install_module_name + (
                (self.install_child_name != "") and ('_' + self.install_child_name) or self.install_child_name)
        self.expand_class_list = list()
        self.parent_class = parent_class  # type:Software

    # init software

    def init_software(self):
        self.unzip(self.zip_file_path, self.config.config['source_path']).prefix(self.install_dir_path)
        if os.path.isdir(self.config.config['source_path']):
            self.source_ok = True
        return self

    def before_install(self):
        return self

    def after_install(self):
        return self

    def before_before_install(self):
        return self

    def after_before_install(self):
        return self

    def before_after_install(self):
        self.install_expand()
        return self

    def after_after_install(self):
        return self

    def before_configure(self):
        return self

    def after_configure(self):
        return self

    def before_before_configure(self):
        return self

    def after_before_configure(self):
        return self

    def before_after_configure(self):
        return self

    def after_after_configure(self):
        return self

    @property
    def child_class(self):
        module = self.module
        child = self.child
        new_module = module.capitalize()
        new_child = child.capitalize()
        if "module_class_name" in self.parameter['info']:
            new_module = self.parameter['info']['module_class_name']
        try:
            class_name = getattr(bin.SoftwareChild, (new_module + new_child))
        except AttributeError:
            try:
                class_name = getattr(bin.SoftwareChild, new_module)
            except AttributeError:
                return self  # type:Software
        return class_name(module, child, self.parameter, self.config, self.parent_class)  # type:Software

    def check_path(self):
        return self

    def install(self):
        self.before_before_install()
        self.before_install()
        self.after_before_install()
        old_work_space = os.getcwd()
        os.chdir(self.source_dir_path)
        os.system('make -j ' + str(self.drive.cpu_counts) + ' && make install')
        os.chdir(old_work_space)
        self.before_after_install()
        self.after_install()
        self.after_after_install()
        return self

    @staticmethod
    def uninstall():
        return 0

    def add_option(self, option):
        self.option += " " + option + ' '
        return self

    def unzip(self, file_name, dir_name):
        if os.path.isdir(self.source_dir_path):
            shutil.rmtree(self.source_dir_path)
        if os.system("tar zxvf " + file_name + " -C " + dir_name) == 0:
            return self
        else:
            return False

    def prefix(self, path):
        self.add_option("--prefix=" + path)
        return self

    def configure(self):
        self.before_before_configure()
        self.before_configure()
        self.after_before_configure()
        old_work_space = os.getcwd()
        os.chdir(self.source_dir_path)
        os.system('./configure' + self.option)
        os.chdir(old_work_space)
        self.before_after_configure()
        self.after_configure()
        self.after_after_configure()
        return self

    def install_rely(self):
        father_info = self.parameter['info']
        if "relies" in father_info:
            for relies in father_info['relies']:
                info = {}
                if type(relies) == list:
                    module = relies[0]
                    child = relies[1]
                    module_info = copy.deepcopy(self.config.supported[module])
                    child_info = module_info['children'][child]
                    if 'info' in module_info:
                        info = module_info['info']
                    if 'info' in child_info:
                        for info_k, info_v in child_info['info'].items():
                            info[info_k] = info_v
                    parameter = child_info
                else:
                    module = relies
                    child = ''
                    module_info = copy.deepcopy(self.config.supported[module])
                    if 'info' in module_info:
                        info = module_info['info']
                    parameter = module_info
                parameter['info'] = info
                install_class = Software(module, child, parameter, self.config).child_class
                install_class.default_install()
                if install_class.installed():
                    self.rely_end(module, child, install_class)
        return self

    def install_expand(self):
        father_info = self.parameter['info']
        if "expansion" in father_info:
            for expansion in father_info['expansion']:
                info = {}
                if type(expansion) == list:
                    module = expansion[0]
                    child = expansion[1]
                    module_info = copy.deepcopy(self.config.supported[module])
                    child_info = module_info['children'][child]
                    if 'info' in module_info:
                        info = module_info['info']
                    if 'info' in child_info:
                        for info_k, info_v in child_info['info'].items():
                            info[info_k] = info_v
                    parameter = child_info
                else:
                    module = expansion
                    child = ''
                    module_info = copy.deepcopy(self.config.supported[module])
                    if 'info' in module_info:
                        info = module_info['info']
                    parameter = module_info
                parameter['info'] = info
                install_class = Software(module, child, parameter, self.config, self).child_class
                install_class.default_install()
                if install_class.installed():
                    self.expand_end(module, child, install_class)
        return self

    def rely_end(self, module, child, install_class):
        return self

    def expand_end(self, module, child, install_class):
        return self

    def default_install(self):
        new_class = self.init_software()
        if not self.installed():
            new_class.install_rely().configure().install()
        new_class.update_config().after_install().before_after_install()
        if self.installed():
            print('已安装' + self.module + self.child)
        else:
            print(new_class.option)
            print('未成功安装' + self.module + self.child)
        return new_class

    def update_config(self):
        if self.installed():
            self.config_parameter['installed'] = 1
            self.config_parameter['install_path'] = self.install_dir_path
        else:
            self.config_parameter['installed'] = 0
            del self.config_parameter['installed']
            self.config_parameter['install_path'] = ''
            del self.config_parameter['install_path']
        return self

    def installed(self):
        if os.path.isdir(self.install_dir_path):
            return True
        else:
            return False

    def extends_hold(self):
        return self
