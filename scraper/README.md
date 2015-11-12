Runthrough of how the files are organized, and how you can efficiently use these
pipelines.

fanduel_player_pipeline.py parses data from the Fanduel Players Sheet, available on the webiste.
You need to download (manually, for now) this every day and point the python file to look at that file.
  
daily_lineup_pipeline.py calls rotogrinder_depth_chart.py (which is a scraper for all the depth charts
for a particular day) to get JSON-formatted data of relevant depth charts for teams involved in each
game

update_stats_pipeline.py takes data from NBA Stuffers (so far, only player data, but can easily be
modularized to support the other data types as well)

query_engine.py is an interface to support stat queries throughout the season. Eventually we will create
a TeamQueryEngine and PlayByPlayQueryEngine.

@TODO: Refactor server.py to call the LineupAnalyzer instead of the original engine we had
@TODO: Write interface for LineupAnalyzer 
@TODO: Write efficient caching mechanism for LineupAnalyzer
@TODO: Improve LineupAnalyzer so that it can refresh daily and be a persistent system
@TODO: Aggregate injury information from FanDuel and the original depth chart data we have
@TODO: Scrape expert opinions, incorporate into system 
@TODO: Get rid of get_player_comments_pipeline.py, it's useless once LineupAnalyzer replaces
the original system