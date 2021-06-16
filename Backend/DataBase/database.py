from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session, registry

# create an engine


from Backend.response import Response, PrimitiveParsable
from Backend.settings import Settings

SQLAlchemy_DATABASE_URI = "postgresql://nklfongbputsdr:780ea33e04aa8fb36400cd72967b97385d186978a31d262416b53791ae93c425@ec2-54-155-35-88.eu-west-1.compute.amazonaws.com:5432/d58n31ogjjv4sj"
SQLAlchemy_DATABASE_URI = Settings.get_instance(False).get_DB()
engine = create_engine(SQLAlchemy_DATABASE_URI)
# create a configured "Session" class
Session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))
session = Session(expire_on_commit=False)
mapper_registry = registry()
db_fail_response = Response(False, obj=PrimitiveParsable(-1), msg="DB failed, please try again later")
