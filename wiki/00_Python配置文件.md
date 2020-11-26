# Python 配置文件

## 1. 将配置写在Python文件里
> 这种方式很简单，写一个例如`conf.py`的文件，使用k=v、字典、类等的形式归类配置项。需要区分开发、测试、线上等环境配置的时候，可以根据启动项目的命令行参数或系统环境变量的不同，来选择不同的配置。

例：
```python
""" 
@file: config/config.py 
"""

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'xxx'


class ProdConfig(Config):
    """
    生产环境配置
    """
    DATABASE_URI = 'xxx'


class DevelopmentConfig(Config):
    """
    开发环境配置
    """
    DEBUG = True


class TestingConfig(Config):
    """
    测试环境配置
    """
    TESTING = True
```

```python
""" 
@file: config/__init__.py
"""

import sys

from config.config import config


if __name__ == '__main__':
    env = sys.argv[1] if len(sys.argv) > 2 else ''

    if env == 'dev':
        CONFIG = config.DevelopmentConfig
    elif env == 'test':
        CONFIG = config.TestingConfig
    elif env == 'prod':
        CONFIG = config.ProdConfig
    else:
        raise ValueError('Invalid environment name')
```

使用
```python
""" 
@file: libs/pg/client.py
"""
from config import CONFIG

print(CONFIG.DATABASE_URI)
```

注意: 配置写在代码中有严重的安全问题


## 2. 使用外部配置文件
> 利用外部的配置文件来存储配置信息，和代码独立开来。使用环境变量来指定配置文件的存放路径，由Python代码来读取配置文件获取配置。配置文件常见格式json、yaml或者ini等。

设置环境变量可以修改profile文件，修改`/etc/profile`文件（对所有用户都是有效的）
```shell script
vi /etc/profile
```

在里面加入:
```
export PROFITEER_CONFIG_PATH=xxx
```

或是修改.bashrc文件：修改`~/.bashrc`文件（每个用户目录下都有，ls -all，单独用户有效）
```shell script
cd ~
vi .bashrc
```

在里面加入：
```shell script
export PROFITEER_CONFIG_PATH=xxx
```

添加完环境变量需要`source`一下修改的文件
```shell script
source .bashrc
```

例：
```ini
""" 
@file: xxx
"""
[PG]
DATABASE_URI=xxx
```

```python
""" 
@file: config/config.py
"""
import os
from configparser import ConfigParser

try:
    CONFIG_PATH = os.environ[str('PROFITEER_CONFIG_PATH')]
except Exception:
    raise ValueError

config = ConfigParser()
config.read(CONFIG_PATH)

DATABASE_URI = config.get(str("PG"), str("DATABASE_URI"))
```


## 3. 直接使用系统环境变量
> 不使用文件来存储配置信息，将所有的配置信息存储到环境变量中，在程序运行前将需要配置信息导入到环境变量中。

例：
```python
""" 
@file: libs/pg/client.py
"""
import os

env_dict = os.environ
print(env_dict.get(str("DATABASE_URI") , ""))
```

注意: 环境变量写入的都是字符串，还要注意避免与系统自带的环境变量冲突，一般加上项目的前缀
