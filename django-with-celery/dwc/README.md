#### start celery
> celery worker --concurrency=2 --app=dwc -l info

#### Running the worker as a daemon

>1. celeryd 是配置文件放在 /etc/defalut/celeryd
>2. celeryd.1 是sh脚本用于启动celery放在 /etc/init.d/celeryd
>3. [配置参考](http://docs.jinkan.org/docs/celery/tutorials/daemonizing.html)
>4. 保存pid和日志的文件夹的所有权给配置文件中指定的用户，权限0640 