from tools.jd_extract import extract_jd_skills

jd = """
岗位职责：
1. 使用Python进行数据分析与大模型应用开发
2. 基于FastAPI搭建后端接口
3. 搭建RAG知识库系统，向量数据库部署使用
4. 使用Docker完成项目容器打包与线上部署
"""

skills = extract_jd_skills.invoke({"jd_text": jd})
print("抽取到的岗位技能：", skills)