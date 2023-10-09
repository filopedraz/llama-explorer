import requests
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Step 2: Define the SQLite model using SQLAlchemy


class GitHubUser(Base):
    __tablename__ = 'github_users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    login = Column(String(50))
    name = Column(String(100))
    location = Column(String(100))


# Setup the SQLite database
DATABASE_URL = "sqlite:///github_users.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Step 3: Fetch data from the GitHub API


def fetch_github_user(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(
            f"Failed to fetch user {username}. Status Code: {response.status_code}")
        return None

# Step 4: Save the fetched data into the SQLite database using the ORM


def save_user_to_db(user_data):
    user = GitHubUser(
        login=user_data['login'],
        name=user_data.get('name', ''),
        location=user_data.get('location', '')
    )
    session.add(user)
    session.commit()


def main():
    username = input("Enter the GitHub username: ")
    user_data = fetch_github_user(username)
    if user_data:
        save_user_to_db(user_data)
        print(f"User {username} saved to the database.")


if __name__ == "__main__":
    main()
