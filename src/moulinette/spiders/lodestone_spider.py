from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http.request import Request

from scrapy import log

from moulinette.items import (Character, CharacterLoader)
from moulinette.settings import (LODESTONE_URL, FREE_COMPANY_ID)


class LodestoneSpider(Spider):

    name = "lodestone_en"

    allowed_domains = [LODESTONE_URL]
    start_urls = [
        'http://{}/lodestone/freecompany/{}/member/'.format(LODESTONE_URL, FREE_COMPANY_ID),
    ]

    def parse(self, response):
        """ Parse the FC member list.

        Each member information is parsed using the parse_character_info method
        (depth-first exploration).
        """

        sel = Selector(response)
        members_sel = sel.xpath('//tr')

        for member_sel in members_sel:
            loader = CharacterLoader(item=Character(), selector=member_sel,
                                     response=response)

            loader.add_xpath(
                'name',
                './/div[@class="player_name_area"]//a/text()'
            )
            loader.add_xpath(
                'rank',
                './/div[@class="fc_member_status"]/text()[last()]'
            )
            loader.add_xpath(
                'id',
                './/div[@class="player_name_area"]//a/@href'
            )
            loader.add_xpath(
                'url',
                './/div[@class="player_name_area"]//a/@href'
            )


            character = loader.load_item()

            log.msg("* Player found : {}".format(character['name']),
                    level=log.INFO)

            yield Request(character['url'], callback=self.parse_character_info,
                          meta={'character': character})

        next = sel.xpath('//a[@rel="next"]')
        if next:
            next_page_url = next[0].xpath('./@href').extract()[0]
            yield Request(next_page_url, callback=self.parse)

    def parse_character_info(self, response):
        """ Parses detailed information about a character.
        """

        sel = Selector(response)
        character = response.request.meta['character']
        loader = CharacterLoader(item=character, selector=sel,
                                 response=response)

        loader.add_xpath(
            'race',
            '//div[@class="chara_profile_title"]/text()'
        )
        loader.add_xpath(
            'ethnic_group',
            '//div[@class="chara_profile_title"]/text()'
        )
        loader.add_xpath(
            'gender',
            '//div[@class="chara_profile_title"]/text()'
        )
        loader.add_xpath(
            'city_state',
            '//li[@class="clearfix"][2]/strong/text()'
        )
        loader.add_xpath(
            'gc',
            '//li[@class="clearfix"][3]/strong/text()'
        )
        loader.add_xpath(
            'gc_rank',
            '//li[@class="clearfix"][3]/strong/text()'
        )
        loader.add_xpath(
            'levels',
            '//td[@class="ic_class_wh24_box"]/following::td[1]/text()'
        )
        loader.add_xpath(
            'current_class',
            '//div[@class="ic_class_wh24_box"]/img[1]/@src'
        )
        loader.add_xpath(
            'current_gear',
            '//div[@class="item_detail_box"]//h2/text() | '
            '//div[@class="pt3 pb3"]/text()'
        )

        character = loader.load_item()

        yield character