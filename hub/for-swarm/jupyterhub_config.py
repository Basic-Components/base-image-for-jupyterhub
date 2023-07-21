"""jupyterhub的配置项

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

+ SPAWNER_NOTEBOOK_IMAGE: 默认值`jupyter/base-notebook:notebook-6.5.4`,指定SPAWNER拉起作为notebook执行器的容器使用的镜像
+ SPAWNER_PULL_POLICY: 默认值`ifnotpresent`,枚举类型,指定拉取NOTEBOOK_IMAGE使用的策略,可选的有:
    + `ifnotpresent`-如果没有就拉取
    + `always`-总是检查更新并拉取
    + `never`- 总是不拉取,如果本地没有就抛出错误
    + `skip`- 总是不拉取,但也不抛出错误
+ SPAWNER_NETWORK_NAME: 必填,指定使用的docker network名
+ SPAWNER_NOTEBOOK_DIR: 默认`/home/jovyan/work`,指定notebook容器中notebook存放路径,不建议修改
+ SPAWNER_PERSISTENCE_VOLUME_TYPE: 默认`local`,notebook服务保存的文件存放的位置类型,支持"local", "nfs3", "nfs4", "cifs"四种类型
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
+ SPAWNER_USE_GPUS: 选填,spawner对应的容器是否需要使用gpu,使用几个gpu,可以为正整数或为-1或者all,也可以使用`device_id=xxx`指定使用的gpu设备号
+ SPAWNER_CONSTRAINTS: 选填,spawner对应的容器的部署位置限制,以`,`隔开限制
+ SPAWNER_PREFERENCE: 选填,spawner对应的容器的部署优先策略,以`,`隔开策略,每条策略形式为`策略:标签`
+ SPAWNER_PLATFORM: 选填,spawner对应的容器部署的平台限制,以`,`隔开限制,每条限制形式为`arch:os`

> AUTH设置

+ AUTH_ADMIN_USER: 默认`admin`,指定admin用户的用户名,多个用`,`隔开
+ AUTH_CHECK_COMMON_PASSWORD: 默认`False`,是否启用复杂密码校验
+ AUTH_MINIMUM_PASSWORD_LENGTH: 默认`6`,密码长度校验
+ AUTH_ALLOWED_FAILED_LOGINS: 默认`3`,最大登录错误次数
+ AUTH_SECONDS_BEFORE_NEXT_TRY: 默认`1200`,重试最长间隔时间
+ AUTH_ENABLE_SIGNUP: 默认`True`,是否开放新用户注册
+ AUTH_OPEN_SIGNUP: 默认`False`,是否允许用户注册后未经管理员确认就可以进入使用
"""
import os
import copy

c = get_config()   # noqa: F821

# proxy设置
proxy_should_start = True if os.environ.get("PROXY_SHOULD_START", "TRUE").lower() in ("true", "1", "ok") else False
c.ConfigurableHTTPProxy.should_start = proxy_should_start
if not proxy_should_start:
    proxy_api_url = os.environ.get("PROXY_API_URL")
    if not proxy_api_url:
        raise AttributeError(f"need to set PROXY_API_URL")
    c.ConfigurableHTTPProxy.api_url = proxy_api_url
    CONFIGPROXY_AUTH_TOKEN = os.environ.get("CONFIGPROXY_AUTH_TOKEN")
    if not CONFIGPROXY_AUTH_TOKEN:
        raise AttributeError(f"need to set CONFIGPROXY_AUTH_TOKEN")
    c.ConfigurableHTTPProxy.auth_token = CONFIGPROXY_AUTH_TOKEN

# hub部分配置
# hub的内网端口
c.JupyterHub.hub_port = int(os.environ.get("HUB_HUB_PORT", '8001'))
# 指定hub的内网host
c.JupyterHub.hub_connect_ip = os.environ.get("HUB_CONNECT_IP", 'jupyterhub')
# 指定hub对外的端口
c.JupyterHub.port = int(os.environ.get("HUB_PORT", '8000'))
# hub的启动坚定host
c.JupyterHub.hub_ip = '0.0.0.0'
# 启动时使用https协议
hub_ssl_key = os.environ.get("HUB_SSL_KEY")
hub_ssl_cert = os.environ.get("HUB_SSL_CERT")
if hub_ssl_key and hub_ssl_cert:
    c.JupyterHub.ssl_key = hub_ssl_key
    c.JupyterHub.ssl_cert = hub_ssl_cert

