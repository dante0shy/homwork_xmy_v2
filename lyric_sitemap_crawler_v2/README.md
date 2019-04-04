## Synopsis

This is a final project for the Data Science class.
It requires a running elasticsearch on localhost.

## Installation

Order of run of the project:<br /><br />
spiders/sitemapcrawl.py<br />
Crawls the sitemap of the lyrics site and saves HTML files.<br />
elastic_scripts/lyrics_songs_extract.py<br />
Parses the HTML files to songs in JSON format.<br />
elastic_scripts/elastic_indexer.py<br />
Indexes songs to Elasticsearch<br />
analysys/genrewordcloud.py<br />
Generates word clouds of songs per genre <br />
analysys/generate_vocabsize.py<br />
Generates graphs of term frequencies per genre.<br />
analysys/generate_vocabsize_per_year.py<br />
Generates graphs of term frequencies per year.<br />

## Contributors

Yizhar Gilboa (https://github.com/xargil), Omri Avrahami (https://github.com/devomri), Amit Mandelbaum (https://github.com/mangate). 