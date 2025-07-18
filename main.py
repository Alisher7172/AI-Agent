from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

@tool
def calculator(a: float, b: float) -> str:
    """A simple calculator tool that perform arithmetic calculations."""
    return f"The sum of {a} and {b} is {a + b}."

def main():
    model = ChatOpenAI(temperature=0, streaming=True)


    tools = [calculator]
    agent_executor = create_react_agent(model, tools)
    
    print("Welcome to the AI Agent!. Type q to quit.")
    print("You can ask me anything, and I will try to help you.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input == "q":
            print("Exiting the AI Agent. Goodbye!")
            break
        print("\nAssistant: " , end="")
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print() 

if __name__ == "__main__":
    main()

