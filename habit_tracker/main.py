import requests
import datetime

TOKEN = "ekfl123ijad"
USERNAME = "fen1z"
GRAPH_ID = "graph1"

pixela_endpoint = "https://pixe.la/v1/users"

# Create a user
parameters = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# response = requests.post(pixela_endpoint, json=parameters)
# print(response.text)


# Create a graph
graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"
graph_config = {
    "id": GRAPH_ID,
    "name": "Learning",
    "unit": "hours",
    "type": "float",
    "color": "momiji",
}

headers = {
    "X-USER-TOKEN": TOKEN,
}

# response = requests.post(graph_endpoint, json=graph_config, headers=headers)
# print(response.text)

# Create a pixel
today = datetime.datetime.now()
pixel_creation_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
pixel_params = {
    "date": today.strftime("%Y%m%d"),
    "quantity": input("How many hours have you learned? "),
}

# response = requests.post(pixel_creation_endpoint, json=pixel_params, headers=headers)
# print(response.text)

# Update a pixel
pixel_update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/20240327"
update_params = {
    "quantity": "15"
}
# response = requests.put(pixel_update_endpoint, json=update_params, headers=headers)
# print(response.text)

# Delete a pixel
pixel_delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/20240327"
response = requests.delete(pixel_delete_endpoint, headers=headers)
print(response.text)
