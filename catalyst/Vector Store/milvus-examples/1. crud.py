from pymilvus import MilvusClient
import numpy as np

client = MilvusClient("./milvus_demo.db")
client.create_collection(
    collection_name="demo_collection",
    dimension=384  # The vectors we will use in this demo has 384 dimensions
)

# Text strings to search from.
docs = [
    "Artificial intelligence was founded as an academic discipline in 1956.",
    "Alan Turing was the first person to conduct substantial research in AI.",
    "Born in Maida Vale, London, Turing was raised in southern England.",
]

'''
For illustration, here we use fake vectors with random numbers (384 dimension).

np.random.uniform(-1, 1)：生成一个在 -1 到 1 之间的随机浮点数。

for _ in range(384)：生成一个包含 384 个随机数的列表，每个随机数在 -1 到 1 之间。

for _ in range(len(docs))：为 docs 中的每个文本生成一个这样的 384 维向量。

最终, vectors 部分为每个文本生成了一个 384 维的随机向量，通常这些向量是通过某种嵌入模型（如 BERT、Word2Vec 等）生成的，但这里为了示例使用了随机数。
'''
vectors = [[ np.random.uniform(-1, 1) for _ in range(384) ] for _ in range(len(docs)) ]
data = [ {"id": i, "vector": vectors[i], "text": docs[i], "subject": "history"} for i in range(len(vectors)) ]
res = client.insert(
    collection_name="demo_collection",
    data=data
)

# This will exclude any text in "history" subject despite close to the query vector.
res = client.search(
    collection_name="demo_collection",
    data=[vectors[0]],
    filter="subject == 'history'",
    limit=2,
    output_fields=["text", "subject"],
)
print(res)
print("*" * 10)

# a query that retrieves all entities matching filter expressions.
res = client.query(
    collection_name="demo_collection",
    filter="subject == 'history'",
    output_fields=["text", "subject"],
)
print(res)
print("*" * 10)


# delete
res = client.delete(
    collection_name="demo_collection",
    filter="subject == 'history'",
)
print(res)