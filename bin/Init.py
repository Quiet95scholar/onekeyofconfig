from subprocess import PIPE
from subprocess import Popen


class Init(object):

    def __init__(self):
        popen_link = Popen(["which", "pip3"], stdout=PIPE)
        popen_link.wait()
        if popen_link.returncode > 0:
            raise Exception('本系统不存在pip3')
        pip3_path = popen_link.communicate()[0].decode()
        try:
            import json
        except ModuleNotFoundError:
            popen_link = Popen([pip3_path, "install", "json"])
            popen_link.wait()
            if popen_link.returncode > 0:
                raise Exception('本系统不存在json')
        try:
            import platform
        except ModuleNotFoundError:
            popen_link = Popen([pip3_path, "install", "platform"])
            popen_link.wait()
            if popen_link.returncode > 0:
                raise Exception('本系统不存在platform')
        try:
            import multiprocessing
        except ModuleNotFoundError:
            popen_link = Popen([pip3_path, "install", "multiprocessing"])
            popen_link.wait()
            if popen_link.returncode > 0:
                raise Exception('本系统不存在multiprocessing')
        try:
            import requests
        except ModuleNotFoundError:
            popen_link = Popen([pip3_path, "install", "requests"])
            popen_link.wait()
            if popen_link.returncode > 0:
                raise Exception('本系统不存在requests')
        try:
            import shutil
        except ModuleNotFoundError:
            popen_link = Popen([pip3_path, "install", "shutil"])
            popen_link.wait()
            if popen_link.returncode > 0:
                raise Exception('本系统不存在shutil')
        try:
            import sys
        except ModuleNotFoundError:
            popen_link = Popen([pip3_path, "install", "sys"])
            popen_link.wait()
            if popen_link.returncode > 0:
                raise Exception('本系统不存在sys')
        try:
            import time
        except ModuleNotFoundError:
            popen_link = Popen([pip3_path, "install", "time"])
            popen_link.wait()
            if popen_link.returncode > 0:
                raise Exception('本系统不存在time')
        try:
            import re
        except ModuleNotFoundError:
            popen_link = Popen([pip3_path, "install", "re"])
            popen_link.wait()
            if popen_link.returncode > 0:
                raise Exception('本系统不存在re')
        try:
            import multiprocessing
        except ModuleNotFoundError:
            popen_link = Popen([pip3_path, "install", "multiprocessing"])
            popen_link.wait()
            if popen_link.returncode > 0:
                raise Exception('本系统不存在multiprocessing')
        try:
            import copy
        except ModuleNotFoundError:
            popen_link = Popen([pip3_path, "install", "copy"])
            popen_link.wait()
            if popen_link.returncode > 0:
                raise Exception('本系统不存在copy')
