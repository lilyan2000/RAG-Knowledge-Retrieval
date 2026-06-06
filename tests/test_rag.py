from core_rag import SimpleRAG

def test_rag():
    rag = SimpleRAG()
    rag.add_doc("机器学习包含线性回归、决策树算法")
    ans = rag.query("什么是机器学习？")
    print("回答:", ans)

if __name__ == "__main__":
    test_rag()