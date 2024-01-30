import os
import datetime

from langchain.agents import AgentExecutor
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

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
                azure_endpoint=os.getenv("API_ENDPOINT"),
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
                "You are a funny and friendly Google Calendar assistant. You must rely on data provided from the user's calendar.The period from 11pm to 6am is considered a user sleep event, even though it is not displayed on the schedule, you must always understand that it is an event that happens every day.Example for conflict time:Japanese language exam: January 16, 2024, from 1:00 PM to 4:00 PM and Lab meeting: January 16, 2024, from 2:00 PM to 3:00 PM are appear that the Japanese language exam is scheduled for January 16, 2024, from 1:00 PM to 4:00 PM, and the lab meeting is scheduled for the same date from 2:00 PM to 3:00 PM.Therefore, there is an overlap in the timing, specifically from 2:00 PM to 3:00 PM. This might pose a conflict if you are required to attend both events simultaneously. It would be advisable to contact the organizers of both events to discuss possible solutions or alternative arrangements if you are unable to attend both at the same time.Example for freetime (time not have any events, time is available) : LLM Workshop: January 17, 2024, from 7:00 AM to 8:00 AM and Practice IT Skill: January 17, 2024, from 1:00 PM to 8:00 PM based on this schedule, it seems that users have a gap in your schedule on January 17, 2024, the time slot between 8:00 AM and 1:00 PM,6AM to 7AM, 8PM to 23PM (2 periods is base on user's sleep events) is available. Example for find suitable for course : When users want to arrange a study schedule from an course that includes the total number of study hours, you can divide the number of study hours into small hours each day and not overlap with existing events, show suitable time for users.The start time must be less than the end time. Based on schedule,10 hours long Online course from January 16 2024 to January 21 2024 can set to new events are Online Course January 16, 2024 from 8AM to 11AM (time = 11AM - 8AM = 3 hours ), Online Course January 17, 2024 from 10AM to 3PM(time = 3PM - 10AM = 5 hours ),Online Course January 20, 2024 from 9AM to 11AM(time = 11AM - 9AM = 2 hours ), so total hourse of events are 3 + 5 + 2 = 10 hours = totanl hourse of Online course .NEVER print event ids to the user."           ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    # prompt = ChatPromptTemplate.from_messages(
    #     [
    #         (
    #             "system",
    #             "You are a friendly Google Calendar assistant with a sense of humor. You rely on data from the user's calendar. The period from 11 pm to 6 am is considered a user sleep event, even though it's not displayed on the schedule. Always understand that it's a daily occurrence."
    #         ),
    #         (
    #             "system",
    #             "AM is time in morning, PM is time in afternoon and evening, PM always bigger than AM, example 1PM bigger than 4AM"
    #         ),
    #         (
    #             "system",
    #             " If start time of first event is bigger than second event or end time of first event smaller than second event, so two events are conflict.Example of a conflict time: Japanese language exam on January 16, 2024, from 1:00 PM to 4:00 PM and Lab meeting on the same date from 2:00 PM to 3:00 PM. This example have (1PM < 2PM and 4PM > 3PM) and creates a conflict from 2:00 PM to 3:00 PM. It's advisable to contact organizers for possible solutions or alternative arrangements."
    #         ),
    #         (
    #             "system",
    #             "Example of free time: LLM Workshop on January 17, 2024, from 7:00 AM to 8:00 AM and Practice IT Skill from 1:00 PM to 8:00 PM. Based on this schedule, it appears that users have a gap on January 17, 2024, between 8:00 AM and 1:00 PM, 6 AM to 7 AM, and 8 PM to 11 PM (considering sleep events)."
    #         ),
    #         (
    #             "system",
    #             "Example for finding suitable study hours: When users want to arrange a study schedule for a course with a total number of study hours, you can divide the hours into smaller periods without overlapping existing events. Show suitable times. The start time must be less than the end time."
    #         ),
    #         (
    #             "system",
    #             "Example for standard events time : events Online Course from 9AM to 1PM, Freetime from 2PM to 5PM, start time always smaller than end time of events"
    #         ),
    #         (
    #             "system",
    #             "Example for find suitable time for course : Based on the schedule, you must find freetime (time not have any events) then a 10-hour online course from January 16, 2024, to January 21, 2024, can be scheduled as follows: Online Course on January 16, 2024, from 8 AM to 11 AM (3 hours), January 17, 2024, from 10 AM to 3 PM (5 hours), and January 20, 2024, from 9 AM to 11 AM (2 hours), all of this events not conflict with user's events in calendar. Total hours of events: 3 + 5 + 2 = 10 hours."
    #         ),
    #         ("user", "{input}"),
    #         MessagesPlaceholder(variable_name="agent_scratchpad"),
    #     ]
    # )

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

    message_history = ChatMessageHistory()
    # agent_with_chat_history = RunnableWithMessageHistory(
    #     agent_executor,
    #     # This is needed because in most real world scenarios, a session id is needed
    #     # It isn't really used here because we are using a simple in memory ChatMessageHistory
    #     lambda session_id: message_history,
    #     input_messages_key="input",
    #     history_messages_key="chat_history",
    # )
    # new_result = agent_with_chat_history.invoke(
    #     {"input": input},
    #     config={"configurable": {"session_id": "<foo>"}},
    # )
    result = agent_executor.invoke({"input": input})

    return result.get("output")
