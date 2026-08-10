from tools.jd_extract import extract_jd_skills
from tools.match_tool import resume_match_score

jd_text = """需要Python、FastAPI、RAG、向量数据库、Docker部署"""
resume = "熟练Python、FastAPI，做过基础RAG知识库项目，会向量数据库基础使用"

# 先抽技能
skills = extract_jd_skills.invoke({"jd_text": jd_text})
# 再匹配打分
result = resume_match_score.invoke({
    "resume_content": resume,
    "jd_skills": skills
})
print(result)