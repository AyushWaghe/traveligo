from langchain.agents import create_agent
from langchain_core.messages import HumanMessage,SystemMessage

from llm.model import create_llm
from tools.flight_search_tool import search_flight_tool


# def create_planner_agent():
llm=create_llm()
    
tools=[search_flight_tool]
    
agent=create_agent(
        model=llm,
        tools=tools,
        system_prompt="""
        You are Traveligo, an AI-powered travel assistant.

        Your responsibility is to help users search for flights.

        Instructions:
        1. Extract the origin, destination, and departure date.
        2. Use the available flight search tool when flight information is requested.
        3. Never fabricate flight prices or availability.
        4. Present the flight results clearly and concisely.
        5. Always mention the correct currency.
        6. If no flights are found, inform the user.
    """
    )
    
response=agent.invoke({
     "messages": [
        HumanMessage(
            content="Find flights from Mumbai to Delhi on November 25, 2026"
        )
    ]
})

print(response["messages"][-1].content)