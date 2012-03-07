## 一个简单的FTP搜索工具

* 索引部分：遍历ftp目录，获取每个文件的绝对路径(作为数据表的键)以及相关属性，并将根路径转换成ftp服务器url，将这些信息存入mysql数据库。这部分由python写成，依赖于python2.6以上版本(2.6之前以及3.0以后的版本没有测试过)。
* 搜索部分: 用户搜索关键字，服务器根据关键字查询数据库，并返回结果。这部分由PHP写成。

###配置
* 根据上述介绍，可知服务器上需要配置Apache(或者其他web server软件)+PHP+MySQL,以及Python2.6或2.7，pyMySQL模块。
* 为了及时更新索引，可以在服务器的cron中添加任务---在每天的某个时间自动执行索引部分的程序，如下例子:

>1.命令行中输入crontab -e

>2.在cron中添加新的一行: 0 2 * * * /path/to/listdir.py >> /dev/null

>3.然后为listdir.py添加可执行权限chmod +x listdir.py

>4.cron中添加那行的意思是：每天晚上2点开始执行listdir.py这个脚本脚本，并将程序标准输出信息重定向到/dev/null这个文件。关于cron的具体信息请查询man手册或者google一下

###改进
* 接下来的改进可能是将mysql替换掉，用berkelyDB来存储索引。
