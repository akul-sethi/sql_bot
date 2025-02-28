import mysql.connector
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.tools import tool
from langgraph.graph import START, END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama


SYSTEM_PROMPT = """
You are a helpful assistant called Akul who will help Sonia access and control a mysql database. Use the tool provided to execute commands on her behalf.
"""


mydb = mysql.connector.connect(
    host="localhost", user="root", password="Soniarider214", database="University"
)
mycursor = mydb.cursor()

llm = ChatOllama(
    model="deepseek-r1",
)


@tool
def query_mysql(query):
    "Use this to run a command on a mysql database"
    mycursor.execute(query)
    return str(mycursor.fetchall())


def generate(state):
    with_tools = llm.bind_tools([query_mysql])
    response = with_tools.invoke(state["messages"])
    return {"messages": [response]}


messages = {"messages": [SystemMessage(SYSTEM_PROMPT)]}

graph_builder = StateGraph(MessagesState)

tools = ToolNode([query_mysql])
graph_builder.add_node("generate", generate)
graph_builder.add_node("tools", tools)

graph_builder.add_edge(START, "generate")
graph_builder.add_conditional_edges("generate", tools_condition)
graph_builder.add_edge("tools", "generate")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "1"}}

graph.update_state(config, messages)

while True:
    x = input("User: ")
    messages = {"messages": [HumanMessage(x)]}
    for chunk in graph.stream(messages, config=config, stream_mode="values"):
        pass
    print(chunk["messages"][-1].content)
