from datetime import datetime
import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    Uuid
)

from .base import Base


class City(Base):
    """City model"""

    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    name_ka: Mapped[str] = mapped_column(String(255), nullable=False)
    
    districts: Mapped['District'] = relationship('District', back_populates='city')


class District(Base):
    """District model"""

    __tablename__ = 'district'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey('city.id'))
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    name_ka: Mapped[str] = mapped_column(String(255), nullable=False)

    city = relationship('City', back_populates='districts')
    streets = relationship('Street', back_populates='district')


class Street(Base):
    """Street model"""

    __tablename__ = 'street'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    district_id: Mapped[int] = mapped_column(Integer, ForeignKey('district.id'))
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    name_ka: Mapped[str] = mapped_column(String(255), nullable=False)
    osm_id: Mapped[int] = mapped_column(Integer, nullable=False)

    district = relationship('District', back_populates='streets')
    outages = relationship('Outage', back_populates='street')


class Outage(Base):
    """Outage model"""

    __tablename__ = 'outage'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    street_id: Mapped[int] = mapped_column(Integer, ForeignKey('street.id'))
    house_number: Mapped[int] = mapped_column(Integer, nullable=True)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(255), nullable=False)
    emergency: Mapped[bool] = mapped_column(Boolean, nullable=False)
    title_en: Mapped[str] = mapped_column(String(255), nullable=True)
    title_ka: Mapped[str] = mapped_column(String(255), nullable=True)
    description_en: Mapped[str] = mapped_column(Text, nullable=True)
    description_ka: Mapped[str] = mapped_column(Text, nullable=True)
    start: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    end: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    uuid: Mapped['uuid.UUID'] = mapped_column(Uuid, default=uuid.uuid4, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now, nullable=False)

    street = relationship('Street', back_populates='outages')
