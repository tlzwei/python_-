# 使用redis实现商品秒杀
# 利用多线程模拟商品秒杀过程,不可以出现超买超卖情况,10钟后自动结束
# redis是单线程,不存在超买超卖
'''
kill_total 商品总数
till_num 成功批购数
till_flag 有效标志位
kill_user 成功批购用户id
'''

from DB.redis_db import pool
import redis
import random
from concurrent.futures import ThreadPoolExecutor

# 随机生成用户id
s=set()
while 1:
    if len(s)==1000:
        break
    num=random.randint(10000,100000)
    s.add(num)

# 创建redis连接
con=redis.Redis(
    connection_pool=pool
)

try:
    # 清除之前秒杀数据
    con.delete("kill_total","kill_num","till_flag","kill_user")
    # 初始化秒杀
    con.set("kill_total",50)
    con.set("kill_num", 0)
    con.set("till_flag", 1)
    con.expire("kill_flag",60*10)  # 过期时间 10分钟
except Exception as e:
    print(e)
finally:
    del con

# 创建模拟用户
executor = ThreadPoolExecutor(2000)
def buy():
    connection = redis.Redis(
        connection_pool=pool
    )  # 创建连接池
    pipline=connection.pipeline()  # 创建事务

    try:
        if connection.exists("kill_flag")==1:   # 秒杀活动是否已经开启
            pipline.watch("kill_num","kill_user") # 监视数据
            total = int(pipline.get("kill_total").decode("utf-8")) # 商品总数
            num = int(pipline.get("kill_num").decode("utf-8"))  # 成功购买数
            if num < total: # 商品还有,添加用户及购买数+1
                pipline.multi()  # 开启redis事务
                pipline.incr("kill_num")  # +1
                user_id=s.pop()  # 删除元素并返回
                pipline.rpush("kill_user",user_id)
                pipline.execute() # 提交事务
    except Exception as e:
        print(e)
    finally:
        if "pipline" in dir():
            pipline.reset()
        del connection

# 线程池模拟秒杀
for i in range(0,1000):
    executor.submit(buy)

print("秒杀已经结束")
