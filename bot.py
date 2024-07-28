import requests
from urllib.parse import parse_qs, urlsplit
import json
import time
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_welcome_message():
    print(r"""
 
  _  _   _    ____  _   ___    _   
 | \| | /_\  |_  / /_\ | _ \  /_\  
 | .` |/ _ \  / / / _ \|   / / _ \ 
 |_|\_/_/ \_\/___/_/ \_\_|_\/_/ \_\
                                   

    """)
    print(Fore.GREEN + Style.BRIGHT + "POP To The MOON BOT")
    print(Fore.CYAN + Style.BRIGHT + "Jajanin dong orang baik :)")
    print(Fore.YELLOW + Style.BRIGHT + "0x5bc0d1f74f371bee6dc18d52ff912b79703dbb54")
    print(Fore.RED + Style.BRIGHT + "Update Link: https://github.com/dcbott01/tothemoon")
    print(Fore.BLUE + Style.BRIGHT + "Tukang Rename MATI AJA")

# Common headers for both requests
common_headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json;charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache'
}

# Function to perform the login and fetch asset data
def process_account(initData):
    login_url = 'https://moon.popp.club/pass/login'

    # Parsing initData to extract initDataUnSafe
    parsed_data = {k: v[0] for k, v in parse_qs(urlsplit(f'/?{initData}').query).items()}
    user_data = json.loads(parsed_data.get('user', '{}'))

    # Prepare the payload with specific formatting
    payload = {
        'initData': initData,
        'initDataUnSafe': {
            'query_id': parsed_data.get('query_id', ''),
            'user': {
                'id': int(user_data.get('id', 0)),
                'first_name': user_data.get('first_name', ''),
                'last_name': user_data.get('last_name', ''),
                'username': user_data.get('username', ''),
                'language_code': user_data.get('language_code', 'en'),
                'is_premium': user_data.get('is_premium', False),
                'allows_write_to_pm': user_data.get('allows_write_to_pm', False)
            },
            'auth_date': parsed_data.get('auth_date', ''),
            'hash': parsed_data.get('hash', '')
        }
    }

    # Send POST request to obtain the token
    response = requests.post(login_url, headers=common_headers, json=payload)
    time.sleep(2)  # Adding a delay of 2 seconds

    # Extract token from the response
    if response.status_code == 200:
        response_data = response.json()
        token = response_data.get('data', {}).get('token', None)
        if token:
            print(f"{Fore.GREEN}====== Berhasil Mendapatkan Data ======")

            # Use the token to make an authorized GET request for asset data
            asset_url = 'https://moon.popp.club/moon/asset'
            asset_headers = common_headers.copy()
            asset_headers['Authorization'] = token

            # Send GET request to access asset data
            asset_response = requests.get(asset_url, headers=asset_headers)
            time.sleep(2)  # Adding a delay of 2 seconds

            if asset_response.status_code == 200:
                asset_data = asset_response.json()
                print(f"{Fore.CYAN}[Username] : {Fore.MAGENTA}{payload['initDataUnSafe']['user']['username']}{Style.RESET_ALL}")

                # Extract sd, probe, eth, and calculate remaining time
                sd = asset_data.get('data', {}).get('sd', 0)
                probe = asset_data.get('data', {}).get('probe', 0)
                eth = asset_data.get('data', {}).get('eth', 0)
                farming_end_time = asset_data.get('data', {}).get('farmingEndTime', 0)
                system_timestamp = asset_data.get('data', {}).get('systemTimestamp', 0)

                # Calculate remaining time in milliseconds
                remaining_time_ms = max(0, farming_end_time - system_timestamp)

                # Convert milliseconds to hours, minutes, and seconds
                remaining_seconds = remaining_time_ms // 1000
                hours = remaining_seconds // 3600
                minutes = (remaining_seconds % 3600) // 60
                seconds = remaining_seconds % 60

                print(f"{Fore.CYAN}[SD] : {Fore.MAGENTA}{sd}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}[Probe] : {Fore.MAGENTA}{probe}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}[ETH] : {Fore.MAGENTA}{eth}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Remaining time for claim: {Fore.YELLOW}{hours} hours, {minutes} minutes, and {seconds} seconds{Style.RESET_ALL}")

                # Check for frozenInviteSd and claim if available
                frozen_invite_sd = asset_data.get('data', {}).get('frozenInviteSd', 0)
                if frozen_invite_sd > 0:
                    print(f"{Fore.GREEN}Claiming invite rewards...{Style.RESET_ALL}")
                    invite_claim_url = 'https://moon.popp.club/moon/claim/invite'
                    invite_claim_response = requests.get(invite_claim_url, headers=asset_headers)
                    time.sleep(2)  # Adding a delay of 2 seconds

                    if invite_claim_response.status_code == 200:
                        print(Fore.GREEN + "Success Claim Invite Rewards.")
                    else:
                        print(Fore.RED + f"Claim invite rewards request failed with status code {invite_claim_response.status_code}")

                # If remaining time for claim is 0, claim farming rewards
                if remaining_seconds == 0:
                    # Claim farming rewards
                    claim_farming_url = 'https://moon.popp.club/moon/claim/farming'
                    claim_response = requests.get(claim_farming_url, headers=asset_headers)
                    time.sleep(2)  # Adding a delay of 2 seconds

                    if claim_response.status_code == 200:
                        print(Fore.GREEN + "Success Claim Farming.")
                    else:
                        print(Fore.RED + f"Claim farming request failed with status code {claim_response.status_code}")

                    # Update farming data
                    update_farming_url = 'https://moon.popp.club/moon/farming'
                    update_response = requests.get(update_farming_url, headers=asset_headers)
                    time.sleep(2)  # Adding a delay of 2 seconds

                    if update_response.status_code == 200:
                        print(Fore.GREEN + "Start Farming.")

                        # Re-fetch asset data to update remaining time
                        asset_response = requests.get(asset_url, headers=asset_headers)
                        time.sleep(2)  # Adding a delay of 2 seconds

                        if asset_response.status_code == 200:
                            asset_data = asset_response.json()

                            # Extract the updated remaining time
                            farming_end_time = asset_data.get('data', {}).get('farmingEndTime', 0)
                            system_timestamp = asset_data.get('data', {}).get('systemTimestamp', 0)

                            # Calculate remaining time in milliseconds
                            remaining_time_ms = max(0, farming_end_time - system_timestamp)

                            # Convert milliseconds to hours, minutes, and seconds
                            remaining_seconds = remaining_time_ms // 1000
                            hours = remaining_seconds // 3600
                            minutes = (remaining_seconds % 3600) // 60
                            seconds = remaining_seconds % 60

                            print(f"{Fore.CYAN}Updated remaining time for claim: {Fore.YELLOW}{hours} hours, {minutes} minutes, and {seconds} seconds{Style.RESET_ALL}")
                        else:
                            print(Fore.RED + f"Asset request failed with status code {asset_response.status_code}")
                    else:
                        print(Fore.RED + f"Start farming data request failed with status code {update_response.status_code}")

            else:
                print(Fore.RED + f"Asset request failed with status code {asset_response.status_code}")

            # Use the token to make an authorized GET request for planets data
            planets_url = 'https://moon.popp.club/moon/planets'
            planets_headers = common_headers.copy()
            planets_headers['Authorization'] = token

            # Send GET request to access planets data
            planets_response = requests.get(planets_url, headers=planets_headers)
            time.sleep(2)  # Adding a delay of 2 seconds

            if planets_response.status_code == 200:
                planets_data = planets_response.json()

                # Print only the IDs of the planets
                print(Fore.GREEN + "Planet IDs:")
                for planet in planets_data.get('data', []):
                    planet_id = planet['id']
                    print(Fore.GREEN + str(planet_id))
                    time.sleep(2)  # Adding a delay of 2 seconds between each planet exploration request

                    # If probe > 0 and planet ID found, make explorer request
                    if probe > 0:
                        explorer_url = f'https://moon.popp.club/moon/explorer?plantId={planet_id}'
                        explorer_response = requests.get(explorer_url, headers=planets_headers)
                        time.sleep(2)  # Adding a delay of 2 seconds

                        if explorer_response.status_code == 200:
                            explore_data = explorer_response.json().get('data', {})
                            amount = explore_data.get('amount', 0)
                            award = explore_data.get('award', 'N/A')
                            print(f"{Fore.CYAN}Explorer for planet {Fore.MAGENTA}{planet_id}{Style.RESET_ALL}{Fore.CYAN}, Award: {Fore.MAGENTA}{award}{Style.RESET_ALL}{Fore.CYAN}, Amount: {Fore.MAGENTA}{amount}{Style.RESET_ALL}")
                        else:
                            print(Fore.RED + f"Explorer request for planet {planet_id} failed with status code {explorer_response.status_code}")
            else:
                print(Fore.RED + f"Planets request failed with status code {planets_response.status_code}")

        else:
            print(Fore.RED + "Token not found in the response.")
    else:
        print(Fore.RED + f"Login request failed with status code {response.status_code}")

    return remaining_seconds

