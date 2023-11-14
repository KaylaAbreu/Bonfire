import requests
import base64
import API_key

def plant_search():
    with open("poison_ivy.jpg", "rb") as file:
        images = [base64.b64encode(file.read()).decode("ascii")]

    response = requests.post("https://api.plant.id/v2/identify",
        json={
            "images": images,
            "modifiers": ["similar_images"],
            "plant_details": ["common_names", "url"],
        },
        headers={
            "Content-Type": "application/json",
            "Api-Key": API_key.API_key,
        }).json()
    for suggestion in response["suggestions"]:
        print("plant name: ",suggestion["plant_name"])
        print("plant details: ",suggestion["plant_details"]["common_names"])
        print("url: ", suggestion["plant_details"]["url"])
        print("probability: ",  suggestion["probability"])

if __name__ == '__main__':
    plant_search()