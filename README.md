# 黄金点游戏-重制版

## 游戏规则

N 个玩家，每人写 **2** 个 **0~100** 之间的有理数 **（不包括 0 或 100 )** ，提交给服务器，服务器在当前回合结束时算出所有数字的 **平均值** ，然后乘以 **0.618**（所谓黄金分割常数），得到 G 值。提交的数字最靠近 G（取绝对值）的玩家得到 **N-2** 分，离 G 最远的玩家得到 **-2** 分，其他玩家得 0 分。

## 设置密钥

```
python3 keygen.py
```

## 部署

```
docker-compose up
```

## 数据库初始化

```
python3 manage.py makemigrations
python3 manage.py migrate
```

## 创建管理员用户

```
python3 manage.py createsuperuser
```
