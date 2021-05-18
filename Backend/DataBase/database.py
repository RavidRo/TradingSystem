from datetime import date

from sqlalchemy import create_engine, Column, Integer, String, Date, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# create an engine
SQLAlchemy_DATABASE_URI = 'postgresql://nklfongbputsdr:780ea33e04aa8fb36400cd72967b97385d186978a31d262416b53791ae93c425@ec2-54-155-35-88.eu-west-1.compute.amazonaws.com:5432/d58n31ogjjv4sj'
engine = create_engine(SQLAlchemy_DATABASE_URI)

# create a configured "Session" class
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


class Actor(Base):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthday = Column(Date)

    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday


movies_actors_association = Table(
    'movies_actors', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
)


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    actors = relationship("Actor", secondary=movies_actors_association)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date


Base.metadata.create_all(engine)

# 3 - create a new session

def add():
    session = Session()

    session.add(bourne_identity)
    session.add(furious_7)
    session.add(pain_and_gain)

    session.add(matt_damon)
    session.add(dwayne_johnson)
    session.add(mark_wahlberg)

    session.commit()
    session.close()

def query():
    session = Session()
    movies = session.query(Movie).all()

    # 4 - print movies' details
    print('\n### All movies:')
    for movie in movies:
        print(f'{movie.title} was released on {movie.release_date}')
    print('')
    session.commit()
    session.close()

if __name__ == '__main__':


    bourne_identity = Movie("The Bourne Identity", date(2002, 10, 11))
    furious_7 = Movie("Furious 7", date(2015, 4, 2))
    pain_and_gain = Movie("Pain & Gain", date(2013, 8, 23))

    matt_damon = Actor("Matt Damon", date(1970, 10, 8))
    dwayne_johnson = Actor("Dwayne Johnson", date(1972, 5, 2))
    mark_wahlberg = Actor("Mark Wahlberg", date(1971, 6, 5))

    bourne_identity.actors = [matt_damon]
    furious_7.actors = [dwayne_johnson]
    pain_and_gain.actors = [dwayne_johnson, mark_wahlberg]

    # query()
    session = Session()
    session.query(Actor).delete(matt_damon)
    session.commit()
    session.close()




