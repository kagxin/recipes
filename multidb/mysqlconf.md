# jiebenpeizhi

#### env
* ubuntu 16.04 64 bit
* mysql 5.7.22


#### masetr
* 将 /etc/mysql/mysql.conf.d/mysqld.cnf 中 bind-address = 127.0.0.1 注释掉 
* grant all privileges on *.* to 'root'@'%' identified by 'root' with grant option;
* flush privieges;
* /etc/mysql/mysql.conf.d/mysqld.cnf
```
server_id=1             # 全局唯一的
log-bin=master-mysql-bin   # 开启logbin功能并设置logbin文件的名称
binlog_ignore_db=mysql      # 复制过滤，不同步mysql系统自带的数据库
binlog_cache_size=1M
binlog_format=mixed          # 混合型复制模式，默认采用基于语句的复制，一旦发现基于语句的无法精确的复制时，就会采用基于行的复制。
```
* service mysql restart

#### slave
* /etc/mysql/mysql.conf.d/mysqld.cnf
```
server_id=63
log-bin=slave-mysql-bin
binlog_ignore_db=mysql
binlog_cache_size=1M
binlog_format=mixed 
```
* slave conf cmmond
```
change master to master_host='192.168.49.130',    # master 服务器的 IP
master_user='root',           # 登录 master 服务器的用户
master_password='root',   # 登录 master 服务器的密码
master_port=3306,           # master 服务器的端口
master_log_file='master-mysql-bin.000001',     # 通过show master status看到的 File
master_log_pos=154,        # 通过show master status看到的position
master_connect_retry=30;
```
* start slave;