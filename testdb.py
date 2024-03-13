from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Provided database connection details
db_type = "mysql"
username = "lynks_eng"
password = "lynks_eng_pwd"
hostname = "localhost"
port = "3306"
database_name = "lynks_db"
echo_status = False # Disabling echo by default, change to True if needed

# Construct the database URL
db_url = f"{db_type}://{username}:{password}@{hostname}:{port}/{database_name}"

# Create an engine to connect to the database
engine = create_engine(db_url, echo=echo_status)

# Create a base class for our declarative class definitions
Base = declarative_base()

# Define a Credentials class to represent the table structure
class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  # name = Column(String(60))
  # address = Column(String(100))
  # email = Column(String(30))
  

# Create the database schema
# Drop the existing 'users' table if it exists
#Base.metadata.drop_all(engine)

# Create the database schema with the updated table structure

Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Add the provided credentials directly
new_user = User(name="Asmaa", address="123 Main St", email="john@example.com")
session.add(new_user)
session.commit()

print("User added successfully.")

# Close the session
session.close()
