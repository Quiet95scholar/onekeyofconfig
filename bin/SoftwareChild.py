import os
import shutil
import re
import bin.Software


class Php(bin.Software.Software):

    def before_configure(self):

        apache_num = 0
        php_num = 0
        for child, child_info in self.config.supported['php']['children'].items():
            if child_info['will_install'] == 1 or child_info['installed'] == 1:
                php_num = php_num + 1
        for child, child_info in self.config.supported['apache']['children'].items():
            if child_info['will_install'] == 1 or child_info['installed'] == 1:
                apache_num = apache_num + 1

        # 当安装apache且php只安装一个版本时
        if apache_num > 0 and php_num <= 1:
            self.add_option('--with-apxs2=$apache_install_dir/bin/apxs')
        # 当未安装apache或者已安装的php与将要安装的php多于一个版本时
        else:
            self.add_option('--enable-fpm')
            self.add_option('--with-fpm-user=' + self.config.config['run_user'])
            self.add_option('--with-fpm-group=' + self.config.config['run_group'])
        # 当php版本大于54时
        if int(self.child) > 54:
            self.add_option('--enable-mysqlnd')
        # 当php版本小于55时
        if int(self.child) < 55:
            self.add_option('--with-mysql=mysqlnd')
        # 当php版本大于54时且开启了opcache
        self.add_option('--enable-opcache')
        # 当php版本大于54时且未开启opcache
        self.add_option('--disable-opcache')
        # 公共部分
        self.add_option('--with-config-file-path=' + self.install_dir_path + 'etc')
        self.add_option('--with-config-file-scan-dir=' + self.install_dir_path + 'etc/php.d')
        self.add_option('--disable-fileinfo')
        self.add_option('--with-mysqli=mysqlnd')
        self.add_option('--with-pdo-mysql=mysqlnd')
        self.add_option('--with-iconv-dir=/usr/local')
        self.add_option('--with-freetype-dir')
        self.add_option('--with-jpeg-dir')
        self.add_option('--with-png-dir')
        self.add_option('--with-zlib')
        self.add_option('--with-libxml-dir=/usr')
        self.add_option('--enable-xml')
        self.add_option('--disable-rpath')
        self.add_option('--enable-bcmath')
        self.add_option('--enable-shmop')
        self.add_option('--enable-exif')
        self.add_option('--enable-sysvsem')
        self.add_option('--enable-inline-optimization')
        self.add_option('--with-curl=/usr/local')
        self.add_option('--enable-mbregex')
        self.add_option('--enable-mbstring')
        self.add_option('--with-mcrypt')
        self.add_option('--with-gd')
        self.add_option('--enable-gd-native-ttf')
        # self.add_option('--with-openssl=${openssl_install_dir}')
        self.add_option('--with-mhash')
        self.add_option('--enable-pcntl')
        self.add_option('--enable-sockets')
        self.add_option('--with-xmlrpc')
        self.add_option('--enable-ftp')
        self.add_option('--enable-intl')
        self.add_option('--with-xsl')
        self.add_option('--with-gettext')
        self.add_option('--enable-zip')
        self.add_option('--enable-soap')
        self.add_option('--disable-debug')
        return self


class Openssl(bin.Software.Software):

    def before_install(self):
        return self

    def after_install(self):
        return self

    def before_configure(self):
        self.add_option("-fPIC")
        self.add_option("shared")
        self.add_option("zlib-dynamic")
        return self

    def configure(self):
        self.before_before_configure()
        self.before_configure()
        self.after_before_configure()
        old_work_space = os.getcwd()
        os.chdir(self.source_dir_path)
        os.system('./config' + self.option)
        os.chdir(old_work_space)
        self.before_configure()
        self.after_configure()
        self.after_after_configure()
        return self


class AprUtil(bin.Software.Software):
    def rely_end(self, module, child, install_class):
        if module == 'apr':
            self.add_option('--with-apr=' + install_class.install_dir_path)
        return self


