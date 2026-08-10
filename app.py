# 1. 所有导入包
import streamlit as st
import tempfile
import os
import uuid
from PyPDF2 import PdfReader
from agent_graph import agent

# 2. 页面配置
st.set_page_config(page_title="AI求职分析Agent", layout="wide")
st.title("AI求职简历&JD匹配分析工具")

# 3. 双栏布局
col1, col2 = st.columns(2)

with col1:
    st.header("上传简历文件/简历图片")
    uploaded_file = st.file_uploader("在这里拖放文件", type=["pdf", "docx"])

    st.divider()
    st.subheader("或手动粘贴简历文本（备用）")
    resume_input_text = st.text_area("简历内容", height=200)

with col2:
    st.header("粘贴招聘JD")
    jd_content = st.text_area("岗位JD", height=300)

# 4. 解析简历文本逻辑
resume_text = ""

# 优先解析上传的文件
if uploaded_file is not None:
    # 生成临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    try:
        # 调用工具统一解析，兼容pdf和docx
        from tools.resume_file_parser import parse_resume_file

        resume_text = parse_resume_file.invoke({"file_path": temp_path})
        st.success("简历文件解析成功")
    except Exception as e:
        st.warning(f"文件解析失败：{e}，请手动粘贴简历文字")
    finally:
        # 删除临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)

# 手动输入优先级更高
if resume_input_text.strip():
    resume_text = resume_input_text.strip()

# 5. 开始分析按钮
if st.button("开始求职分析", type="primary"):
    # 空值校验
    if not resume_text.strip():
        st.error("请上传简历文件或手动粘贴简历内容")
        st.stop()
    if not jd_content.strip():
        st.error("请粘贴岗位JD内容")
        st.stop()

    with st.spinner("分析中，请稍候..."):
        tid = str(uuid.uuid4())
        input_data = {
            "resume_content": resume_text,
            "jd_content": jd_content
        }
        # 调用Agent
        result = agent.invoke(
            input_data,
            config={"configurable": {"thread_id": tid}}
        )

        # 只展示最终报告，不输出整个字典
        st.divider()
        st.subheader("📋 求职分析最终报告")
        st.markdown(result["final_report"])