import webbrowser
from flask import Flask, request, Response, send_from_directory
from flask_cors import CORS
from core_rag import SimpleRAG
from pdf_parse import extract_pdf

# --------------------------
# 全局只初始化 1 次
# --------------------------
rag = SimpleRAG()

print("正在解析 PDF...")
knowledge = extract_pdf("tests/MLbook.pdf", end=5)
rag.add_doc(knowledge)
print("✅ 知识库加载完成！")

# --------------------------
# Flask 服务
# --------------------------
app = Flask(__name__)
CORS(app)

# 根路由，防止 404
@app.route("/")
def index():
    return send_from_directory(".", "ui.html")

# 问答接口
@app.route("/ask", methods=["POST"])
def ask():
    question = request.json["question"]
    answer = rag.query(question)
    return Response(answer, content_type="text/plain; charset=utf-8")

# --------------------------
# 关键：debug=False
# --------------------------
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8080")
    # 关键：关闭 debug，防止重复解析！
    app.run(host="127.0.0.1", port=8080, debug=False, threaded=True)