# profiteer

## 1. 项目介绍

一个无聊的项目，还不知道做什么


## 2. 项目结构

* 对内提供RPC用户基础服务接口
* 对外暴露HTTP接口


## 3. 异步化

> 在服务中，异步化主要分布在两个地方， 一个是 Dispatcher 处，使用`gevent.pool`限流; 另一个是在model层，异步化处理数据库操作，业务handler无需考虑是否异步。

* rpc服务在 Dispatcher 使用`gevent`的`pool.spawn`限制同时处理的客户端请求数，与数据库连接池数量一致，可以稍比数据库连接池数量小, 且必须指定超时时间

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
