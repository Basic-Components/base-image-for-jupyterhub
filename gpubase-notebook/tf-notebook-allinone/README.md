# tf-notebook-allinone

使用[nvidia/cuda](https://hub.docker.com/r/nvidia/cuda)作为基镜像,安装了tensorflow的notebook镜像

本镜像除了tensorflow外还提供如下包:

>基础工具

+ cython
+ lxml

> 数据获取

+ peewee
+ SQLAlchemy
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

> 图计算

+ networkx

> 图像算法

+ scikit-image
+ opencv-python
+ Pillow

> 大数据计算

+ dask
