# Milvus
Milvus 是一个查询比较高效的向量数据库，开源版支持很好的私有性，适合私有化场景，还具备分布式扩展能力，将来的扩展性很好。

向量数据库本质上和传统数据库没有什么差别，也可以存储传统数据库的信息，只是为了方便将来做向量查询，需要对查询字段做向量存储。

Milvus 数据库的 Collection 就相当于传统数据库的表，因为 Milvus 数据库是非结构化的，因此可以把产品信息分成若干段结构存入Milvus。


示例：
```python
import configparser
import time
from pymilvus import connections, utility, Collection, DataType, FieldSchema, CollectionSchema
from transformers import BertModel, BertTokenizer
import torch


if __name__ == '__main__':
    # 连接到 Milvus
    cfp = configparser.RawConfigParser()
    cfp.read('config.ini')
    milvus_uri = cfp.get('example', 'uri')
    token = cfp.get('example', 'token')
    connections.connect("default",
                        uri=milvus_uri,
                        token=token)
    print(f"Connecting to DB: {milvus_uri}")


    # 检查集合是否存在
    collection_name = "product_info"
    
    # 定义集合的 schema
    dim = 64  # 向量的维度
    product_id_field = FieldSchema(name="product_id", dtype=DataType.INT64, is_primary=True, description="产品ID")
    product_name_field = FieldSchema(name="product_name_vector", dtype=DataType.FLOAT_VECTOR, dim=dim, description="产品名称向量")
    model_number_field = FieldSchema(name="model_number", dtype=DataType.VARCHAR, max_length=50, description="产品型号")
    features_field = FieldSchema(name="features", dtype=DataType.VARCHAR, max_length=1000, description="核心特点")
    tech_specs_field = FieldSchema(name="tech_specs", dtype=DataType.VARCHAR, max_length=1000, description="技术参数")
    target_market_field = FieldSchema(name="target_market", dtype=DataType.VARCHAR, max_length=1000, description="目标市场")
    promotion_strategy_field = FieldSchema(name="promotion_strategy", dtype=DataType.VARCHAR, max_length=1000, description="促销策略")


    schema = CollectionSchema(fields=[
        product_id_field,
        product_name_field,
        model_number_field,
        features_field,
        tech_specs_field,
        target_market_field,
        promotion_strategy_field
    ], auto_id=False, description="产品信息集合")
    
    print(f"Creating collection: {collection_name}")
    collection = Collection(name=collection_name, schema=schema)
    print(f"Schema: {schema}")
    print("Success!")


    # 产品信息
    product_name = "AirPure Pro 智能空气净化器"
    product_name_vector = generate_vector_from_text(product_name, dim)
    
    product_ids = [1]
    product_name_vectors = [product_name_vector]
    model_numbers = ["AP5000"]
    features = ["四层过滤系统: 高效的四层过滤，包括初效滤网、活性炭滤网、HEPA滤网和负离子发生器，能够去除99.97%的空气污染物。空气质量检测传感器: 内置的高精度传感器实时监测空气中的PM2.5、甲醛、二氧化碳等有害物质，显示在LCD屏幕上，并自动调整净化模式。智能控制: 支持Wi-Fi连接，用户可通过专属手机App远程查看空气质量报告、设置定时开关机、调整净化速度等。节能与静音: 采用超静音风扇设计，夜间模式下噪音低至20分贝，并具备节能模式，自动调节风速以减少电能消耗。滤网寿命提示: 内置滤网更换提醒功能，根据使用情况智能提示滤网更换时间，确保净化效果最佳。"]
    tech_specs = ["适用面积: 60-80平方米, CADR值: 500立方米/小时, 噪音水平: 20-50分贝, 功率: 45W"]
    target_markets = ["城市家庭，特别是有婴幼儿、老人或宠物的家庭，关注室内空气质量的用户，如过敏患者、呼吸道疾病患者"]
    promotion_strategies = ["新用户优惠: 首次购买享受20%折扣, 赠品: 赠送一年的替换滤网, 推荐奖励: 推荐朋友购买可获得额外优惠券"]


    entities = [
        product_ids,
        product_name_vectors,
        model_numbers,
        features,
        tech_specs,
        target_markets,
        promotion_strategies
    ]


    print("Inserting entities...")
    t0 = time.time()
    collection.insert(entities)
    total_rt = time.time() - t0
    print(f"Succeed in {round(total_rt, 4)} seconds!")
    
    ... ...
    # 断开连接
    connections.disconnect("default")
```