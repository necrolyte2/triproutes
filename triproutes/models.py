from sqlalchemy import (
    Column, Index, Integer,
    Text, Float, ForeignKey,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(
        extension=ZopeTransactionExtension()
    )
)
Base = declarative_base()

class Trip(Base):
    __tablename__ = 'trip'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    complete = Column(Boolean)
    plops = relationship("Plop")

    def __init__( self, name ):
        self.name = name
        self.complete = False

class Plop(Base):
    __tablename__ = 'plop'
    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lng = Column(Float)
    timestamp = Column(Integer)
    annotation = Column(Text)
    trip_id = Column(Integer, ForeignKey('trip.id'))

    def __init__( self, lat, lng, timestamp, annotation='', trip=None ):
        self.lat = lat
        self.lng = lng
        self.timestamp = timestamp
        self.annotation = annotation
        if isinstance( trip, int ):
            self.trip_id = trip
        else:
            self.trip_id = trip.id

    @property
    def datetime( self ):
        from datetime import datetime
        if self.timestamp:
            try:
                d = datetime.fromtimestamp( self.timestamp )
            except ValueError as e:
                if 'year is out of range' in e.message:
                    d = datetime.fromtimestamp( self.timestamp/1000.0 )
                else:
                    raise e
        else:
            d = None
        return d

#Index('my_index', MyModel.name, unique=True, mysql_length=255)
