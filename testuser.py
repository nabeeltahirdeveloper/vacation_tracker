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
    first_name = Column(String(130), nullable=False)
    last_name = Column(String(130), nullable=False)
    email = Column(String(130), nullable=False)
    personal_email = Column(String(130), nullable=False)
    national_id_number = Column(String(14), nullable=False)
    personal_phone = Column(String(14), nullable=False)
    phone = Column(String(14), nullable=False)
    title = Column(String(130), nullable=False)

# Create the database schema
# Drop the existing 'users' table if it exists
# Base.metadata.drop_all(engine)

# Create the database schema with the updated table structure
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Add the provided credentials directly
#new_user = User(first_name="Asmaa", last_name="Shehata", email="john@example.com", personal_email="asmaa@example.com", national_id_number="12345678910123", personal_phone="12345678910123", phone="12345678910123", title="Software Engineer")
user1= User(first_name="Rita", last_name="John", email="rita@example.com", personal_email="r.john@example.com", national_id_number="12345678910123", personal_phone="12345678910123", phone="12345678910123", title="Software Engineer")
user2= User(first_name="Zina", last_name="John", email="zeina@example.com", personal_email="zina.john@example.com", national_id_number="12345678910456", personal_phone="12345678910123", phone="12345678910789", title="accountant")

session.add(user1)
session.commit()

print("User added successfully.")

# Close the session
session.close()
