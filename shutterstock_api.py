import requests

# Set up Shutterstock API credentials
api_key = "g2t8YXASYd2bGSsuBiWfiAEz2E94TVMG"
api_secret = "ctzQGAuZTPsyp0nX"
api_token = "v2/ZzJ0OFlYQVNZZDJiR1NzdUJpV2ZpQUV6MkU5NFRWTUcvMTcwNTQ4OTgwL2N1c3RvbWVyLzQvc2w0MVlRVkViWkFtM3dUNzRaSjRiUUhsT0ZyTDFyeVpiN01WWlpuanFsemk2RjZISTBEdUJjTU9PN2RfYkdPSHJ2MU5CY25Pb0lQS2lTOV92TTMwTF9BOGJfT1lNc2lMT0VxcEFHV0dZRk45VF94eDVNZVJtMG53V3d2VlNFZ0lqZHdXRkg0VmV2d1AyU3NaTjNQOXNIZEpDYXY5WkNNT3RUZFlTMmk1Sks1MGlDUHhrLUs3Y1ZiRm9FbG1rTy1jaU1COUZGLUR0NTh2eVl5LTFzeVRTQS9JSFpySGhJWTJaVWFlZUt0YmIzMkxR"

# Set up search parameters
search_term = "ben nevis"
per_page = 1
sort = "popular"
image_type = "photo"
people_number = 0
safe = "true"
# orientation = "horizontal"
# license = "editorial"

# Construct the API request
url = f"https://api.shutterstock.com/v2/images/search?query={search_term}&per_page={per_page}&sort={sort}&image_type={image_type}&people_number={people_number}&safe={safe}"
headers = {
    "Authorization": f"Bearer {api_token}"
}

print(url)

# Send the request and get the response
response = requests.get(url, headers=headers)
data = response.json()

print(data)
# Print the results
# for image in data["data"]:
#     print(image["id"])

