from langchain.tools import tool
from typing import List

@tool
def generate_interview_questions(jd_skills: list, lack_skills: list) -> List[str]:
    """
    根据岗位技能+薄弱缺口生成面试题+回答思路
    参数：
        jd_skills：岗位全部技能
        lack_skills：个人欠缺技能
    返回：面试题目+答题思路列表
    """
    from dotenv import load_dotenv
    import os
    from langchain_openai import ChatOpenAI
    load_dotenv()
    llm = ChatOpenAI(api_key=os.getenv("LLM_API_KEY"), base_url=os.getenv("LLM_BASE_URL"), model=os.getenv("LLM_MODEL_NAME"))

    prompt = f"""
    岗位核心技能：{jd_skills}
    个人薄弱技能：{lack_skills}
    生成5道数据分析/大模型应用岗面试题，每道题附带简短答题思路
    """
    res = llm.invoke(prompt)
    return res.content.split("\n")