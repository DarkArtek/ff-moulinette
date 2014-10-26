all:
	rm -f members.json
	scrapy crawl lodestone_en -o members.json -t json -L INFO
	json_pp < members.json > members_clean.json
