import os
try:
    import sys
except ModuleNotFoundError:
    os.system('pip install sys')
    import sys
try:
    import time
except ModuleNotFoundError:
    os.system('pip install time')
    import time
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
    import re
except ModuleNotFoundError:
    os.system('pip install re')
    import re
try:
    import requests
except ModuleNotFoundError:
    os.system('pip install requests')
    import requests
import bin.Drive as Drive
import config.Config as Config
import bin.Tools as Tools
from collections import defaultdict

# noinspection PyBroadException
# openssl = bin.Software.Software('aa')
# openssl.prefix('/usr/local/openssl').add_option('-fPIC shared zlib-dynamic').configure().install()

# drive = Drive.Drive()
# print(drive.system_name)
# print(drive.cpu_counts)
# print(drive.system_size)
# print(drive.system_branch_name)
# print(drive.version)
# print(drive.big_version)
# print(drive.abbr)

# config_file = open('config.json', 'r')
# config = json.load(config_file)
# config['Supported']['php']['version']["53"]['version'] = "5.3.29"
# config['Supported']['php']['version']["54"]['version'] = "5.4.45"
# config['Supported']['php']['version']["55"]['version'] = "5.5.38"
# config['Supported']['php']['version']["56"]['version'] = "5.6.32"
# config['Supported']['php']['version']["70"]['version'] = "7.0.26"
# config['Supported']['php']['version']["71"]['version'] = "7.1.12"
# config['Supported']['php']['version']["72"]['version'] = "7.2.0"
# config_file = open('config.json', 'w')
# json.dump(config, config_file, skipkeys=True, indent=4)
config = Config.Config()
tools = Tools.Tools()
if config.status == "config":
    for module, module_info in config.supported.items():
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
        want = tools.input_re('\rWant to install ' + module + ' ? please input y/n ( default "' + want + '" ): ', want,
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
                    '\r\tPlease select the option value , input [0-' + children_size + '] ( default "' + want_child + '" ): ',
                    want_child, r'^([\s]*[0][\s]*)$|^(([\s]*[1-' + children_size + '])' + ((
                                                                                                   '([\s]+[0-' + children_size + '][\s]*)*') if 'can_coexist' in info_p and
                                                                                                                                                info_p[
                                                                                                                                                    'can_coexist'] == 1 else '[\s]*') + ')?$',
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
    for module, module_info in config.supported.items():
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
config.check_download()
config.install()
config.write_config()
