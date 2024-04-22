import pymongo
import json

# 连接到 MongoDB 服务器
client = pymongo.MongoClient("mongodb://localhost:27017/")

# `指定数据库
db = client["bookstore"]

# 指定集合
collection = db["book"]

# 读取 JSON 文件
with open("E:\\大二下\\数据库系统\\第一次大作业\\allsturead\\book_lx.json", "r") as file:
    data = json.load(file)

# 将数据插入到集合中
collection.insert_many(data)

print("导入完成")