class Apache(bin.Software.Software):
    def __init__(self, module, child, parameter, config, parent_class=object):
        super().__init__(module, child, parameter, config, parent_class)
        self.port = 80

    def before_configure(self):
        self.add_option('--with-mpm=prefork')
        self.add_option('--with-included-apr')
        self.add_option('--enable-headers')
        self.add_option('--enable-deflate')
        self.add_option('--enable-so')
        self.add_option('--enable-rewrite')
        self.add_option('--enable-expires')
        self.add_option('--enable-static-support')
        self.add_option('--enable-suexec')
        self.add_option('--enable-modules=all')
        self.add_option('--enable-mods-shared=all')
        if int(self.child) == 24:
            self.add_option('--enable-dav')
        os.system('LDFLAGS=-ldl')
        return self

    def after_install(self):
        os.system('unset LDFLAGS')
        if self.installed():
            if self.drive.system_name == 'Linux':
                profile = open("/etc/profile.d/" + self.module + ".sh", "w")
                profile.write("export PATH=" + self.install_dir_path + os.sep + "bin" + os.sep + ":$PATH")
                profile.close()
                file_data = ""
                file = self.install_dir_path + os.sep + "conf" + os.sep + "httpd.conf"
                with open(file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = re.sub(r'^(\s*)User.*', "\\1User " + self.config.config['run_user'], line)
                        line = re.sub(r'^(\s*)Group.*', "\\1Group " + self.config.config['run_group'], line)
                        if self.config.installed('nginx'):
                            self.port = 88
                            line = re.sub(r'^(\s*)[#]?ServerName.*', "\\1ServerName " + "127.0.0.1:" + str(self.port),
                                          line)
                            line = re.sub(r'^(\s*)Listen.*', "\\1Listen " + str(self.port), line)
                            line = re.sub(r'^(\s*LogFormat\s+"%\S+\s+)(.*)', "\\1%a \\2", line)
                            line = re.sub(r'^(\s*)(Include.*httpd-mpm.conf.*)', '''\\1\\2
\\1Include conf/extra/httpd-remoteip.conf''', line)
                        else:
                            line = re.sub(r'^(\s*)[#]?ServerName.*', "\\1ServerName " + "0.0.0.0:" + str(self.port),
                                          line)
                        line = re.sub(r'^(\s*)AddType(.*)\.Z',
                                      "\\1AddType\\2.Z\n"
                                      "\\1AddType application/x-httpd-php .php .phtml\n"
                                      "\\1AddType application/x-httpd-php-source .phps",
                                      line)
                        line = re.sub(r'^(\s*)#(AddHandler.*\.cgi)', "\\1\\2 .pl", line)
                        line = re.sub(r'^(\s*DirectoryIndex.*)', "\\1 index.php", line)
                        line = re.sub(r'^(\s*DocumentRoot)\s*\".*htdocs\"',
                                      "\\1 \"" + self.config.config['wwwroot_dir'] + os.sep + "default\"", line)
                        line = re.sub(r'^(\s*<Directory)\s*\".*htdocs\">',
                                      "\\1 \"" + self.config.config['wwwroot_dir'] + os.sep + "default\">", line)
                        line = re.sub(r'^(\s*)[#]?(Include.*httpd-mpm\.conf)', "\\1\\2", line)
                        if int(self.child) == 24:
                            line = re.sub(r'^(\s*)[#]?(.*mod_suexec.so)', "\\1\\2", line)
                            line = re.sub(r'^(\s*)[#]?(.*mod_vhost_alias.so)', "\\1\\2", line)
                            line = re.sub(r'^(\s*)[#]?(.*mod_rewrite.so)', "\\1\\2", line)
                            line = re.sub(r'^(\s*)[#]?(.*mod_deflate.so)', "\\1\\2", line)
                            line = re.sub(r'^(\s*)[#]?(.*mod_expires.so)', "\\1\\2", line)
                            line = re.sub(r'^(\s*)[#]?(.*mod_ssl.so)', "\\1\\2", line)
                            line = re.sub(r'^(\s*)[#]?(.*mod_http2.so)', "\\1\\2", line)
                        file_data += line
                file_data += '''
<IfModule mod_headers.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/css text/xml text/javascript
  <FilesMatch "\.(js|css|html|htm|png|jpg|swf|pdf|shtml|xml|flv|gif|ico|jpeg)\$">
    RequestHeader edit "If-None-Match" "^(.*)-gzip(.*)\$" "\$1\$2"
    Header edit "ETag" "^(.*)-gzip(.*)\$" "\$1\$2"
  </FilesMatch>
  DeflateCompressionLevel 6
  SetOutputFilter DEFLATE
</IfModule>

ProtocolsHonorOrder On
PidFile /var/run/httpd.pid
ServerTokens ProductOnly
ServerSignature Off
Include conf/vhost/*.conf'''
                with open(file, "w", encoding="utf-8") as f:
                    f.write(file_data)
                f.close()
                vhost_path = self.install_dir_path + os.sep + "conf" + os.sep + "vhost"
                if not os.path.isdir(vhost_path):
                    os.makedirs(vhost_path)

                default_conf_file = open(vhost_path + os.sep + "0.conf", "w", encoding="utf-8")
                default_conf_file.write('''<VirtualHost *:''' + str(self.port) + '''>
  ServerAdmin admin@example.com
  DocumentRoot "''' + self.config.config['wwwroot_dir'] + '''/default"
  ServerName 127.0.0.1 
  ErrorLog "''' + self.config.config['wwwlogs_dir'] + '''/error_apache.log"
  CustomLog "''' + self.config.config['wwwlogs_dir'] + '''/access_apache.log" common
<Directory "''' + self.config.config['wwwroot_dir'] + '''/default">
  SetOutputFilter DEFLATE
  Options FollowSymLinks ExecCGI''' + (int(self.child) == 24 and '''
  Require all granted''' or '') + '''
  AllowOverride All
  Order allow,deny
  Allow from all
  DirectoryIndex index.html index.php
</Directory>
<Location /server-status>
  SetHandler server-status
  Order Deny,Allow
  Deny from all
  Allow from 127.0.0.1
</Location>
</VirtualHost>''')
                default_conf_file.close()
                if self.config.installed('nginx'):
                    with open(
                            self.install_dir_path + os.sep + "conf" + os.sep + "extra" + os.sep + "httpd-remoteip.conf",
                            "w", encoding="utf-8") as f:
                        f.write('''LoadModule remoteip_module modules/mod_remoteip.so
RemoteIPHeader X-Forwarded-For
RemoteIPInternalProxy 127.0.0.1''')
                    f.close()

        return self

    def rely_end(self, module, child, install_class):
        if module == 'apr' or module == 'apr-util':
            to_idr = self.source_dir_path + os.sep + "srclib" + os.sep + install_class.module
            if os.path.isdir(to_idr):
                shutil.rmtree(to_idr)
            shutil.copytree(install_class.source_dir_path, to_idr)
        if module == 'nghttp2':
            self.add_option('--enable-http2')
            self.add_option('--with-nghttp2=' + install_class.config_parameter['install_path'])
        if module == 'pcre':
            self.add_option('--with-pcre=' + install_class.config_parameter['install_path'])
        if module == 'openssl':
            os.system(
                'LD_LIBRARY_PATH=' + install_class.config_parameter['install_path'] + os.sep + 'lib:$LD_LIBRARY_PATH')
            self.add_option('--enable-ssl')
            self.add_option('--with-ssl=' + install_class.config_parameter['install_path'])
        return self

    def installed(self):
        if os.path.isfile(self.install_dir_path + os.sep + "conf" + os.sep + "httpd.conf"):
            return True
        else:
            return False


class Nginx(bin.Software.Software):
    def before_configure(self):
        self.add_option('--user=www')
        self.add_option('--group=www')
        self.add_option('--with-http_stub_status_module')
        self.add_option('--with-http_v2_module')
        self.add_option('--with-http_ssl_module')
        self.add_option('--with-http_gzip_static_module')
        self.add_option('--with-http_realip_module')
        self.add_option('--with-http_flv_module')
        self.add_option('--with-http_mp4_module')
        self.add_option('--with-ld-opt="-ljemalloc"')
        return self

    def rely_end(self, module, child, install_class):
        if module == 'pcre':
            self.add_option('--with-pcre=' + install_class.config_parameter['install_path'])
            self.add_option('--with-pcre-jit')
        return self


class HttpdRemoteip(bin.Software.Software):
    def default_install(self):
        print(self.parent_class.install_dir_path)

    def installed(self):
        if os.path.isdir(self.install_dir_path):
            return True
        else:
            return False

    def expand_end(self, module, child, install_class):
        return self
