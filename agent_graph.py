from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
import operator
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from system_prompt import SYSTEM_PROMPT
from tools.jd_extract import extract_jd_skills
from tools.match_tool import resume_match_score
from tools.interview_tool import generate_interview_questions
from tools.resume_file_parser import parse_resume_file

load_dotenv()

# 1. 定义全局状态结构体：所有字段名全程统一
class AgentState(TypedDict):
    resume_content: str   # 简历纯文本
    jd_content: str       # JD纯文本
    jd_skills: list       # 抽取后的JD技能列表
    match_result: dict    # 匹配打分结果
    interview_content: list  # 生成的面试题列表
    final_report: str     # 最终汇总报告

# 2. 初始化LLM
llm = ChatOpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
    model=os.getenv("LLM_MODEL_NAME")
).bind_tools([parse_resume_file, extract_jd_skills, resume_match_score, generate_interview_questions])

# 3. 定义各个节点函数
def node_parse_resume_file(state: AgentState):
    """兼容模式：前端已传文本就直接跳过，不做文件解析"""
    # 什么都不返回，状态保持原样，避免覆盖字段
    return {}

def node_extract_jd(state: AgentState):
    """节点1：抽取JD技能"""
    skills = extract_jd_skills.invoke({"jd_text": state["jd_content"]})
    return {"jd_skills": skills}

def node_match_resume(state: AgentState):
    """节点2：简历匹配打分"""
    match_data = resume_match_score.invoke({
        "resume_content": state["resume_content"],
        "jd_skills": state["jd_skills"]
    })
    return {"match_result": match_data}

def node_gen_interview(state: AgentState):
    """节点3：生成面试题"""
    interview = generate_interview_questions.invoke({
        "jd_skills": state["jd_skills"],
        "lack_skills": state["match_result"]["lack_skills"]
    })
    return {"interview_content": interview}

def node_summary(state: AgentState):
    """节点4：汇总所有已生成的数据，输出格式化的最终报告"""
    prompt = f"""
请根据以下已生成的分析数据，整理成一份结构清晰的求职分析报告，直接输出结果，不要提工具调用、不要说执行步骤。

【已提取的岗位技能】
{state['jd_skills']}

【简历匹配结果】
匹配总分：{state['match_result']['score']}分
已掌握技能：{state['match_result']['match_skills']}
技能缺口：{state['match_result']['lack_skills']}

【面试题库】
{state['interview_content']}

输出格式严格按照以下结构：
### 一、岗位核心要求
逐条列出岗位技能

### 二、简历匹配度
显示匹配总分，用一句话总结匹配情况

### 三、已掌握技能
逐条罗列

### 四、技能缺口与优化建议
逐条说明缺口，并给出对应的简历补充方向

### 五、高频面试题与答题思路
整理成清晰的题目+思路格式
"""
    final = llm.invoke(prompt)
    return {"final_report": final.content}

# 4. 搭建流程图
workflow = StateGraph(AgentState)

workflow.add_node("解析简历文件", node_parse_resume_file)
workflow.add_node("抽取JD技能", node_extract_jd)
workflow.add_node("简历匹配打分", node_match_resume)
workflow.add_node("生成面试题", node_gen_interview)
workflow.add_node("汇总报告", node_summary)

workflow.add_edge(START, "解析简历文件")
workflow.add_edge("解析简历文件", "抽取JD技能")
workflow.add_edge("抽取JD技能", "简历匹配打分")
workflow.add_edge("简历匹配打分", "生成面试题")
workflow.add_edge("生成面试题", "汇总报告")
workflow.add_edge("汇总报告", END)

# 记忆持久化
memory = MemorySaver()
agent = workflow.compile(checkpointer=memory)