# 设置hub的cookie_secret数据的存储
c.JupyterHub.cookie_secret_file = os.environ.get("HUB_COOKIE_SECRET_FILE", "/data/jupyterhub_cookie_secret")
# 指定数据库路径
c.JupyterHub.db_url = os.environ.get("HUB_DB_URL", "sqlite:////data/jupyterhub.sqlite")
# 指定挂载spawner服务的最大数量,超过这个数量后hub服务将不会启动新的spawner服务,通常一个用户绑定一个spawner服务
c.JupyterHub.active_server_limit = int(os.environ.get("HUB_ACTIVE_SERVER_LIMIT", "100"))
# 活跃用户总数的检查间隔时间,单位s
c.JupyterHub.active_user_window = int(os.environ.get("HUB_ACTIVE_USER_WINDOW", "1800"))
# 活跃用户状态刷新间隔时间,单位s,这个参数用于限制状态写入的频率
c.JupyterHub.activity_resolution = int(os.environ.get("HUB_ACTIVITY_RESOLUTION", "30"))
# 同时并发的spawn数量最大值
c.JupyterHub.concurrent_spawn_limit = int(os.environ.get("HUB_CONCURRENT_SPAWN_LIMIT", "20"))
# 内部通信启用ssl
hub_internal_ssl_path = os.environ.get('HUB_INTERNAL_SSL_PATH')
if hub_internal_ssl_path:
    c.JupyterHub.internal_ssl = True
    c.JupyterHub.internal_certs_location = hub_internal_ssl_path

# spawner初始化最大时长
c.JupyterHub.init_spawners_timeout = int(os.environ.get("HUB_INIT_SPAWNERS_TIMEOUT", "60"))

# 设置Spawner
# 指定使用docker spawner
c.JupyterHub.spawner_class = "dockerspawner.SwarmSpawner"
# 指定Spawner容器使用的镜像
c.DockerSpawner.image = os.environ.get("SPAWNER_NOTEBOOK_IMAGE", 'jupyter/base-notebook:notebook-6.5.4')
# 指定镜像的拉取模式,可选的有
# + `ifnotpresent`-如果没有就拉取
# + `always`-总是检查更新并拉取
# + `never`- 总是不拉取,如果本地没有就抛出错误
# + `skip`- 总是不拉取,但也不抛出错误
c.SwarmSpawner.pull_policy = os.environ.get("SPAWNER_PULL_POLICY", 'ifnotpresent')
# 指定Spawner容器使用内部网络
c.SwarmSpawner.use_internal_ip = True
# 指定网络Spawner容器连接的网络,必须从环境变量指定
network_name = os.environ["SPAWNER_NETWORK_NAME"]
if network_name:
    c.SwarmSpawner.network_name = network_name
else:
    raise AttributeError("need to set environ DOCKER_NETWORK_NAME")
# 设置Spawner容器存储
notebook_dir = os.environ.get('SPAWNER_NOTEBOOK_DIR', '/home/jovyan/work')
c.SwarmSpawner.notebook_dir = notebook_dir
# 设置容器存储的位置,支持local,nfs3,nfs4,cifs
supported_volume_types = ["local", "nfs3", "nfs4", "cifs"]
spawner_volume_type = os.environ.get('SPAWNER_PERSISTENCE_VOLUME_TYPE', 'local')

if spawner_volume_type not in supported_volume_types:
    raise AttributeError(f"need to set SPAWNER_PERSISTENCE_VOLUME_TYPE in {supported_volume_types}")
if spawner_volume_type == "local":
    mounts = [
        {
            "type": "volume",
            "target": notebook_dir,
            "source": "jupyterhub-user-{username}",
            "no_copy": True
        }
    ]
