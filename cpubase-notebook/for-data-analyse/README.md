# 小规模数据处理使用的镜像

数据来源限定为pg,mysql和s3协议的对象存储.本镜像提供如下包:

>基础工具

+ cython
+ lxml

> 数据获取

+ peewee(pymsql,pg)
+ SQLAlchemy(pymsql,pg)
+ boto3
+ s3fs

> 格式支持

+ fastparquet
+ pyarrow
+ fastavro

> 数据可视化

+ matplotlib
+ seaborn

> 表格结构

+ pandas

> 数据检测处理

+ thefuzz
+ pyod

> 分词

+ jieba

> 基本算法工具

+ scipy
+ scikit-learn
+ sympy
+ mpmath
+ xgboost
+ lightgbm
+ catboost

> 时间序列算法

+ skforecast

> 统计

+ statsmodels
+ pingouin
