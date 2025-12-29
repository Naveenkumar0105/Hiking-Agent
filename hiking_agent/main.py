import ollama
from weather import get_weather, get_todays_weather_summary
from parks import get_parks, get_trails
from location import get_current_location
from config import NPS_API_KEY


def query_model(system_prompt, user_prompt):
    """Generic function to query the ollama model."""
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    """ this is the way to structure the prompt for the GPT model"""
    print("Asking model...")
    response = ollama.chat(model='gpt-oss:20b', messages=messages)
    return response['message']['content'].strip()


def main():
    # step 1: Getting our location

    print("Starting the hiking agent...")
    print("Detecting your location...")
    latitude, longitude, state = get_current_location()
    if not latitude:
        print("Could not find your location. Please try again later or restart the program.")
        return

    print(f"Your location(State) is: {state}")

    # Step 2: Getting the weather information

    print("Checking the weather near you...")
    weather_data = get_weather(latitude, longitude)
    if not weather_data:
        print("Could not retrieve weather data. Please try again later or restart the program.")
        return
    weather_summary = get_todays_weather_summary(weather_data)
    print(f"Weather summary is: {weather_summary}")

    # Reflection 1: Decide if the weather is good enough for a hike

    weather_prompt = f"Based on this forecast, is it a good day for a hike? {weather_summary}"
    weather_system_prompt = "You are an assistant that determines if the weather is good for hiking. Respond with only 'yes' or 'no'."
    model_decision = query_model(weather_system_prompt, weather_prompt).lower()
    print(f"Model decision: {model_decision}")

    if "no" in model_decision:
        print("\nThe model determined the weather is not suitable for hiking today.")
        return

    # Step 4: Gather park and trail data

    print("\nWeather looks good! Searching for nearby parks and trails...")
    parks_data = get_parks(NPS_API_KEY, state)

    if not parks_data or not parks_data.get("data"):
        print(f"Could not find any parks or trails data in {state}. Please try again later.")
        return

    # getting the park data and storing it in a dictionary and giving it to AI
    # The AI will understand that data on our behalf and gives us recommendations
    print("Analyzing parks and trails...")

    parks_and_trails = {}
    for park in parks_data["data"]:
        park_name = park['fullName']
        trails_data = get_trails(NPS_API_KEY, park["parkCode"])
        if not trails_data:
            continue
        if trails_data.get("data"):
            trails_list = [trail['title'] for trail in trails_data["data"]]
            parks_and_trails[park_name] = trails_list

    print("Asking the model for hiking recommendations...")
    recommendations_system_prompt = "You are an expert hiking guide. Your task is to analyze the following list of parks and trails and recommend the top 2-3 options..."

    # converting the big dictionary of key value pair into a string
    prompt_data = ""
    for park_name, trails in parks_and_trails.items():
        prompt_data += f"\nPark: {park_name}\n"
        if trails:
            for trail in trails:
                prompt_data += f" - Trail: {trail}\n"
        else:
            prompt_data += " - No specific trails listed.\n"

    recommendations = query_model(recommendations_system_prompt,
                                  f"Here are the available parks and trails:\n{prompt_data}")
    print("\n Hiking Recommendations:")
    print(recommendations)


if __name__ == '__main__':
    main()
