import requests


from main import fetch_stargazers

response = requests.get("https://api.github.com/repos/ggerganov/llama.cpp/stargazers?page=500&per_page=100")
print(response.status_code)

exit()
users = fetch_stargazers("ggerganov/llama.cpp")
print(users)
print(len(users))