from dashscope import Generation
from http import HTTPStatus
from config import API_KEY, MODEL


def llm_chat(prompt:str,sys_prompt:str=None)-> str:
    """
        通用LLM问答函数：RAG拼接上下文回答问题用
        :param prompt: 用户提问+检索到的知识库上下文
        :param sys_prompt: 系统角色提示词，不传默认RAG严格约束
        :return: 大模型返回文本
        """
    # RAG固定强约束系统提示词【关键改这里，杜绝幻觉】
    rag_sys = """你是知识库专属问答助手，硬性执行以下5条规则：
1、**只允许使用用户给出的参考资料内容作答，严禁使用你自身预训练知识库、不能额外科普、不能补充原文不存在的释义**；
2、资料写什么就答什么，禁止自行扩展知识点；
3、参考资料无对应内容，固定回复：【知识库无相关内容】；
4、回答精简，不冗余废话；
5、绝对不能编造信息。"""
    # 外部不传sys_prompt就用上面RAG规则
    if sys_prompt is None:
        sys_prompt = rag_sys

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": prompt}
    ]
    resp = Generation.call(
        api_key=API_KEY,
        model=MODEL,
        messages=messages,
        result_format="message"
    )
    if resp.status_code == HTTPStatus.OK:
        return resp.output.choices[0].message.content.strip()
    else:
        # 报错直接返回错误信息，方便调试
        err = f"LLM调用失败:{resp.code}:{resp.message}"
        print(err)
        return err