else:
    if spawner_volume_type in ("nfs3", "nfs4"):
        spawner_nfs_host = os.environ.get('SPAWNER_PERSISTENCE_NFS_HOST')
        spawner_nfs_device = os.environ.get('SPAWNER_PERSISTENCE_NFS_DEVICE')
        if not all([spawner_nfs_host, spawner_nfs_device]):
            raise AttributeError("need to set SPAWNER_PERSISTENCE_NFS_HOST and SPAWNER_PERSISTENCE_NFS_DEVICE")
        if not spawner_nfs_device.startswith(":"):
            spawner_nfs_device = ":" + spawner_nfs_device
        if spawner_volume_type == "nfs3":
            spawner_nfs_opts = os.environ.get("SPAWNER_PERSISTENCE_NFS_OPTS", ",rw,vers=3,nolock,soft")
        else:
            spawner_nfs_opts = os.environ.get("SPAWNER_PERSISTENCE_NFS_OPTS", ",rw,nfsvers=4,async")
        if not spawner_nfs_opts.startswith(","):
            spawner_nfs_opts = "," + spawner_nfs_opts
        mounts = [
            {
                "type": "volume",
                "target": notebook_dir,
                "source": "jupyterhub-user-{username}",
                "no_copy": True,
                "driver_config": {
                    'name': 'local',
                    'options': {
                        'type': 'nfs',
                        'o': 'addr=' + spawner_nfs_host + spawner_nfs_opts,
                        'device': spawner_nfs_device
                    }
                }
            }
        ]
    else:
        spawner_cifs_host = os.environ.get('SPAWNER_PERSISTENCE_CIFS_HOST')
        spawner_cifs_device = os.environ.get('SPAWNER_PERSISTENCE_CIFS_DEVICE')
        if not all([spawner_cifs_host, spawner_cifs_device]):
            raise AttributeError("need to set SPAWNER_PERSISTENCE_CIFS_HOST and SPAWNER_PERSISTENCE_CIFS_DEVICE")
        spawner_cifs_opts = os.environ.get("SPAWNER_PERSISTENCE_CIFS_OPTS", ",file_mode=0777,dir_mode=0777")
        if not spawner_cifs_opts.startswith(","):
            spawner_cifs_opts = "," + spawner_cifs_opts
        mounts = [
            {
                "type": "volume",
                "target": notebook_dir,
                "source": "jupyterhub-user-{username}",
                "no_copy": True,
                "driver_config": {
                    'name': 'local',
                    'options': {
                        'type': 'nfs',
                        'o': 'addr=' + spawner_cifs_host + spawner_cifs_opts,
                        'device': spawner_cifs_device
                    }
                }
            }
        ]

    def spawner_start_hook(spawner):
        # username = spawner.user.name
        print("spawner_start_hook start")
        mounts = []
        old_mounts = spawner.extra_container_spec.get("mounts")
        if old_mounts:
            for mount in old_mounts:
                new_mount = copy.deepcopy(mount)
                device = spawner.format_volume_name(mount["driver_config"]["options"]["device"], spawner)
                new_mount["driver_config"]["options"]["device"] = device
                mounts.append(new_mount)
            spawner.mounts = mounts
            print("spawner_start_hook format device name ok")
        print("spawner_start_hook ok")

    c.Spawner.pre_spawn_hook = spawner_start_hook

c.SwarmSpawner.extra_container_spec = {
    'mounts': mounts
}
# 限制cpu数
c.SwarmSpawner.cpu_limit = float(os.environ.get('SPAWNER_CPU_LIMIT', '2'))
# 限制cpu最低使用量
c.SwarmSpawner.cpu_guarantee = float(os.environ.get('SPAWNER_CPU_GUARANTEE', '1'))

# 限制容器内存
c.SwarmSpawner.mem_limit = os.environ.get('SPAWNER_MEM_LIMIT', '4G')
# 最低容器内存
c.SwarmSpawner.mem_guarantee = os.environ.get('SPAWNER_MEM_GUARANTEE', '1G')
# 容器的环境变量设置,使用`A:1;B:2`这样的形式
SwarmSpawner_environment = os.environ.get('SPAWNER_ENVIRONMENT')
if SwarmSpawner_environment:
    c.SwarmSpawner.environment = {i.split(":")[0].strip(): i.split(":")[1].strip() for i in SwarmSpawner_environment.split(";") if i.strip()}
# 访问和负载均衡模式
support_endpoint_modes = ["vip", "dnsrr"]
swarmspawner_endpoint_mode = os.environ.get('SPAWNER_ENDPOINT_MODE')
if swarmspawner_endpoint_mode:
    if swarmspawner_endpoint_mode not in support_endpoint_modes:
        raise AttributeError(f"SPAWNER_ENDPOINT_MODE must in {support_endpoint_modes}")
    else:
        c.SwarmSpawner.extra_endpoint_spec = {
            "mode": swarmspawner_endpoint_mode
        }

# 容器启动命令
c.SwarmSpawner.cmd = os.environ.get("SPAWNER_SPAWN_CMD", "start-singleuser.sh")

