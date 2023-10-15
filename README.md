# 🦙 Llama Explorer

SCREENSHOT / COVER

Keep track of all the Open Source AI projects, repositories, and contributors in an intuitive UI.

Check out the [Llama Explorer](https://llama-explorer.joandko.io/) website.

## 🚀 Roadmap

- [ ] One Leaderboard to rule them all. No more 10 different tabs to check OpenLLM Leaderboard, CodeGen Leaderboards etc etc.
- [ ] Fear and Hype Index. A metric to measure the hype and fear around open-source AI based on Twitter and Reddit posts.
- [ ] Hot Topics and Trends. A list of the most popular topics and trends in the Open Source AI community. Check on what the main projects are working on based on Issues and PRs.
- [ ] Hot Tools. A list of the most mentioned tools across Reddit and Twitter.

## 🛠️ Self Host

Simply use `docker-compose`

```bash
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
```