# Main execution
print_welcome_message()

while True:
    shortest_remaining_time = float('inf')

    # Read initData for multiple accounts from data.txt
    with open('query.txt', 'r') as file:
        initData_lines = file.readlines()

    # Process each account
    for index, initData in enumerate(initData_lines):
        initData = initData.strip()
        if initData:
            print(f"{Fore.YELLOW}====== Processing account {index + 1}/{len(initData_lines)} ======")
            remaining_seconds = process_account(initData)
            time.sleep(2)  # Adding a delay of 2 seconds between processing accounts

            # Track the shortest remaining time for next action
            if remaining_seconds > 0 and remaining_seconds < shortest_remaining_time:
                shortest_remaining_time = remaining_seconds

    # Wait for the shortest remaining time for next claim or farming update
    if shortest_remaining_time < float('inf'):
        print(f"{Fore.GREEN}====== Semua Akun Telah Di Proses ======")
        print(f"{Fore.CYAN}Waiting {shortest_remaining_time // 3600} hours, {(shortest_remaining_time % 3600) // 60} minutes, and {shortest_remaining_time % 60} seconds before re-processing...{Style.RESET_ALL}")
        time.sleep(shortest_remaining_time)
    else:
        # If no remaining time is set, wait a default time (e.g., 10 minutes) before next check
        print(f"{Fore.CYAN}No specific wait time, waiting 10 minutes...{Style.RESET_ALL}")
        time.sleep(600)  # 10 minutes
