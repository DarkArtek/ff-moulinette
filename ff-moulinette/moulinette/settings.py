# This is the settings file for the ff-moulinette crawler.
#
# This file contains mostly required settings. Other settings depend on Scrapy
# behaviour and are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
# However, you must at least define your free company ID for this crawler to
# work (see below).


################################################################################
#                                                                              #
#                    DEFINE YOUR FREE COMPANY ID HERE                          #
#                                                                              #
################################################################################

# If your FC homemage on the Lodestone is looks something like:
#
#     http://eu.finalfantasyxiv.com/lodestone/freecompany/9231253336202693693/
#
# Then you company ID is "9231253336202693693"

LODESTONE_URL = 'eu.finalfantasyxiv.com'
FREE_COMPANY_ID = '9231253336202693693'

################################################################################


# This crawler uses XIVPads list of item IDs to get XIVdb's ids.
ITEM_ID_URL = 'http://xivpads.com/items.json'


BOT_NAME = 'moulinette'
SPIDER_MODULES = ['moulinette.spiders']
NEWSPIDER_MODULE = 'moulinette.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'moulinette (+http://www.yourdomain.com)'
