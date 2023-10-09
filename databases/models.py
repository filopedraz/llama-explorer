import requests
from peewee import Model, CharField, PostgresqlDatabase

# PostgreSQL database configuration
DATABASE = 'your_database_name'
USER = 'your_username'
PASSWORD = 'your_password'
HOST = 'localhost'
PORT = 5432

# Step 1: Define the PostgreSQL database and the model using Peewee
db = PostgresqlDatabase(DATABASE, user=USER,
                        password=PASSWORD, host=HOST, port=PORT)


class GitHubUser(Model):
    login = CharField()
    name = CharField(null=True)
    location = CharField(null=True)

    class Meta:
        database = db


# Create tables if they don't exist
db.connect()
db.create_tables([GitHubUser], safe=True)

# Step 2: Fetch data from the GitHub API


def fetch_github_user(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(
            f"Failed to fetch user {username}. Status Code: {response.status_code}")
        return None

# Step 3: Save the fetched data into the PostgreSQL database using Peewee


def save_user_to_db(user_data):
    GitHubUser.create(
        login=user_data['login'],
        name=user_data.get('name', ''),
        location=user_data.get('location', '')
    )


def main():
    username = input("Enter the GitHub username: ")
    user_data = fetch_github_user(username)
    if user_data:
        save_user_to_db(user_data)
        print(f"User {username} saved to the database.")


if __name__ == "__main__":
    main()
