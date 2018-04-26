#!/usr/bin/env python3
import bin.Init as Init
import config.Config as Config
Init.Init()

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
config = config.rewrite_config()
config.check_download()
config.install()
config.write_config()
