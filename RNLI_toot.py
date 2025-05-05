import requests
from datetime import datetime
import os
import sys
import csv
from mastodon import Mastodon #Masto
from atproto import Client #Bsky

SOME_SECRET = os.environ['SOME_SECRET']
BSKY_SECRET = os.environ['BSKY_SECRET']

# Define the name of the file to write to
filename = 'launch_time.txt'

# Define the Mastodon instance URL and access token
mastodon_url = 'https://mas.to/'
access_token = 'SOME_SECRET'

# Create a Mastodon instance
mastodon = Mastodon(
    access_token=SOME_SECRET,
    api_base_url=mastodon_url
)

# Log int o BSKY
client = Client()
client.login('outonashout.bsky.social', BSKY_SECRET)

# Make a GET request to the API endpoint
response = requests.get('https://services.rnli.org/api/launches')
if response.status_code != 200:
    print('Failed to fetch launches:', response.status_code)
    sys.exit()

# Convert the response data to JSON format
response_data = response.json()

# Access the first launch in the response data
first_launch = response_data[0]

# Access the 'shortName' 'website' 'boat id' and 'launchDate' parameters for the first launch
short_name = first_launch['title']
website = first_launch['website']
boat_id = first_launch['lifeboat_IdNo']

# Parse the ISO 8601 formatted date string and convert it to a datetime object
launch_datetime = datetime.fromisoformat(first_launch['launchDate'])

# Format the datetime object as hh:mm and store it in a string variable
launch_time = launch_datetime.strftime('%H:%M')

# Function to look up lifeboat class by IdNo
def get_lifeboat_class(boat_id):
    with open('RNLI_Lifeboat_Fleet.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # Check if the second column matches the boat_id
            if row[10] == boat_id:
                return row[12]  # Return the 12th column (lifeboat class)
    return "Unknown Lifeboat"

# Get the lifeboat class based on the IdNo
lifeboat_class = get_lifeboat_class(boat_id)

# Check if the file already exists
if os.path.isfile(filename):
    # If the file exists, read its contents and compare to the new launch time
    with open(filename, 'r') as file:
        last_launch_time = file.read()
    if last_launch_time == launch_time:
        # If the launch time hasn't changed, exit the program without writing to the file
        print('Launch time has not changed:', launch_time)
        sys.exit()
    else:
        # If the launch time has changed, delete the existing file and continue
        os.remove(filename)

# Write the new launch time to the file
with open(filename, 'w') as file:
    file.write(launch_time)

# Ensure URL is fully qualified with "https://"
full_url = f'https://{website}'

# Create a hashtag suitable for both platforms
# hashtag = '#RNLI'

# Format the status update with full URL and hashtag. changed to try and deal with "Unknown class Class lifeboat"
# # status_update = f'{lifeboat_class} class lifeboat launched from {short_name} at {launch_time} - {full_url}'

# Determine the correct format for the lifeboat class in the status update
if lifeboat_class == "Unknown Lifeboat":
    # Format status update without "Unknown Lifeboat" and "class"
    status_update = f'Lifeboat launched from {short_name} at {launch_time} - {full_url}'
else:
    # Include lifeboat class as usual
    status_update = f'{lifeboat_class}-class lifeboat launched from {short_name} at {launch_time} - {full_url}'


# Post to Mastodon
try:
    mastodon.status_post(status_update)
except Exception as e:
    print('Mastodon post failed:', e)

# Post to Bluesky
try:
    post = client.send_post(status_update)
except Exception as e:
    print('Bluesky post failed:', e)

# Confirmation message
print('Launch time has been updated to:', launch_time)
