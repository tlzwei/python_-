# 数据库入  mongodb  添删改查

from pymongo import MongoClient
client = MongoClient(host="localhost",port=27017)
# client.admin.authenticate("admin","abc")  # 带密码进入
client = MongoClient()

# from mongo_db import client # 导入数据库

# db = client.teacher
# collection = db.teacher
# result = collection.insert_one({"name":"李路"})  # 添加单条数据



# 插入一条数据

client.school.teacher.insert_one({"name":"aasd"})  # 创建 school数据库 teacher表
# 添加多条记录
client.school.teacher.insert_many([
    {"name": "aaa"},
    {"name": "bbb"},
    {"name": "ccc"},
     ])



# find_one find_  查询

teachers=client.school.teacher.find({})
for one in teachers:
    print(one['_id'],one['name'])

teacher = client.school.teacher.find_one({"name":"aaa"})
print(teacher['_id'],teacher['name'])


# update_one  update_many 数据修改

# {} 查询条件 set 修改  (所有教室都添加一个role字段)
client.school.teacher.update_many(
    {},{"$set":{"role":["班主任"]}}
)
# 查询aaa 修改性别
client.school.teacher.update_many(
    {"name":"aaa"},{"$set":{"role":["班主任"]}}
)
# 添加
client.school.teacher.update_many(
    {"name":"aaa"},{"$push":{"role": "年级主任"}}
)