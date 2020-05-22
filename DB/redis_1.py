# pip install redis -i https://pypi.tuna.tsinghua.edu.cn/simple some-package

import redis
# 创建redis连接池
pool = redis.ConnectionPool(
    host="localhost",
    port=6379,
    password="abc123456",
    db=0,
    max_connections=20
)

r = redis.Redis(
    connection_pool=pool
)

# 创建与关闭连接