import requests
from datetime import datetime
import os
import sys
from mastodon import Mastodon

SOME_SECRET = os.environ['SOME_SECRET']
print("secret1")
print(SOME_SECRET)

# Define the name of the file to write to
filename = 'launch_time.txt'

# Define the Mastodon instance URL and access token
mastodon_url = 'https://botsin.space/'
access_token = 'SOME_SECRET'

print("secret")
print(SOME_SECRET)
print("access")
print(access_token)

# Create a Mastodon instance
mastodon = Mastodon(
    access_token=SOME_SECRET,
    api_base_url=mastodon_url
)
print("access token", access_token)

# Make a GET request to the API endpoint
response = requests.get('https://services.rnli.org/api/launches')

# Convert the response data to JSON format
response_data = response.json()

# Access the first launch in the response data
first_launch = response_data[0]

# Access the 'shortName' 'website' and 'launchDate' parameters for the first launch
short_name = first_launch['shortName']
website = first_launch['website']

# Parse the ISO 8601 formatted date string and convert it to a datetime object
launch_datetime = datetime.fromisoformat(first_launch['launchDate'])

# Format the datetime object as hh:mm and store it in a string variable
launch_time = launch_datetime.strftime('%H:%M')


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

# Post to Mastodon with a status update
status_update = f'Launched from {short_name} at {launch_time} - http://{website}'

mastodon.status_post(status_update)

# Print a confirmation message to the console
print('Launch time has been updated to:', launch_time)
