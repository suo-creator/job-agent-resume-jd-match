from langchain.tools import tool
from typing import Dict

@tool
def resume_match_score(resume_content: str, jd_skills: list) -> Dict:
    """
    对比简历内容和JD技能列表，计算匹配分数、区分已掌握/缺失技能
    参数：
        resume_content：个人简历文本
        jd_skills：JD抽取出来的技能列表
    返回：
        字典：score总分、match_skills已掌握、lack_skills缺失技能
    """
    from dotenv import load_dotenv
    import os
    from langchain_openai import ChatOpenAI
    load_dotenv()
    llm = ChatOpenAI(api_key=os.getenv("LLM_API_KEY"), base_url=os.getenv("LLM_BASE_URL"), model=os.getenv("LLM_MODEL_NAME"))

    prompt = f"""
    简历内容：{resume_content}
    岗位需要技能：{jd_skills}
    要求：
    1. 计算0-100匹配总分
    2. 列出简历已经具备的技能
    3. 列出简历欠缺的技能
    严格按照json格式返回，key：score(int)、match_skills(list)、lack_skills(list)
    """
    resp = llm.invoke(prompt)
    import json
    data = json.loads(resp.content)
    return data