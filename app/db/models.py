from datetime import datetime
import uuid
from sqlalchemy import MetaData, Table, Column, ForeignKey
from sqlalchemy import (
    Integer,
    String,
    Text,
    Boolean,
    TIMESTAMP,
    Uuid
)


metadata = MetaData()


cities = Table(
    'cities',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name_en', String(255), nullable=False),
    Column('name_ka', String(255), nullable=False),
)

districts = Table(
    'districts',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name_en', String(255), nullable=False),
    Column('name_ka', String(255), nullable=False),

    Column('city_id', Integer, ForeignKey('cities.id'))
)

streets = Table(
    'streets',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name_en', String(255)),
    Column('name_ka', String(255), nullable=False),

    Column('district_id', Integer, ForeignKey('districts.id'))
)

outages = Table(
    'outages',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('type', String(255), nullable=False),
    Column('provider', String(255), nullable=False),
    Column('emergency', Boolean, nullable=False),
    Column('title_en', String(255)),
    Column('title_ka', String(255)),
    Column('description_en', Text),
    Column('description_ka', Text),
    Column('start', TIMESTAMP),
    Column('end', TIMESTAMP),
    Column('uuid', Uuid, default=uuid.uuid4),
    Column('created_at', TIMESTAMP, default=datetime.now),

    Column('street_id', Integer, ForeignKey('streets.id'))
)
