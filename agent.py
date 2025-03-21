import os
from dotenv import load_dotenv
from openai import OpenAI
from duckduckgo_search import DDGS
import requests
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def search(query: str) -> str:
    """Enhanced search function using DuckDuckGo."""
    try:
        # First try DuckDuckGo search
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                formatted_results = "\n".join([
                    f"- {result['title']}: {result['link']}\n  {result['body']}"
                    for result in results
                ])
                return f"Found information:\n{formatted_results}"
            return f"No results found for: {query}"
    except Exception as e:
        return f"Search error: {str(e)}"

def get_weather(location: str) -> str:
    """Get weather information for a location using OpenWeatherMap."""
    try:
        # You would need to sign up for a free API key at OpenWeatherMap
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return "Weather API key not configured. Please set OPENWEATHER_API_KEY in your .env file."
        
        # Make API request
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            # Format the response
            weather_info = f"Weather in {location}:\n"
            weather_info += f"Temperature: {data['main']['temp']}°F\n"
            weather_info += f"Feels like: {data['main']['feels_like']}°F\n"
            weather_info += f"Conditions: {data['weather'][0]['description']}\n"
            weather_info += f"Humidity: {data['main']['humidity']}%\n"
            weather_info += f"Wind speed: {data['wind']['speed']} mph"
            return weather_info
        else:
            return f"Could not get weather for {location}. Error: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Weather error: {str(e)}"

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
        "calculator": calculator,
        "weather": get_weather
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
- search: Search for information about any topic using DuckDuckGo
- calculator: Perform mathematical calculations
- weather: Get current weather for any location (requires OpenWeather API key)

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
    print("Testing the enhanced agent...")
    print("Using OpenAI API key:", os.getenv("OPENAI_API_KEY")[:10] + "...")
    
    try:
        print("\nTesting enhanced search functionality:")
        result = run_agent("What is the population of Tokyo?")
        print(f"Result: {result}")
        
        print("\nTesting weather functionality:")
        result = run_agent("What's the weather like in New York?")
        print(f"Result: {result}")
        
        print("\nTesting calculator functionality:")
        result = run_agent("What is 25 * 48?")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Test failed with error: {str(e)}")
        import traceback
        print("Full error:")
        print(traceback.format_exc())