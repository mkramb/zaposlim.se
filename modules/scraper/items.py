from scrapy.item import Item, Field

class BaseItem(Item):
    def load_image(self, image_url):
        self['image_urls'] = []
        self['image_urls'].append(image_url)

class JobItem(BaseItem):
    id = Field()
    source = Field()
    source_label = Field()

    title = Field()
    company = Field()
    category = Field()

    city = Field()
    summary = Field()
    content = Field()
    published_date = Field()

    details_url = Field()
    image_urls = Field()
    images = Field()
