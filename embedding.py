#文本向量化
from dashscope import TextEmbedding
from config import API_KEY

def get_embedding(text: str):
    resp = TextEmbedding.call(
        api_key=API_KEY,
        model="text-embedding-v3",
        input=text
    )
    return resp.output["embeddings"][0]["embedding"]
