import os
import datetime

from langchain.agents import AgentExecutor
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

from backend.llm_agent import (
    GetCalendarEventsTool,
    TimeDeltaTool,
    CreateCalendarEventTool,
    SpecificTimeTool,
    DeleteCalendarEventTool,
)




def run_agent_executor(user_email: str, user_input: str, calendar_id: str):
    # Options
    llm = AzureChatOpenAI(temperature=0, model="GPT35TURBO",
                azure_endpoint=os.getenv("AZURE_ENDPOINT"),
                api_version = os.getenv("API_VERSION"),
                api_key=os.getenv("API_KEY"))
    tools = [
        TimeDeltaTool(),
        GetCalendarEventsTool(),
        CreateCalendarEventTool(),
        SpecificTimeTool(),
        DeleteCalendarEventTool(),
    ]

    input = f"""
calendar_id: {calendar_id}
user_email: {user_email}
current datetime: {datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")}
current weekday: {datetime.datetime.utcnow().strftime("%A")}
user input: {user_input}
"""
    print(f"======= Starting Agent with input ======= \n {input} \n")

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a funny and friendly Google Calendar assistant. NEVER print event ids to the user.",
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    functions = [format_tool_to_openai_function(t) for t in tools]

    llm_with_tools = llm.bind(functions=functions)

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    result = agent_executor.invoke({"input": input})

    return result.get("output")