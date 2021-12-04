from volleyball.stat.StatMaker import *
from volleyball.scraper.LinkProcessor import LinkProcessor


link_processor = LinkProcessor([LinkProcessor.WOMEN], [LinkProcessor.REGULAR_SEASON, LinkProcessor.PLAY_OFF, LinkProcessor.CHAMP], list(range(2020, 2021)), list(range(1, 3)))
link_processor.make_round_number()
stat = Stat(link_processor.links)

stat.fill_games()
stat.fill_sets()
stat.fill_messages()
stat.fill_rallies()
