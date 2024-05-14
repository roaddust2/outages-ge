#!/usr/bin/env python
import os
import sys
import logging
from typing import Optional, List
import argparse
from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session
import overpy
import time

# Required to "import" from parent directory
sys.path.append(
    os.path.join(os.path.dirname(__file__), '..')
)

from settings import DATABASE_URL  # noqa: E402
from app.db.models import City, District, Street  # noqa: E402


logging.basicConfig(level=logging.DEBUG)


class Database:
    """
    The primary purpose of this class is to populate the database with initial data
    for cities and districts and to keep the streets data updated by interfacing with the Overpass API.

    Attributes (optional):
        cities (list): List of city dictionaries.
        districts (list): List of district dictionaries.

    Methods:
        setup_cities(self): Populate database with cities.
        setup_districts(self): Populate database with districts.
        update_streets(self): Interface with the Overpass API, to update streets data.
        Update existing, Insert new and Delete removed (key is Street.osm_id column).
    """

    def __init__(self, cities: Optional[List[dict]] = None, districts: Optional[List[dict]] = None) -> None:
        self.engine = create_engine(DATABASE_URL)
        self.cities = cities if cities is not None else [{'name_en': 'Tbilisi', 'name_ka': 'თბილისი'}]
        self.districts = districts if districts is not None else [
            {"city_id": 1, "name_en": "Samgori District", "name_ka": "სამგორის რაიონი"},
            {"city_id": 1, "name_en": "Nadzaladevi District", "name_ka": "ნაძალადევის რაიონი"},
            {"city_id": 1, "name_en": "Didube District", "name_ka": "დიდუბის რაიონი"},
            {"city_id": 1, "name_en": "Saburtalo District", "name_ka": "საბურთალოს რაიონი"},
            {"city_id": 1, "name_en": "Vake District", "name_ka": "ვაკის რაიონი"},
            {"city_id": 1, "name_en": "Isani District", "name_ka": "ისნის რაიონი"},
            {"city_id": 1, "name_en": "Krtsanisi District", "name_ka": "კრწანისის რაიონი"},
            {"city_id": 1, "name_en": "Chugureti District", "name_ka": "ჩუღურეთის რაიონი"},
            {"city_id": 1, "name_en": "Mtatsminda District", "name_ka": "მთაწმინდის რაიონი"},
            {"city_id": 1, "name_en": "Gldani District", "name_ka": "გლდანის რაიონი"}
        ]

    def setup_cities(self) -> None:

        with Session(self.engine) as session:
            for city in self.cities:
                city_name = city.get('name_en')
                existing_city = session.query(City).filter_by(name_en=city_name).first()
                if existing_city is None:
                    session.add(City(name_en=city_name, name_ka=city.get('name_ka')))
                    session.commit()
                    logging.info(f"{city_name} inserted successfully!")
                else:
                    logging.info(f"{city_name} already exists in the database.")
        return

    def setup_districts(self) -> None:

        with Session(self.engine) as session:
            for district in self.districts:
                district_city = district.get('city_id')
                district_name = district.get('name_en')
                existing_district = session.query(District).filter_by(
                    city_id=district_city,
                    name_en=district_name).first()
                if existing_district is None:
                    session.add(District(city_id=district_city, name_en=district_name, name_ka=district.get('name_ka')))
                    session.commit()
                    logging.info(f"{district_name} inserted successfully!")
                else:
                    logging.info(f"{district_name} already exists in the database.")
        return

    def update_streets(self) -> None:  # noqa: C901

        api = overpy.Overpass()
        query = """
        [out:json];
        area["name:en"="{district}"]->.district;
        (
        way(area.district)["highway"="trunk"]["name"];
        way(area.district)["highway"="primary"]["name"]["bridge"!="Yes"];
        way(area.district)["highway"="secondary"]["name"];
        way(area.district)["highway"="tertiary"]["name"];
        way(area.district)["highway"="residential"]["name"];
        way(area.district)["highway"="living_street"]["name"];
        );
        out tags;
        """
        with Session(self.engine) as session:
            districts = session.query(District).all()
            new_streets = []
            old_streets = session.query(Street).all()

            # Map existing streets by osm_id column as key
            existing_streets_map = {old_street.osm_id: old_street for old_street in old_streets}

            # TODO: Need refactoring
            for district in districts:
                logging.info(f"Trying to retrieve all streets of {district.name_en}.")
                try:
                    time.sleep(0.1)
                    result = api.query(query.format(district=district.name_en))
                    logging.info(f"{len(result.ways)} streets retrieved successfully.")
                except Exception as err:
                    logging.error(f"Error occured when retrieving data from Overpass API. {err}")
                for way in result.ways:
                    street = {
                        'district_id': district.id,
                        'name_en': way.tags.get('name:en'),
                        'name_ka': way.tags.get('name:ka', way.tags.get('name')),
                        'osm_id': way.id
                    }
                    new_streets.append(street)

            # Update existing streets
            for street in new_streets:
                exists = existing_streets_map.get(street['osm_id'])
                if exists:
                    try:
                        session.execute(update(Street).where(Street.osm_id == street['osm_id']).values(street))
                        session.commit()
                    except Exception as err:
                        session.rollback()
                        logging.error(f"Error occured when updating streets in database. {err}")

            # Insert new streets
            try:
                insert_mapping = [street for street in new_streets if street['osm_id'] not in existing_streets_map]
                session.bulk_insert_mappings(Street, insert_mapping)
                session.commit()
            except Exception as err:
                session.rollback()
                logging.error(f"Error occured when inserting new streets in database. {err}")

            # Delete removed streets
            try:
                filter_mapping = [street['osm_id'] for street in new_streets]
                session.query(Street).filter(~Street.osm_id.in_(filter_mapping)).delete(synchronize_session=False)
                session.commit()
            except Exception as err:
                session.rollback()
                logging.error(f"Error occered when deleting removed streets from database. {err}")

        return


def main():

    parser = argparse.ArgumentParser(description='outages-ge command-line utility')
    parser.add_argument(
        'function',
        help='Function to execute [setup_cities, setup_districts, update_streets]'
    )
    args = parser.parse_args()

    db = Database()

    match args.function:
        case 'setup_cities':
            db.setup_cities()
        case 'setup_districts':
            db.setup_districts()
        case 'update_streets':
            db.update_streets()
        case _:
            print('Command does not exist')
    pass


if __name__ == '__main__':
    main()
