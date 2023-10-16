# 🦙 Llama Explorer

![cover](https://github.com/filopedraz/llama-explorer/assets/29598954/9cfc62de-c110-4c2b-aadf-77749ece1bd9)

Keep track of all the Open Source AI projects, repositories, and contributors in an intuitive UI.

## 🖥️ First Glance

<img width="1093" alt="image" src="https://github.com/filopedraz/llama-explorer/assets/29598954/c95215c9-001c-4d6a-986a-eb9142183beb">

Check out the [Llama Explorer](https://llama-explorer.joandko.io/) website.

## 🚀 Roadmap

- [ ] One Leaderboard to rule them all. No more 10 different tabs to check OpenLLM Leaderboard, CodeGen Leaderboards etc etc.
- [ ] Fear and Hype Index. A metric to measure the hype and fear around open-source AI based on Twitter and Reddit posts.
- [ ] Hot Topics and Trends. A list of the most popular topics and trends in the Open Source AI community. Check on what the main projects are working on based on Issues and PRs.
- [ ] Hot Tools. A list of the most mentioned tools across Reddit and Twitter.

## 🛠️ Self Host with docker-compose

```bash
# clone the repo
git clone https://github.com/filopedraz/llama-explorer

# run the docker-compose
docker-compose up --build -d
```

## 💻 Contributing

```bash
# clone the repo
git clone https://github.com/filopedraz/llama-explorer

# install all dependencies
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# configure pre-commit
pip install pre-commit
pre-commit install

# configure env variables
cp .env.example .env

# run the peripherics with docker-compose
docker-compose up -d postgres redis

# run the django backend
python manage.py migrate
python manage.py runserver

# run the tasks to fetch data
python manage.py repositories
python manage.py commits
python manage.py contributors
python manage.py locations

# run the streamlit app
streamlit run Home.py
```
