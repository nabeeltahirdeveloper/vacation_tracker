from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime, Integer
from datetime import datetime

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
class Request(Base):
    __tablename__ = 'requests'
    #id = Column(Integer, primary_key=True)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    note = Column(String(500), nullable=True)
    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    response_by_id = Column(String(60), ForeignKey('users.id'), nullable=True)
    response = Column(Boolean, nullable=True)
    response_note = Column(String(1000), nullable=True)

# Create the database schema
# Drop the existing 'users' table if it exists
# Base.metadata.drop_all(engine)

# Create the database schema with the updated table structure
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Add the provided credentials directly
#new_request = Request(user_id = '03577cc7-aafd-4599-8aca-15799d3634cd', note = 'Sick Leave', starts_at = DateTime(2024, 2, 26, 0, 0), ends_at = DateTime(2024, 2, 26, 0, 0), duration = 1, response_by_id = 'bcf7c3d0-8274-4015-a3d0-000576b029c3', response = True, response_note = 'Approved')
n_reqest = Request(user_id='bcf7c3d0-8274-4015-a3d0-000576b029c3',note='Annual Leave', starts_at=datetime(2024, 2, 28), ends_at=datetime(2024, 2, 28), duration=1, response_by_id='70bff056-4f0c-449c-a69d-9c002013c5bb', response=True, response_note='Approved')

session.add(n_reqest)
session.commit()

print("Request added successfully.")

# Close the session
session.close()
