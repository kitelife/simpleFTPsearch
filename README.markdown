## FTP简易搜索(第二版)
* 在第一版中，采用cron定时任务对ftp的目录进行索引，每次索引之前清空数据库，然后遍历所有目录，将文件，文件夹的绝对路径和名称插入mysql中。搜索的过程是直接查询mysql数据库。定时任务的缺点是：两次任务的时间间隔中。文件以及文件目录的变化是不会被即时索引的。另外，在这样一个简单的应用中，数据的操作非常简单，使用mysql反而效率不高。
* 所以第二版中，采用pyinotify库(基于内核的inotify功能)来监听ftp的目录，进行实时索引，数据库引擎则采用Berkely DB。搜索部分采用python cgi脚本。
* 目前存在的问题是，inotify监听的目录数量虽然可以自行设置，但数量应该和内存使用相关，这一点可能会限制能够监听的目录数量。

###配置
* 由于采用python cgi脚本来实现搜索部分的功能，所以需要配置apache的cgi。
** 下载安装libapache2-mod-python：sudo apt-get install libapache2-mod-python
** 将search文件夹内的文件和子文件夹置于apache的DocumentRoot下。
** 打开文件/etc/apache2/sites-available/default，找到如下部分内容:

> ScriptAlias /cgi-bin/ /var/www/cgi-bin/
>
> <Directory "/var/www/cgi-bin">
>
>    AllowOverride None
>
>    Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
>
>    Order allow,deny
>
>    Allow from all
>
> </Directory>

修改为:


> ScriptAlias /cgi-bin/ /var/www/cgi-bin/
>
> <Directory "/var/www/cgi-bin">
>
>    AllowOverride None
>
>    Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
>
>    Order allow,deny
>
>    Allow from all
>
>    AddHandler cgi-script .py
>
>    AddHandler default-handler .html .htm
>
> </Directory>

** 重启apache：sudo /etc/init.d/apache2 restart

### 注意：
* 需要给python cgi脚本result.py添加可执行权限，且保证文件格式正确(使用file命令检查，如果输出中有a python script这样的信息则正确)
