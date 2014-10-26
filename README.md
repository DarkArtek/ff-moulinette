ff-moulinette : a crawler for FF14's Lodestone
===

### Features and limitations

This crawler fetches data from all characters within the same Free Company (FC)
using character sheets publicly available at http://www.finalfantasyxiv.com/

Collected data for each character:

	* name, Lodestone ID and character sheet URL
	* race, gender, city-state, GC rank...
	* level for each class
	* current class and last equipped gear set
	* gear set contains item names, ILV, and IDs on XIVdb database (http://xivdb.com)

Item IDs are resolved using the XIVPads *dirty json* (http://xivpads.com/items.json).
Altough this method has limitations (the json file is not really up-to-date), it
is possible to use the XIVdb tooltip system quite directly.
Such limitations might be adressed with later versions. 

See http://xivdb.com/?tooltip for more information on XIVdb's tooltip system.


### Install and use

This cralwer is build using the Scrapy toolkit. Using a Python virtual
environment is the best way to test this software. The `requirements.txt`
contains the project's requirements.

Once you have your environment all set up, get to the `src` sub-folder:

	* set you FC ID in the `moulinette/settings.py` file
	* run the Makefile (using `make` will do the trick)
	* results are saved in the `members.json` file


### Roadmap

Altough there is no real roadmap for this project, a few things may be improved
lated on :

	- [] use another item ID source instead of XIVpads' json file
	- [] keep track of different gear sets (one for each class)
	- [] something better than a lousy Makefile
	- [] collect underpants

For suggestions or requests, please create a ticket in the issues, it's always
nice to have feedback.

Have fun !