from langchain.tools import tool
from typing import List

@tool
def extract_jd_skills(jd_text: str) -> List[str]:
    """
    抽取招聘JD里全部技能要求，返回结构化技能列表
    参数：
        jd_text: 招聘岗位JD完整文本
    返回：
        岗位需要的技能字符串列表
    """
    prompt = f"""
    提取下面招聘JD里所有技术技能、硬性要求，只输出纯列表，不要多余文字
    JD内容：{jd_text}
    """
    from dotenv import load_dotenv
    import os
    from langchain_openai import ChatOpenAI
    load_dotenv()
    llm = ChatOpenAI(api_key=os.getenv("LLM_API_KEY"), base_url=os.getenv("LLM_BASE_URL"), model=os.getenv("LLM_MODEL_NAME"))
    result = llm.invoke(prompt)
    # 简单处理转为列表
    skill_list = [i.strip() for i in result.content.split("\n") if i.strip()]
    return skill_list