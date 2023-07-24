# 使用docker的通用部署方案

本镜像适用于打算使用单机docker方式部署单用户notebook的场景

## 特点

+ 通过环境变量进行基础设置
+ 支持挂载nfs和cifs
+ 支持gpu
+ 支持根据用户名后缀配置镜像以及镜像的gpu支持设置
+ 支持postgresql和mysql作为hub的数据库

## jupyterhub的配置项

可以使用环境变量设置的项目包括

> HUB设置

+ HUB_CONNECT_IP: 默认`jupyterhub`,连接hub可以使用的ip
+ HUB_PORT: 默认`8000`,指定hub对外的端口,注意8001和8081都不能使用,
+ HUB_SSL_KEY和HUB_SSL_CERT: 可选,用于设置https方式提供服务,需要都提供
+ HUB_COOKIE_SECRET_FILE: 默认`/data/jupyterhub_cookie_secret`,hub的cookie_secret文件存放位置,注意指的是容器中的存放位置
+ HUB_DB_URL: 默认`sqlite:////data/jupyterhub.sqlite`,hub数据保存的数据库位置
+ HUB_ACTIVE_SERVER_LIMIT: 默认100,指定挂载spawner服务的最大数量,超过这个数量后hub服务将不会启动新的spawner服务,通常一个用户绑定一个spawner服务
+ HUB_ACTIVE_USER_WINDOW: 默认1800,活跃用户总数的检查间隔时间,单位s
+ HUB_ACTIVITY_RESOLUTION: 默认30,活跃用户状态刷新间隔时间,单位s,这个参数用于限制状态写入的频率
+ HUB_CONCURRENT_SPAWN_LIMIT: 默认20,同时并发的spawn数量最大值
+ HUB_INTERNAL_SSL_PATH: 可选,指定内部通信启用ssl时ssl文件存放的位置,如果设置则启用内部ssl通信
+ HUB_INIT_SPAWNERS_TIMEOUT: 默认`60`,spawner初始化最大时长

> SPAWNER设置

+ SPAWNER_NOTEBOOK_IMAGE: 默认值`jupyter/base-notebook:notebook-6.5.4`,指定SPAWNER拉起作为notebook执行器的容器使用的镜像
+ SPAWNER_PULL_POLICY: 默认值`ifnotpresent`,枚举类型,指定拉取NOTEBOOK_IMAGE使用的策略,可选的有:
    + `ifnotpresent`-如果没有就拉取
    + `always`-总是检查更新并拉取
    + `never`- 总是不拉取,如果本地没有就抛出错误
    + `skip`- 总是不拉取,但也不抛出错误
