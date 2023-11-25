import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('TILTIFY_API_ID')
client_secret = os.getenv('TILTIFY_API_SECRET')

team_campaign_id = '4e33d51d-bdca-4e45-863a-77a668a364d4'  

token_url = 'https://v5api.tiltify.com/oauth/token'
api_url = f'https://v5api.tiltify.com/api/public/team_campaigns/{team_campaign_id}'

#Obtain Client Authorization for Server
credentials = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': "public" }

def authorize():
    response = requests.post(token_url, data=urlencode(credentials), headers={'Content-Type': 'application/x-www-form-urlencoded'})

    if response.status_code == 200:
        
        token_data = response.json()
        access_token = token_data.get('access_token')
        headers = {'Authorization': f'Bearer {access_token}'}

        return headers
        
    else:
        return response.status_code

def raised():
    headers = authorize()
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        team_data = response.json()
        total_raised = (team_data["data"]["amount_raised"]["value"])
        total_goal = (team_data["data"]["original_goal"]["value"])

        return total_raised

    else:

        return response.status_code

def goal():
    headers = authorize()
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        team_data = response.json()
        total_raised = (team_data["data"]["amount_raised"]["value"])
        total_goal = (team_data["data"]["original_goal"]["value"])
        
        return total_goal

    else:

        return response.status_code
    

