SOME_SECRET = os.environ['SOME_SECRET']

access_token = 'SOME_SECRET'

print(SOME_SECRET)

# Create a Mastodon instance
mastodon = Mastodon(
    access_token=access_token,
    api_base_url=mastodon_url
)
print("access token", access_token)

# Open a file for writing
with open("output.txt", "w") as file:
    # Write the variable to the file
    file.write("some secret")
    file.write(SOME_SECRET)
    file.write("access token")
    file.write(access_token)
