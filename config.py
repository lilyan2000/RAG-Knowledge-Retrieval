import os
from dotenv import load_dotenv

#加载密钥...
load_dotenv()
API_KEY = os.getenv("DASHSCOPE_API_KEY")
MODEL=os.getenv("QWEN_LLM_MODEL")
QWEN_VISION_MODEL=os.getenv("QWEN_VISION_MODEL")


