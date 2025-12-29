import requests


def get_parks(api_key, state_code):
    """
    Fetches park data from the National Park Service (NPS) API for a given state.

    Args:
        api_key (str): The API key for the NPS API.
        state_code (str): The two-letter state code to search for parks in.

    Returns:
        dict: A dictionary containing the API response with park data,
              or None if an error occurs.
    """
    url = f"https://developer.nps.gov/api/v1/parks?stateCode={state_code}&api_key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching parks data: {e}")
        return None


def get_trails(api_key, park_code):
    """
    Fetches "things to do" (including trails) from the NPS API for a specific park.

    Args:
        api_key (str): The API key for the NPS API.
        park_code (str): The park code for the specific park.

    Returns:
        dict: A dictionary containing the API response with trail data,
              or None if an error occurs.
    """
    url = f"https://developer.nps.gov/api/v1/thingstodo?parkCode={park_code}&api_key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trails data: {e}")
        return None


if __name__ == '__main__':
    # Example usage
    from config import NPS_API_KEY

    state_code = "CA"  # Example state code for California
    parks_data = get_parks(NPS_API_KEY, state_code)

    if "data" in parks_data and parks_data["data"]:
        # Get trails for the first park in the list
        park_code = parks_data["data"][0]["parkCode"]
        trails_data = get_trails(NPS_API_KEY, park_code)

        if "data" in trails_data:
            print(f"Trails in {parks_data['data'][0]['fullName']}:")
            for trail in trails_data["data"]:
                print(trail["title"])
        else:
            print("Could not fetch trails data.")
    else:
        print("Could not fetch parks data. Please check your API key and state code.")
