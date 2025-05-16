import dataclasses
import logging
import typing as t

from bs4 import BeautifulSoup

from cratedb_about.util import get_cache_client


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Resource:
    url: str
    size: int = -1


@dataclasses.dataclass
class LLMsTxtHubItem:
    title: str
    website: str
    description: str
    logo: str
    tags: t.List[str] = dataclasses.field(default_factory=list)
    resources: t.List[Resource] = dataclasses.field(default_factory=list)


class LLMsTxtHub:
    url: str = "https://llmtxt.dev/hub"

    def __init__(self):
        self.items: t.List[LLMsTxtHubItem] = []
        self.client = get_cache_client(ttl=60*60*24)

    def fetch(self):
        index_html = self.client.get(self.url)
        bs = BeautifulSoup(index_html, "html.parser")
        cards = bs.find_all(attrs={"class": "website-card"})
        self.items = [self.card_to_model(card) for card in cards]
        self.acquire_sizes()
        return self

    def acquire_sizes(self):
        logger.info(f"Acquiring sizes for {len(self.items)} items")
        for item in self.items:
            logger.info(f"Acquiring size for {item}")
            for resource in item.resources:
                try:
                    response = self.client.get(resource.url)
                    resource.size = len(response.text)
                except Exception as e:
                    logger.warning(f"Failed to acquire size for {item}: {e}")

    @staticmethod
    def card_to_model(card):
        divs = card.find(name="div")
        title = divs.find(name="h3").text
        tags = []
        for tag in divs.find_all(name="span"):
            tags.append(tag.text)
        website = divs.find(name="p", attrs={"class": "text-sm"}).text
        description = divs.find(name="p", attrs={"class": "text-sm", "title": True}).text
        logo_url = divs.find(name="img").get("src")
        resources = []
        for anchor in divs.find_all(name="a"):
            resources.append(Resource(url=anchor.get("href")))
        return LLMsTxtHubItem(title=title, website=website, description=description, logo=logo_url, tags=tags, resources=resources)
