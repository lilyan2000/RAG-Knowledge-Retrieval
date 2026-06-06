from dashscope import MultiModalConversation
import base64
import os
from config import API_KEY,QWEN_VISION_MODEL

# 方案1：最简写法【推荐，直接传路径，SDK自动上传】
def describe_image(image_path):
    # 不拼接file://，直接绝对路径
    abs_path = os.path.abspath(image_path)
    resp = MultiModalConversation.call(
        api_key=API_KEY,
        model=QWEN_VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"image": abs_path},
                    {"text": "请详细描述这张图片里的内容"}
                ]
            }
        ]
    )
    if resp.status_code == 200:
        return resp.output.choices[0].message.content
    else:
        return f"错误：{resp.code} -> {resp.message}"
'''
# 方案2：上面还报错就用Base64万能兼容（必过）
def describe_image_base64(image_path):
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    ext = os.path.splitext(image_path)[1].strip(".").lower()
    b64_data = base64.b64encode(img_bytes).decode("utf-8")
    img_data_uri = f"data:image/{ext};base64,{b64_data}"

    resp = MultiModalConversation.call(
        api_key=API_KEY,
        model=QWEN_VISION_MODEL,
        messages=[
            {"role": "user", "content": [{"image": img_data_uri},{"text":"详细描述图片"}]}
        ]
    )
    if resp.status_code == 200:
        return resp.output.choices[0].message.content
    else:
        return f"错误：{resp.code} -> {resp.message}"
'''
# 测试
if __name__ == "__main__":
    # 优先用方案1
    result = describe_image("./test.png")
    print("图片描述：\n", result)