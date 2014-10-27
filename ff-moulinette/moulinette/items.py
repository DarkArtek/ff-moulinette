# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import (Identity, TakeFirst, Compose,
                                             MapCompose)
from scrapy import log

from moulinette.settings import LODESTONE_URL

import requests
import hashlib


class Character(Item):
    """ Item class for parsed characters.

    Characters' informations are scrapped from the Lodestone database. Bear in
    mind that some fields contain several values, as *levels* and
    *current_gear* set.
    Saving character items must take into account the current class in order to
    override the correct gear set.
    """

    id = Field()
    url = Field()
    name = Field()

    rank = Field()

    race = Field()
    ethnic_group = Field()
    gender = Field()

    city_state = Field()
    gc = Field()
    gc_rank = Field()

    levels = Field()
    current_class = Field()
    current_gear = Field()


class CharacterLoader(ItemLoader):
    """ Loader for the Character items, define attribure processors.

    Pre-save field processing is more likely to be performed here.
    """

    item_name_to_id = requests.get("http://xivpads.com/items.json").json()

    def strip_tabs_newlines(value):
        return value.strip('\t\n')

    def get_character_id(character_sheet_url):
        return character_sheet_url.split('/')[-2]

    def get_full_character_url(character_sheet_url, loader_context):
        return 'http://{}{}'.format(LODESTONE_URL, character_sheet_url)

    def get_race(title_section):
        return title_section.split(' / ')[0]

    def get_ethnic_group(title_section):
        return title_section.split(' / ')[1].split('\n')[0]

    def get_gender(title_section):
        gender_sign = title_section.split('\n')[1].strip('\t')
        if gender_sign == u'\u2642':
            return 'male'
        else:
            return 'female'

    def get_gc(gc_title):
        return gc_title.split('/')[0]

    def get_gc_rank(gc_title):
        return gc_title.split('/')[1]

    def clean_levels(levels_list):
        return [int(lvl) if lvl != u'-' else 0 for lvl in levels_list]

    def get_levels(cleaned_levels_list):
        classes = ['gla', 'pgl', 'mar', 'lcn', 'arc',
                   'cnj', 'tha', 'acn',
                   'car', 'bls', 'arm', 'gld', 'ltw', 'wvr', 'alc', 'cul',
                   'min', 'btn', 'fsh']
        return dict(zip(classes, cleaned_levels_list))

    def get_class_from_miniature(img_url):
        img_name = img_url.split('/')[-1].split('?')[0]
        img_classes = {
            u'59fde9fca303490477962039f6cd0d0101caeabe.png': u'arcanist',
            u'ec5d264e53ea7749d916d7d8bc235ec9c8bb7b51.png': u'gladiator',
            u'6157497a98f55a73af4c277f383d0a23551e9e98.png': u'conjurer',
            u'924ded09293b2a04c4cd662afbf7cda7b0576888.png': u'lancer',
            u'd39804e8810aa3d8e467b7a476d01965510c5d18.png': u'archer',
            u'5ca476c2166b399e3ec92e8008544fdbea75b6a2.png': u'marauder',
            u'e2a98c81ca279607fc1706e5e1b11bc08cac2578.png': u'thaumaturge',
            u'9fe08b7e2827a51fc216e6407646ffba716a44b8.png': u'pugilist',

            u'98d95dec1f321f111439032b64bc42b98c063f1b.png': u'blackmage',
            u'7a72ef2dc1918f56e573dd28cffcec7e33a595df.png': u'bard',
            u'ee5788ae748ff28a503fecbec2a523dbc6875298.png': u'scholar',
            u'c460e288d5db83ebc90d0654bee6d0d0a0a9582d.png': u'whitemage',
            u'626a1a0927f7d2510a92558e8032831264110f26.png': u'paladin',
            u'2c38a1b928c88fd20bcc74fe0b4d9ba0a8f56f67.png': u'summoner',
            u'36ce9c4cc01581d4f900102cd51e09c60c3876a6.png': u'dragoon',
            u'8873ffdf5f7c80770bc40f5b82ae1be6fa1f8305.png': u'monk',
            u'2de279517a8de132f2faad4986a507ed728a067f.png': u'warrior',

            u'd41cb306af74bb5407bc74fa865e9207a5ce4899.png': u'carpenter',
            u'aab4391a4a5633684e1b93174713c1c52f791930.png': u'armorer',
            u'605aa74019178eef7d8ba790b3db10ac8e9cd4ca.png': u'goldsmith',
            u'343bce834add76f5d714f33154d0c70e99d495a3.png': u'alchemist',
            u'86f1875ebc31f88eb917283665be128689a9669b.png': u'culinatian',
            u'131b914b2be4563ec76b870d1fa44aa8da0f1ee6.png': u'weaver',
            u'6e0223f41a926eab7e6bc42af7dd29b915999db1.png': u'blacksmith',
            u'f358b50ff0a1b1dcb67490ba8f4c480e01e4edd7.png': u'leatherworker',

            u'289dbc0b50956ce10a2195a75a22b500a648284e.png': u'fisher',
            u'937d3313d9d7ef491319c38a4d4cde4035eb1ab3.png': u'botanist',
            u'8e82259fcd979378632cde0c9767c15dba3790af.png': u'miner',
        }
        current_class = img_classes.get(img_name)
        if not current_class:
            log.msg('Unknown class image : {}'.format(img_url),
                    level=log.ERROR)
            return u'unknown'
        else:
            return current_class

    def get_current_gear(items_list):

        # About i.strip() test :
        # Sometimes, the selected elements contain irrelevant items that are
        # strings made only of newlines and/or tabs.
        # Those elements are filtered with strip() for once stripped, they are
        # equal to empty strings which translates as False.
        items = [i for i in items_list[::2] if i.strip()]
        ilv = [int(i.split()[-1]) for i in items_list[1::2] if i.strip()]

        log.msg('Item levels = {}'.format(ilv), level=log.DEBUG)
        log.msg('{} items, {} ilvs'.format(len(items), len(ilv)),
                level=log.DEBUG)

        gear = []
        for i in xrange(min(len(items), len(ilv))):

            item_name = items[i]
            item_level = ilv[i]

            cleaned_name = item_name.lower().replace(' ', '').replace('\'', '')
            name_md5 = hashlib.md5(cleaned_name).hexdigest()
            item_zam_id = CharacterLoader.item_name_to_id.get(name_md5)

            if not item_zam_id:
                log.msg("x Couldn't resolve item ID for {} (md5: {}".format(
                        item_name, name_md5), level=log.ERROR)

            gear.append({
                'name': item_name,
                'ilv': item_level,
                'id': item_zam_id,
            })



        return gear

    default_output_processor = TakeFirst()

    id_in = MapCompose(get_character_id)
    url_in = MapCompose(get_full_character_url)
    rank_in = MapCompose(strip_tabs_newlines)

    race_in = MapCompose(get_race)
    ethnic_group_in = MapCompose(get_ethnic_group)
    gender_in = MapCompose(get_gender)

    gc_in = MapCompose(get_gc)
    gc_rank_in = MapCompose(get_gc_rank)

    levels_in = Compose(clean_levels, get_levels)
    current_class_in = MapCompose(get_class_from_miniature)
    current_gear_in = Compose(get_current_gear)
    current_gear_out = Identity()
