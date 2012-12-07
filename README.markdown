## FTP简易搜索(第二版)
* 在第一版中，采用cron定时任务对ftp的目录进行索引，每次索引之前清空数据库，然后遍历所有目录，将文件，文件夹的绝对路径和名称插入mysql中。搜索的过程是直接查询mysql数据库。定时任务的缺点是：两次任务的时间间隔中。文件以及文件目录的变化是不会被即时索引的。另外，在这样一个简单的应用中，数据的操作非常简单，使用mysql反而效率不高。
* 所以第二版中，采用pyinotify库(基于内核的inotify功能)来监听ftp的目录，进行实时索引，数据库引擎则采用Berkely DB。搜索部分采用python cgi脚本。
* 目前存在的问题是，inotify监听的目录数量虽然可以自行设置，但数量应该和内存使用相关，这一点可能会限制能够监听的目录数量。

###配置

* 安装python-pyinotify, python-bsddb3：sudo apt-get install python-pyinotify python-bsddb3

由于采用python cgi脚本来实现搜索部分的功能，所以需要配置apache的cgi。

* 下载安装libapache2-mod-python：sudo apt-get install libapache2-mod-python
* 将search文件夹内的文件和子文件夹置于apache的DocumentRoot下。
* 打开文件/etc/apache2/sites-available/default，找到如下部分内容:

> ScriptAlias /cgi-bin/ /var/www/cgi-bin/
>
> \<Directory "/var/www/cgi-bin"\>
>
>    AllowOverride None
>
>    Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
>
>    Order allow,deny
>
>    Allow from all
>
> \</Directory\>

修改为:


> ScriptAlias /cgi-bin/ /var/www/cgi-bin/
>
> \<Directory "/var/www/cgi-bin"\>
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
> \</Directory\>

* 重启apache：sudo /etc/init.d/apache2 restart

另外还需要注意配置index的config.py，以及search的cgiConfig.py文件。

### 使用

* 建立索引数据库并监听ftp目录: sudo python ftpIndexer.py -i \>\> ftpindex.log &
* 文件testIndex.py可用于测试是否成功建立索引数据库: python testIndex.py 关键字

### 注意：
* 需要给python cgi脚本result.py添加可执行权限，且保证文件格式正确(使用file命令检查，如果输出中有a python script这样的信息则正确)
* linux内核的文件系统监听功能(inotify)对监听文件/目录(包括递归监听的)的数目是有配额的，默认比较小(为8192)，监听初始化时，如果要监听的数目超过了配合，就会抛出异常pyinotify ERROR。这时需要手动更改这个配额的值。在pyinotify项目wiki的[Frequently-Asked-Questions](https://github.com/seb-m/pyinotify/wiki/Frequently-Asked-Questions)中说明了如何查看，如何更改这个配额。
>
>I always get WD=-1 or the message No space left on device (ENOSPC) whenever I try to add a new watch
>You must have reached your quota of watches, type sysctl -n fs.inotify.max_user_watches to read your current limit and type sysctl -n -w fs.inotify.max_user_watches=16384 to modify (increase) it.

### 更新:

2012-12-04: 之前的代码中是使用配置文件中一个硬编码的外网ip来生成搜索结果中的ftp下载链接的。但某些情况下，在内网只能使用服务器的内网ip(比如192.168.1.254)来访问ftp搜索服务，那么这时生成的下载超链接是无效的，需要用户手动修改下载链接中的服务器域名或者外网ip。新代码中使用os.environ['SERVER_NAME']环境变量来根据用户请求url中的域名或者服务器ip部分来生成搜索结果中的下载超链接。
