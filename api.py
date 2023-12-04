import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
import base64

#Functions to get Tiltify Data
load_dotenv()

def authorize_tiltify():

    load_dotenv()

    
    token_url = 'https://v5api.tiltify.com/oauth/token'

    client_id = os.getenv('TILTIFY_API_ID')
    client_secret = os.getenv('TILTIFY_API_SECRET')

    credentials = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': "public" }

    response = requests.post(token_url, data=urlencode(credentials), headers={'Content-Type': 'application/x-www-form-urlencoded'})

    if response.status_code == 200:
        
        token_data = response.json()
        access_token = token_data.get('access_token')
        headers = {'Authorization': f'Bearer {access_token}'}

        return headers
        
    else:
        return response.status_code

def get_tiltify():

    
    team_campaign_id = '4e33d51d-bdca-4e45-863a-77a668a364d4'  
    api_url = f'https://v5api.tiltify.com/api/public/team_campaigns/{team_campaign_id}'

    headers = authorize_tiltify()
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        team_data = response.json()
        total_raised = float((team_data["data"]["amount_raised"]["value"]))+float((team_data["data"]["supporting_amount_raised"]["value"]))

        return float(total_raised)

    else:

        return response.status_code

#Functions to get Fourthwall Data

def get_fourthwall():
    
    load_dotenv()

    username = os.getenv('FOURTHWALL_USER')
    password =  os.getenv('FOURTHWALL_PASS')

    # Combine username and password with a colon
    combined_credentials = f"{username}:{password}"

    # Encode the combined credentials to Base64
    base64_credentials = base64.b64encode(combined_credentials.encode()).decode()

    api_url = "https://api.fourthwall.com/api/shops/stats/chart?chartTypes=PROFIT&from=2023-11-16T00%3A00%3A00Z&precision=DAY&sid=sh_46c88f17-4af1-4c56-8f75-583c6227ba3e&to=2024-01-16T23%3A59%3A59Z"
    headers = {
        "Authorization": f"Basic {base64_credentials}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()  # Parse the JSON response
        # Handle the API response data here
        value = aggregated_value = data['current']['profit']['aggregatedValue']

        return float(value)
    except requests.exceptions.RequestException as e:
        # Handle errors
        print("Error:", e)

#Functions to get Sheets Data

def authourize_sheets():
    pass



  

