# 使用swarm的通用部署方案

本镜像适用于打算使用swarm方式部署单用户notebook的场景

## 特点

+ 通过环境变量进行基础设置
+ 支持挂载nfs和cifs
+ 支持gpu
+ 支持根据用户名后缀配置部署节点限制,镜像以及镜像的gpu支持设置
+ 支持postgresql和mysql作为hub的数据库
+ 支持外挂proxy

## jupyterhub的配置项

可以使用环境变量设置的项目包括

jupyterhub的配置项

可以使用环境变量设置的项目包括

> 外部代理设置

+ PROXY_SHOULD_START: 默认True,执行容器是否要外接proxy,如果为True则不外接
+ PROXY_API_URL: 如果PROXY_SHOULD_START设置为False则必填,外接proxy的url
+ CONFIGPROXY_AUTH_TOKEN: 如果PROXY_SHOULD_START设置为False则必填,和外接proxy共用的认证token

> HUB设置

+ HUB_HUB_PORT: 默认`8001`,hub的内部端口
+ HUB_CONNECT_IP: 默认`jupyterhub`,连接hub可以使用的ip
+ HUB_PORT: 默认`8000`,指定hub对外的端口,proxy也会监听该接口,注意8001和8081都不能使用,
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

+ SPAWNER_NOTEBOOK_IMAGE: 默认值`jupyter/base-notebook:notebook-6.5.4`,指定SPAWNER默认拉起作为notebook执行器的容器使用的镜像
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
+ SPAWNER_PERSISTENCE_NFS_DEVICE: 如果`SPAWNER_PERSISTENCE_VOLUME_TYPE`为"nfs3"或"nfs4则必填,指定nfs服务器上的路径,比如`:/var/docker-nfs`
+ SPAWNER_PERSISTENCE_NFS_OPTS: 选填,如果`SPAWNER_PERSISTENCE_VOLUME_TYPE`为"nfs3"或"nfs4则生效,nfs3时默认值为`,rw,vers=3,nolock,soft`;nfs4时默认值为`,rw,nfsvers=4,async`,指定nfs连接的配置项
+ SPAWNER_PERSISTENCE_CIFS_HOST: 如果`SPAWNER_PERSISTENCE_VOLUME_TYPE`为cifs则必填,指定cifs服务器的地址,比如`uxxxxx.your-server.de`
+ SPAWNER_PERSISTENCE_CIFS_DEVICE: 如果`SPAWNER_PERSISTENCE_VOLUME_TYPE`为cifs则必填,指定cifs服务器上的路径,比如`//uxxxxx.your-server.de/backup`
+ SPAWNER_PERSISTENCE_CIFS_OPTS:  选填,如果`SPAWNER_PERSISTENCE_VOLUME_TYPE`为cifs则生效,默认值为`,file_mode=0777,dir_mode=0777`
+ SPAWNER_CPU_LIMIT: 默认`2`,指定notebook容器最大可使用的cpu资源量
+ SPAWNER_CPU_GUARANTEE: 默认`1`,指定notebook容器最低使用的cpu资源量
+ SPAWNER_MEM_LIMIT: 默认`4G`,指定notebook容器最大可使用的内存资源量
+ SPAWNER_MEM_GUARANTEE: 默认`1G`,指定notebook容器最小可使用的内存资源量
+ SPAWNER_ENVIRONMENT: 选填,使用`A:1;B:2`这样的形式指定notebook容器的环境变量
+ SPAWNER_ENDPOINT_MODE: 选填,只能是`vip`或`dnsrr`之一,设置服务的网络访问和负载均衡方式
+ SPAWNER_SPAWN_CMD: 默认`start-singleuser.sh`,指定notebook容器的启动执行命令
+ SPAWNER_REMOVE: 默认`True`,Spawner容器在程序停止后是否删除容器,注意为true时没有保存在对应volume中的数据会丢失
+ SPAWNER_DEBUG: 默认`True`,Spawner容器设为debug模式
+ SPAWNER_CONSECUTIVE_FAILURE_LIMIT: 默认0,Spawner关闭与hub连接前允许的最大故障数,0表示不限制
+ SPAWNER_POLL_INTERVAL: 默认30, 轮询Spawner的间隔,单位s
+ SPAWNER_START_TIMEOUT: 默认120,单用户容器启动最大等待时间,单位s
+ SPAWNER_USE_GPUS: 选填,默认不使用spawner对应的容器是否默认需要使用gpu,使用几个gpu,可以为正整数或为-1或者all,也可以使用`device_id=xxx`指定使用的gpu设备号
+ SPAWNER_CONSTRAINTS: 选填,spawner对应的容器的部署位置限制,以`,`隔开限制
+ SPAWNER_PREFERENCE: 选填,spawner对应的容器的部署优先策略,以`,`隔开策略,每条策略形式为`策略:标签`
+ SPAWNER_PLATFORM: 选填,spawner对应的容器部署的平台限制,以`,`隔开限制,每条限制形式为`arch:os`
+ SPAWNER_CONSTRAINT_IMAGES: 选填,有值则生效,根据用户名的后缀确定部署镜像和限制,形式如`后缀1[:限制1,限制2,...]->镜像名1;后缀2[:限制3,限制4...]->镜像名2...`当登录用户用户名有后缀`-后缀1`时会使用镜像1而非默认镜像构造容器,部署时如果有设置限制则也会增加限制
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
version: "3.8"
services:
    proxy:
        image: jupyterhub/configurable-http-proxy:4.5
        networks:
            - jupyterhub_network
        ports:
            - mode: host
              protocol: tcp
              published: 8001
              target: 8000
        environment:
            CONFIGPROXY_AUTH_TOKEN: abc123
        command:
            - configurable-http-proxy
            - "--error-target"
            - "http://jupyterhub/hub/error"

        deploy:
            mode: global
            placement:
                constraints:
                    - node.hostname==RaspPiNode1
            resources:
                limits:
                    cpus: '1.0'
                    memory: 500M
                reservations:
                    cpus: '0.1'
                    memory: 10M
            restart_policy:
                condition: on-failure
                delay: 5s
                max_attempts: 3
                window: 100s
        
    jupyterhub:
        image: hsz1273327/jupyterhub-for-swarm:4.0.1
        hostname: jupyterhub
        container_name: jupyterhub
        networks:
            - jupyterhub_network
        volumes:
            - "/var/run/docker.sock:/var/run/docker.sock"
            - "jupyterhub-data:/data"
        environment:
            PROXY_SHOULD_START: "False"
            PROXY_API_URL: http://proxy:8001
            CONFIGPROXY_AUTH_TOKEN: abc123
            HUB_DB_URL: "postgresql://postgres:postgres@pghost:5433/jupyterhub"
            SPAWNER_NETWORK_NAME: jupyterhub_network
            SPAWNER_NOTEBOOK_IMAGE: hsz1273327/small-dataset-notebook:notebook-6.5.4
            SPAWNER_CONSTRAINTS: "node.role==manager"
            SPAWNER_ENDPOINT_MODE: dnsrr

            SPAWNER_CONSTRAINT_IMAGES: "base:calculation_type==cpu->jupyter/base-notebook:notebook-6.5.4;torch:calculation_type==gpu->hsz1273327/gpu-torch-notebook:pytorch2.0.1-cuda11.8.0-notebook6.5.4"
            SPAWNER_CONSTRAINT_WITH_GPUS: "torch->1"
            SPAWNER_PERSISTENCE_VOLUME_TYPE: "nfs3"
            SPAWNER_PERSISTENCE_NFS_HOST: xxxxx.nas.aliyuncs.com # nas的host
            SPAWNER_PERSISTENCE_NFS_DEVICE: ":/nas/jupyterhub/{username}"
            SPAWNER_PERSISTENCE_NFS_OPTS: ",vers=3,nolock,hard"
        deploy:
            endpoint_mode: dnsrr
            mode: replicated
            replicas: 1
            placement:
                constraints:
                    - node.role==manager
            resources:
                limits:
                    cpus: '2.0'
                    memory: 500M
                reservations:
                    cpus: '0.1'
                    memory: 10M
            restart_policy:
                condition: on-failure
                delay: 5s
                max_attempts: 3
                window: 100s

volumes:
    jupyterhub-data:

networks:
    jupyterhub_network:
        external: true
```