import os
import bin.Drive
import time
import re
import requests


class Tools(object):

    @staticmethod
    def input_re(msg="请输入选项", default="", pattern="", flags=0, t=0):
        want = default
        while 1:
            input_str = input(msg)
            if re.match(pattern, input_str, flags=flags):
                if not input_str == '':
                    want = input_str.lower()
                break
            else:
                print('\r' + '\t' * t + '*****  ' + 'Input error!' + '  *****', end='')
                time.sleep(0.5)
        select_list = list(filter(lambda x: x and x.strip(), re.split(r'\s+', want)))
        select_list = sorted(set(select_list), key=select_list.index)
        if len(select_list) > 1:
            return select_list
        return select_list[0]

    @staticmethod
    def download_file(url, file_name):
        file_url = url
        r = requests.get(file_url, stream=True)
        content_size = int(r.headers['content-length'])
        download_size = 0
        if not (os.path.isfile(file_name) and content_size == os.path.getsize(file_name)):
            with open(file_name, "wb") as file:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        download_size += len(chunk)
                        file.write(chunk)
                        if download_size == content_size:
                            end = '\n'
                        else:
                            end = ''
                        print('\r正在下载' + file_name + ' ' + str(download_size) + "/" + str(content_size), end=end)
        if os.path.isfile(file_name):
            print(file_name+' 检查成功')
            return True
        else:
            return False
