import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def search(query: str) -> str:
    """Search for information about a topic."""
    query = query.lower()
    if any(phrase in query for phrase in ["capital of france", "france capital", "paris france"]):
        return "Found information: Paris is the capital of France"
    elif "capital" in query:
        return "I can only tell you about the capital of France at the moment."
    return f"No specific information found for: {query}"

def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        return str(eval(expression))
    except:
        return "Invalid expression"

def get_tool_response(tool_name: str, tool_input: str) -> str:
    """Get response from a specific tool."""
    tools = {
        "search": search,
        "calculator": calculator
    }
    return tools[tool_name](tool_input)

def run_agent(query: str) -> str:
    """Run the agent with a query."""
    try:
        # Create a chat completion using the new API structure
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using GPT-4o Mini model - faster and more cost-effective
            messages=[
                {"role": "system", "content": """You are a helpful AI assistant that can use tools to answer questions.
Available tools:
- search: Search for information about topics (currently only knows about France's capital)
- calculator: Perform mathematical calculations

To use a tool, respond in the format:
TOOL: <tool_name>
INPUT: <tool_input>

If you have the final answer, respond with:
FINAL ANSWER: <your answer>"""},
                {"role": "user", "content": query}
            ],
            temperature=0
        )

        # Get the assistant's response
        assistant_response = response.choices[0].message.content

        # Parse the response
        if "TOOL:" in assistant_response:
            # Extract tool name and input
            tool_lines = assistant_response.split("\n")
            tool_name = tool_lines[0].replace("TOOL:", "").strip().lower()
            tool_input = tool_lines[1].replace("INPUT:", "").strip()

            # Get tool response
            tool_response = get_tool_response(tool_name, tool_input)

            # Get final answer with tool response
            final_response = client.chat.completions.create(
                model="gpt-4o-mini",  # Using GPT-4o Mini model - faster and more cost-effective
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant. Provide a clear and concise final answer based on the tool's response."},
                    {"role": "user", "content": f"Tool response: {tool_response}\nWhat is the final answer?"}
                ],
                temperature=0
            )
            return final_response.choices[0].message.content
        else:
            # Return direct response if no tool was used
            return assistant_response.replace("FINAL ANSWER:", "").strip()

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Testing the agent...")
    print("Using OpenAI API key:", os.getenv("OPENAI_API_KEY")[:10] + "...")
    
    try:
        print("\nTesting search functionality:")
        result = run_agent("What is the capital of France?")
        print(f"Result: {result}")
        
        print("\nTesting calculator functionality:")
        result = run_agent("What is 2 + 2?")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Test failed with error: {str(e)}")
        import traceback
        print("Full error:")
        print(traceback.format_exc())