+ SPAWNER_NETWORK_NAME: 必填,指定使用的docker network名
+ SPAWNER_NOTEBOOK_DIR: 默认`/home/jovyan/work`,指定notebook容器中notebook存放路径,不建议修改
+ SPAWNER_PERSISTENCE_VOLUME_TYPE: 默认`local`,notebook服务保存的文件存放的位置类型,支持"local", "nfs3", "nfs4", "cifs"四种类型
+ SPAWNER_PERSISTENCE_VOLUME_SOURCE_NAME: 默认`jupyterhub-user-{username}`,挂载的volume名字,也就是source名
+ SPAWNER_PERSISTENCE_VOLUME_TARGET_SUBPATH: 默认`/persistence`,挂载的volume在容器中的路径,完整路径为`{SPAWNER_NOTEBOOK_DIR}{SPAWNER_PERSISTENCE_VOLUME_TARGET_SUBPATH}`
+ SPAWNER_PERSISTENCE_NFS_HOST: 如果`SPAWNER_PERSISTENCE_VOLUME_TYPE`为"nfs3"或"nfs4则必填,指定nfs服务器的地址,比如`10.0.0.10`
+ SPAWNER_PERSISTENCE_NFS_DEVICE: 如果`SPAWNER_PERSISTENCE_VOLUME_TYPE`为"nfs3"或"nfs4则必填,指定nfs服务器上的路径,比如`:/var/docker-nfs`,可以在其中设置`{username}`,它将在构造镜像时替换为用户的名称
+ SPAWNER_PERSISTENCE_NFS_OPTS: 选填,如果`SPAWNER_PERSISTENCE_VOLUME_TYPE`为"nfs3"或"nfs4则生效,nfs3时默认值为`,rw,vers=3,nolock,soft`;nfs4时默认值为`,rw,nfsvers=4,async`,指定nfs连接的配置项
+ SPAWNER_PERSISTENCE_CIFS_HOST: 如果`SPAWNER_PERSISTENCE_VOLUME_TYPE`为cifs则必填,指定cifs服务器的地址,比如`uxxxxx.your-server.de`
+ SPAWNER_PERSISTENCE_CIFS_DEVICE: 如果`SPAWNER_PERSISTENCE_VOLUME_TYPE`为cifs则必填,指定cifs服务器上的路径,比如`//uxxxxx.your-server.de/backup`
+ SPAWNER_PERSISTENCE_CIFS_OPTS:  选填,如果`SPAWNER_PERSISTENCE_VOLUME_TYPE`为cifs则生效,默认值为`,file_mode=0777,dir_mode=0777`
+ SPAWNER_CPU_LIMIT: 默认`2`,指定notebook容器最大可使用的cpu资源量
+ SPAWNER_CPU_GUARANTEE: 默认`1`,指定notebook容器最低使用的cpu资源量
+ SPAWNER_MEM_LIMIT: 默认`4G`,指定notebook容器最大可使用的内存资源量
+ SPAWNER_MEM_GUARANTEE: 默认`1G`,指定notebook容器最小可使用的内存资源量
+ SPAWNER_ENVIRONMENT: 选填,使用`A:1;B:2`这样的形式指定notebook容器的环境变量
+ SPAWNER_SPAWN_CMD: 默认`start-singleuser.sh`,指定notebook容器的启动执行命令
+ SPAWNER_REMOVE: 默认`True`,Spawner容器在程序停止后是否删除容器,注意为true时没有保存在对应volume中的数据会丢失
+ SPAWNER_DEBUG: 默认`True`,Spawner容器设为debug模式
+ SPAWNER_CONSECUTIVE_FAILURE_LIMIT: 默认0,Spawner关闭与hub连接前允许的最大故障数,0表示不限制
+ SPAWNER_POLL_INTERVAL: 默认30, 轮询Spawner的间隔,单位s
+ SPAWNER_START_TIMEOUT: 默认120,单用户容器启动最大等待时间,单位s
+ SPAWNER_USE_GPUS: 选填,spawner对应的容器是否需要使用gpu,使用几个gpu,可以为正整数或为-1或者all,也可以使用`device_ids=xxx,xxx`指定使用的gpu设备号
+ SPAWNER_CONSTRAINT_IMAGES: 选填,有值则生效,根据用户名的后缀确定部署镜像和限制,形式如`后缀1->镜像名1;后缀2->镜像名2...`当登录用户用户名有后缀`-后缀1`时会使用镜像1而非默认镜像构造容器
+ SPAWNER_CONSTRAINT_WITH_GPUS: 选填,当SPAWNER_CONSTRAINT_IMAGES生效时可以生效,指定后缀是否使用gpu,gpu设置语法与SPAWNER_USE_GPUS一致,形式如`后缀1->gpu设置1;....`

> AUTH设置

+ AUTH_ADMIN_USER: 默认`admin`,指定admin用户的用户名,多个用`,`隔开
+ AUTH_CHECK_COMMON_PASSWORD: 默认`False`,是否启用复杂密码校验
+ AUTH_MINIMUM_PASSWORD_LENGTH: 默认`6`,密码长度校验
+ AUTH_ALLOWED_FAILED_LOGINS: 默认`3`,最大登录错误次数
+ AUTH_SECONDS_BEFORE_NEXT_TRY: 默认`1200`,重试最长间隔时间
+ AUTH_ENABLE_SIGNUP: 默认`True`,是否开放新用户注册
+ AUTH_OPEN_SIGNUP: 默认`False`,是否允许用户注册后未经管理员确认就可以进入使用

## 例子

比如我们可以使用如下例子部署

```yml
version: "2.4"
services:
    jupyterhub:
        image: hsz1273327/jupyterhub-for-standalone:4.0.1
        hostname: jupyterhub
        container_name: jupyterhub
        networks:
            - jupyterhub_network
        ports:
            - 8001:8000
        volumes:
            - "/var/run/docker.sock:/var/run/docker.sock"
            - "jupyterhub-data:/data"
        environment:
            HUB_PORT: 8000
            SPAWNER_NETWORK_NAME: jupyterhub_network
            SPAWNER_NOTEBOOK_IMAGE: hsz1273327/small-dataset-notebook:notebook-6.5.4
            SPAWNER_CONSTRAINT_IMAGES: "base->jupyter/base-notebook:notebook-6.5.4;spark->jupyter/all-spark-notebook:notebook-6.5.4"
            SPAWNER_PERSISTENCE_VOLUME_TYPE: "nfs3"
            SPAWNER_PERSISTENCE_NFS_HOST: xxxxx.nas.aliyuncs.com # nas的host
            SPAWNER_PERSISTENCE_NFS_DEVICE: ":/nas/jupyterhub/{username}"
            SPAWNER_PERSISTENCE_NFS_OPTS: ",vers=3,nolock,hard"
volumes:
    jupyterhub-data:

networks:
    jupyterhub_network:
        external: true
```
