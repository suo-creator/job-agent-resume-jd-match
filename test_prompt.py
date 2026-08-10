from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from system_prompt import SYSTEM_PROMPT

load_dotenv()
print(os.getenv("LLM_MODEL_NAME"))
llm = ChatOpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
    model=os.getenv("LLM_MODEL_NAME"),
)

res = llm.invoke([
    ("system", SYSTEM_PROMPT),
    ("human", "简历：熟练使用Python、Pandas、FastAPI、RAG基础开发；JD：需要Python、FastAPI、RAG、向量数据库、Docker")
])
print(res.content)