# Spawner service在程序停止后删除容器
c.DockerSpawner.remove = True if os.environ.get("SPAWNER_REMOVE", "True").lower() in ("true", "1", "ok") else False
# Spawner service设为debug模式
c.SwarmSpawner.debug = True if os.environ.get("SPAWNER_DEBUG", "True").lower() in ("true", "1", "ok") else False
# Spawner关闭与hub连接前允许的最大故障数,0表示不限制
c.SwarmSpawner.consecutive_failure_limit = int(os.environ.get("SPAWNER_CONSECUTIVE_FAILURE_LIMIT", "0"))
# 轮询Spawner的间隔,单位s
c.SwarmSpawner.poll_interval = int(os.environ.get("SPAWNER_POLL_INTERVAL", "30"))
# dockerservice启动最大等待时间
c.SwarmSpawner.start_timeout = int(os.environ.get("SPAWNER_START_TIMEOUT", "120"))
# dockerservice启动的时候是否要使用gpu,使用几个gpu,如果不填则表示不使用gpu
SwarmSpawner_use_gpus = os.environ.get("SPAWNER_USE_GPUS", "").lower()
if SwarmSpawner_use_gpus:
    SwarmSpawner_use_gpus_count = 0
    SwarmSpawner_use_gpus_device_id = ""
    _use_gpus = False
    if SwarmSpawner_use_gpus == "all":
        SwarmSpawner_use_gpus_count = -1
        _use_gpus = True
    elif SwarmSpawner_use_gpus.isdigit():
        DockerSpawner_use_gpus_count = int(SwarmSpawner_use_gpus)
        _use_gpus = True
    elif SwarmSpawner_use_gpus.startswith("device_id="):
        SwarmSpawner_use_gpus_device_id = SwarmSpawner_use_gpus.replace("device_id=", "").strip()
        _use_gpus = True
    if _use_gpus:
        if DockerSpawner_use_gpus_count != 0:
            c.SwarmSpawner.extra_resources_spec = {
                "generic_resources": {
                    'gpu': DockerSpawner_use_gpus_count
                }
            }
        else:
            c.SwarmSpawner.extra_resources_spec = {
                "generic_resources": {
                    'gpu': SwarmSpawner_use_gpus_device_id
                }
            }
# 指定docker service的部署位置策略
SwarmSpawner_constraints = os.environ.get('SPAWNER_CONSTRAINTS')
SwarmSpawner_preferences = os.environ.get('SPAWNER_PREFERENCE')
SwarmSpawner_platforms = os.environ.get('SPAWNER_PLATFORM')
if any([SwarmSpawner_constraints, SwarmSpawner_preferences, SwarmSpawner_platforms]):
    extra_placement_spec: dict[str, list[str | tuple[str, str]]] = {}
    if SwarmSpawner_constraints:
        extra_placement_spec["constraints"] = [i.strip() for i in SwarmSpawner_constraints.split(",")]
    if SwarmSpawner_preferences:
        extra_placement_spec["preferences"] = [(i.strip().split(":")[0].strip(), i.strip().split(":")[1].strip()) for i in SwarmSpawner_preferences.split(",")]
    if SwarmSpawner_platforms:
        extra_placement_spec["platforms"] = [(i.strip().split(":")[0].strip(), i.strip().split(":")[1].strip()) for i in SwarmSpawner_platforms.split(",")]
    c.SwarmSpawner.extra_placement_spec = extra_placement_spec

# 用户认证相关设置
# 指定认证类型
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
# c.JupyterHub.template_paths = [f"{os.path.dirname(nativeauthenticator.__file__)}/templates/"]
# 指定admin用户的用户名,多个用`,`隔开
admins = os.environ.get("AUTH_ADMIN_USER", 'admin')
c.Authenticator.admin_users = set([admin for admin in admins.split(",") if admin.strip()])
# 是否启用复杂密码校验
c.NativeAuthenticator.check_common_password = True if os.environ.get("AUTH_CHECK_COMMON_PASSWORD", 'False').lower() in ("true", "1", "ok") else False
# 密码长度校验
c.NativeAuthenticator.minimum_password_length = int(os.environ.get("AUTH_MINIMUM_PASSWORD_LENGTH", "6"))
# 最大登录错误次数
c.NativeAuthenticator.allowed_failed_logins = int(os.environ.get("AUTH_ALLOWED_FAILED_LOGINS", "3"))
# 重试最长间隔时间
c.NativeAuthenticator.seconds_before_next_try = int(os.environ.get("AUTH_SECONDS_BEFORE_NEXT_TRY", "1200"))
# 是否开放新用户注册
c.NativeAuthenticator.enable_signup = True if os.environ.get("AUTH_ENABLE_SIGNUP", 'True').lower() in ("true", "1", "ok") else False
# 是否允许用户注册后未经管理员确认就可以进入使用
c.NativeAuthenticator.open_signup = True if os.environ.get("AUTH_OPEN_SIGNUP", 'False').lower() in ("true", "1", "ok") else False
