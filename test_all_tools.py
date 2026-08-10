from tools.jd_extract import extract_jd_skills
from tools.match_tool import resume_match_score
from tools.interview_tool import generate_interview_questions
from tools.resume_file_parser import parse_resume_file

# 替换成你本地简历文件路径
resume_text = parse_resume_file.invoke({"file_path": r"C:\Users\86152\Downloads\索梓轩-个人简历.pdf"})
print("提取的简历文本：\n", resume_text)
if __name__ == "__main__":
    # 1. 模拟岗位JD文本
    test_jd = """
    岗位职责：
    1. 使用Python、Pandas做数据分析
    2. FastAPI开发后端接口
    3. 搭建RAG知识库，使用FAISS向量库
    4. 使用Docker容器化部署项目
    要求熟悉大模型调用、文本分块、检索增强生成
    """

    # 2. 模拟个人简历文本
    test_resume = """
    熟练掌握Python、Pandas；独立开发FastAPI后端服务；
    完成RAG检索增强项目，实现文档切片、FAISS向量存储、知识库问答；
    了解大模型API调用，未深度使用Docker线上部署。
    """

    print("===== 第一步：抽取JD岗位技能 =====")
    skill_list = extract_jd_skills.invoke({"jd_text": test_jd})
    print("抽取到的岗位技能：")
    for s in skill_list:
        print(f"- {s}")
    print("\n")

    print("===== 第二步：简历与JD匹配打分 =====")
    match_result = resume_match_score.invoke({
        "resume_content": test_resume,
        "jd_skills": skill_list
    })
    print(f"匹配总分：{match_result['score']}")
    print("已掌握技能：")
    for s in match_result["match_skills"]:
        print(f"- {s}")
    print("技能缺口：")
    for s in match_result["lack_skills"]:
        print(f"- {s}")
    print("\n")

    print("===== 第三步：根据缺口生成面试题 =====")
    interview_text = generate_interview_questions.invoke({
        "jd_skills": skill_list,
        "lack_skills": match_result["lack_skills"]
    })
    for line in interview_text:
        if line.strip():
            print(line)