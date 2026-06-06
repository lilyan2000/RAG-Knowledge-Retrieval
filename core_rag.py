from llm import llm_chat
from embedding import get_embedding
from utils import split_text, cos_sim

class SimpleRAG:
    def __init__(self):
        self.chunks = []   # 存文本块
        self.vecs = []     # 存向量

    # 1. 添加文档 → 切块 → 向量化 → 保存
    def add_doc(self, text):
        chunks = split_text(text)
        for c in chunks:
            vec = get_embedding(c)
            self.chunks.append(c)
            self.vecs.append(vec)


    # 2. 检索最相关的文本
    def retrieve(self, question, top_k=3):
        q_vec = get_embedding(question)
        scores = []

        for i, v in enumerate(self.vecs):
            scores.append((i, cos_sim(q_vec, v)))

        scores.sort(key=lambda x: x[1], reverse=True)
        return [self.chunks[i] for i, _ in scores[:top_k]]


    # 3. 最终提问
    def query(self, question):
        docs = self.retrieve(question)
        if docs:
            print("【检索到了知识库原文】")  # 关键：控制台打印召回内容
        else:
            return "抱歉，知识库中没有找到相关内容，无法回答该问题。"
        context = "\n".join(docs)

        prompt = f"资料：{context}\n问题：{question}\n请根据资料回答"
        return llm_chat(prompt)