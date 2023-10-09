# GH Metrics
# 0. Total records collected.
# 1. How many unique developers there are across these repositories?
# 2. Where do these developers come from?
# 3. How many developers are from the United States?
# 4. How many developers are experienced open-source developers (>100 follwers)?
# 5. How many developers have an email address listed on their profile?
# 6. How many developers have a company listed on their profile?
# 7. How many developers have experience with AI or ML based on their bio (Data, AI, ML, Machine Learning, Artificial Intelligence) in their profile?
# 8. Which Programmings languages are the most used by these developers?
# 9. Which are the most common words in the bio section of these developers?
# 10. Are these developers active (>10 commits per month)?

# Reddit Metrics
# List of all the posts mentioning the topics you are interested in with the links and summaries.

# 0. List of all the posts of yesterday with title and some stats (upvotes, comments, awards, etc).
# 1. Generic Yesterday summary of content
# 2. Most mentioned tools, languages, frameworks, etc.
# 3. Most mentioned companies

# Twitter Metrics
# 0. List of all the tweets of yesterday with title and some stats (likes, retweets, replies, etc).
# 1. Generic Yesterday summary of content
# 2. Most mentioned tools, languages, frameworks, etc.

import pandas as pd

df = pd.read_csv("./data/data.csv")
print(df.count())
