import requests


username = input("username: ").strip()

response = requests.get(f"https://api.github.com/users/{username}/events")

r = response.json()

print(type(r))

commit = 0 
repo_create = 0 


for data in r:
    print(data)
    print()