from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

# create an engine
from Backend.Domain.TradingSystem.product import Product

SQLAlchemy_DATABASE_URI = 'postgresql://nklfongbputsdr' \
                          ':780ea33e04aa8fb36400cd72967b97385d186978a31d262416b53791ae93c425@ec2-54-155-35-88.eu-west' \
                          '-1.compute.amazonaws.com:5432/d58n31ogjjv4sj '
engine = create_engine(SQLAlchemy_DATABASE_URI)

# create a configured "Session" class
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Session = scoped_session(Session)

Base = declarative_base()
