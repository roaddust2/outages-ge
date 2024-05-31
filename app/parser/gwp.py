from datetime import datetime, date
from urllib.parse import urljoin
from app.parser.base import AbstractProvider
from typing import List


class GWP(AbstractProvider):
    """GWP water provider"""

    TYPE = 'water'
    ROOT_URL = 'https://www.gwp.ge'
    PLANNED_URL = urljoin(ROOT_URL, '/en/dagegmili')
    EMERGENCY_URL = urljoin(ROOT_URL, '/en/gadaudebeli')

    async def scrap_outages(self, emergency: bool = False) -> list:
        """Abstract interface to retrieve outages"""

        # Retrieve current date
        current_date = datetime.now().date()

        # Determine url for emergency type
        url = self.EMERGENCY_URL if emergency else self.PLANNED_URL

        # Retrieve outage alerts with links
        scrapped_outages = await self._get_outages(url, current_date, emergency)

        # Divide outages by districts
        outages_by_district = await self._divide_outages_by_district(scrapped_outages)

        # TODO: divide outages by streets

        # Return results
        return outages_by_district

    async def _get_outages(
        self, url: str, current_date: date, emergency: bool
    ) -> List[dict]:
        """Scraps outages on high level from outages list view"""

        result = []
        soup = await self._get_soup(url)

        rows = soup.find('table', class_='samushaoebi').find_all('tr')

        for row in rows:
            date = datetime.strptime(
                row.find('span', {'style': 'color:#f00000'}).text.strip(),
                '%d/%m/%Y'
            ).date()
            if date >= current_date:
                link = urljoin(self.ROOT_URL, row.a.get('href'))
                title = row.find_all("a")[1].get_text(strip=True)
                result.append(
                    {
                        'date': date,
                        'type': self.TYPE,
                        'emergency': emergency,
                        'title': title,
                        'link': link
                    }
                )

        return result

    async def _divide_outages_by_district(
        self, outages: List[dict]
    ) -> List[dict]:
        """Jump into outage detail view and scrap it"""

        result = []

        for outage in outages:

            # Description patterns
            emergency = outage.get('emergency')
            if emergency:
                selector = ".initial > ul > li > p"
            else:
                selector = ".news-details > p"

            url = outage.get('link')
            soup = await self._get_soup(url)
            outage_descriprions = soup.css.select(selector)

            # TODO: Select districts from database
            # and add District.id to outage dictionary
            for description in outage_descriprions:
                if description.get_text(strip=True) != '':
                    result.append(
                        {
                            'date': outage.get('date'),
                            'type': self.TYPE,
                            'emergency': emergency,
                            'title': outage.get('title'),
                            'description': description.get_text(strip=True).replace("\xa0", " ")
                        }
                    )

        return result
    
    # TODO: divide outages by streets
    async def _divide_outages_by_streets():
        pass
