# profiteer

## 1. 项目介绍

一个无聊的项目，还不知道做什么；计划`oath_rpc`提供账号登录、注册和授权服务，`user_rpc`提供用户信息服务


## 2. 项目结构
> 对内提供RPC用户基础服务接口

项目一级目录

| 目录或文件 | 说明 |
| -------- | --- | 
| config   | 环境、数据库等配置 |
| handlers | 具体处理逻辑 |
| libs     | 项目的组件等 |
| models   | 数据库crud  |
| test     | 单元测试    |
| utils    | 全局通用方法 |
| wiki     | 文档       |
| dispacher.py | handler 路由 |
| server.py | 项目启动入口 |

libs 二级目录

| 目录或文件 | 说明 |
| -------- | --- | 
| cache    | Redis client |
| mongo    | mongod client |
| pg       | postgresql client |
| rpc      | 调用\定义 rpc 服务 |

utils 二级目录

| 目录或文件 | 说明 |
| -------- | --- | 
| logger   | log 输出 |

* python 版本使用3.6.5；
* 使用`thriftpy2`提供的rpc框架；
* 使用`gevent`做限流及异步化；
* 使用`SQLAlchemy`的orm做pg数据的crud；
* 使用`pytest`做单元测试
* 数据库使用`postgresql`、`MongoDB`、`Redis`


## 3. 异步化
> 在服务中，异步化主要分布在两个地方， 一个是 Dispatcher 处，使用`gevent.pool`限流; 另一个是在model层，异步化处理数据库操作，业务handler无需考虑是否异步。

* 在 Dispatcher 处使用`gevent`的`pool.spawn`限制同时处理的客户端请求数，与数据库连接池数量一致，可以稍比数据库连接池数量小, 且必须指定超时时间

例：
```python
class Dispatcher(object):
    @classmethod
    def getUser(cls, user_id):
        g = pool.spawn(UserHandler.get, user_id)
        # 设置业务处理函数超时时间
        g.join(timeout=TimeoutLevel)
        return g.get()
```

* model层所有操作均使用`gevent.spawn(==无限制创建协程==)`异步化处理, 对于含有多个数据库查询操作的，异步获取所有结果，然后进行组装。

```python
class User(Base):
    id = Column(Integer)
    ...

    @classmethod
    def _get(cls, user_id):
        session = get_user_session()
        result = session.query(model).filter(model.user_id == user_id).first()
        session.close()
        return result

    @classmethod
    def get(cls, user_id):
        job = gevent.spawn(cls._get, user_id)
        job.join()
        return job.value

    @classmethod
    def gets(cls, user_ids):
        jobs = [gevent.spawn(cls.get, user_id) for user_id in user_ids]
        gevent.joinall(jobs)
        results = [job.value for job in jobs]
        return results
```


## 部署

### 1. 创建配置文件夹，并编辑配置文件
```shell script
cd ~
mkdir ".profiteer"
cd .profiteer
vim config.ini
```

### 2. 将定义好的配置文件加入系统环境变量
```shell script
export PROFITEER_CONFIG_PATH=~/.profiteer/config.ini
```

### 3. 测试rpc服务端启动命令
```shell script
python server.py -H host -P port
```
