文档搜索系统
====
前阵子同学说单位里文档太多太乱，查资料很费劲，故受此启发，搞了这个项目。（还在完善中。。。）

说明
===========
* 通过后端管理系统上传文件，用celery搭配broker Redis异步解析文件并将信息索引至elasticsearch搜索引擎。然后在前端搜索页面给人提供搜索并下载的功能
* 默认端口 8000
* admin管理后台配置相关基础数据，数据库用的sqlite,地址为http://XX.XX.XX.XX:8000/admin,可配置相关用户信息，文档类型等。
* 前端搜索直接登陆http://XX.XX.XX.XX:8000即可，后台登陆http://XX.XX.XX.XX:8000/backend/login
* 后端管理登陆用户名密码默认用户为aaa/aaa django的admin用户名密码admin/admin
* 支持使用docker-compose快速编排部署。docker-compose up 直接使用即可， 就可以把celery redis elasticsearch等等应用快速构建。如用docker-compose起则应用端口为8001
* 如果不是用docker-compose启动，要修改setting.py中的配置 ES_URL CELERY_BROKER_URL CELERY_RESULT_BACKEND，将其配置为真实的地址
* 默认开启DEBUG=true，这样方便调试，不过这样会导致celery有内存泄漏，真想用就把DEBUG=false，并且前端加上nginx和gunicorn。
* 最后随时可能弃坑 = =

上传的流程
===========

![index](https://github.com/mnpiozhang/DocumentSearch/blob/master/example/uploadandindex.jpg)