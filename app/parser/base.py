from abc import ABC, abstractmethod
import logging
import time
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.parser.exceptions import GetOutagesError


class AbstractProvider(ABC):
    """
    Abstract base class defining a common interface for provider classes.

    This class serves as a blueprint for creating provider parsers,
    ensuring a consistent interface across various provider implementations.

    You should redefine ROOT_URL, PLANNED_URL, EMERGENCY_URL, TYPE and
    scrap_outages, normalize_ouyages abstract methods.

    Example:
        ```python
        class GWP(AbstractProvider):

            TYPE = 'water'
            ROOT_URL = 'https://www.gwp.ge'
            EMERGENCY_URL = urljoin(ROOT_URL, '/emergency')
            PLANNED_URL = urljoin(ROOT_URL, '/planned')

            async def scrap_outages(self) -> list:
                # Yourl logic here
                return [
                    {'date': 'yyyy-mm-dd',
                    'type': 'water',
                    'emergency': True,
                    'title': 'Title',
                    'info': 'Info'
                    }
                ]
        ```
    """

    ROOT_URL = 'https://www.example.com'
    EMERGENCY_URL = urljoin(ROOT_URL, '/emergency')
    PLANNED_URL = urljoin(ROOT_URL, '/planned')
    TYPE = 'type'

    async def get_outages(self) -> list:
        """Wrapper"""

        try:
            start_time = time.time()
            logging.debug("Scrapping started.")
            scrapped_outages = await self.scrap_outages(emergency=False)
            scrapped_outages.extend(await self.scrap_outages(emergency=True))
            logging.debug(
                f"Scrapping ended. "
                f"{len(scrapped_outages)} elements in {time.time() - start_time}s"
            )

            return scrapped_outages

        except Exception as err:
            raise GetOutagesError(err)

    @staticmethod
    async def _get_soup(url: str) -> BeautifulSoup:
        """Returns soup from given url"""

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response_text = response.text

        soup = BeautifulSoup(response_text, 'html.parser')
        return soup

    @abstractmethod
    async def scrap_outages(self, emergency: bool = False) -> list:
        """Scraps outages"""
        pass
