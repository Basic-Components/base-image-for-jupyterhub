# jetson r32使用的tensorflow的notebook

基于镜像[nvcr.io/nvidia/l4t-tensorflow](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-tensorflow)中版本为r32的镜像构造,额外增加notebook功能,并增加如下包:

+ Pillow
+ onnx
+ tf2onnx
+ boto3
+ s3fs
+ psycopg2-binary
+ pymysql
+ peewee
+ SQLAlchemy
+ matplotlib
+ seaborn
+ pandas
+ thefuzz
+ scipy
+ scikit-learn
+ scikit-image
+ jieba
+ transformers
+ datasets

需要注意由于基镜像使用ubuntu 18以及python 3.6,版本较低,因此许多依赖也有版本低的问题.
