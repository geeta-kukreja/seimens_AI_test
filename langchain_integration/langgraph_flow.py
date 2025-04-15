from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, MessagesState, END, START
from langchain_google_genai import ChatGoogleGenerativeAI
import logging
from config import GOOGLE_API_KEY, DB_URI
from db_connection import checkpointer, memory_store

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if not GOOGLE_API_KEY:
    logger.error("GOOGLE_API_KEY environment variable not set.")
    raise EnvironmentError("GOOGLE_API_KEY environment variable not set.")


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)


def generate(state: MessagesState):
    tool_messages = [m for m in state["messages"] if m.type == "tool"][-2:]
    context = "\n\n".join(msg.content for msg in tool_messages)
    sys_msg = SystemMessage(
        content="You are an assistant for question-answering tasks. "
                "Use the following pieces of retrieved context to answer "
                "the question. If you don't know the answer, say that you "
                "don't know. Use three sentences maximum and keep the "
                "answer concise: \n\n" + context
    )
    chat_history = [
        m
        for m in state["messages"]
        if m.type in ("human", "system") or (m.type == "ai" and not m.tool_calls)
    ]
    prompt = [sys_msg] + chat_history
    response = llm.invoke(prompt)
    return {"messages": [response]}


def get_langgraph():
    builder = StateGraph(MessagesState)
    builder.add_node("generate", generate)
    builder.add_edge(START, "generate")
    builder.add_edge("generate", END)
    return builder.compile(checkpointer=checkpointer, store=memory_store)
