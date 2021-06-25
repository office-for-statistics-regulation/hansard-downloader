from datetime import datetime, timedelta
import sys

import requests
from bs4 import BeautifulSoup as Soup
import pandas as pd

import config


def scrape_hansard(date):
	"""Scrapes Hansard publications for a certain date.

	Keyword arguments:
	date -- the date (in YYYY-MM-DD format)

	Output:
	A dataframe for the scraped data, saved to same folder as script
	"""

	url = 'https://hansard.parliament.uk/commons/' + date
	response = requests.get(url, timeout=5)
	page_content = Soup(response.content, "html.parser")
	folders = page_content.find_all("div", attrs={"class": "card-folder"})

	folder_name = ''
	folder_desc = ''

	folder_name_lst = []
	folder_desc_lst = []
	sub_folder_name_lst = []
	card_lst = []
	link_lst = []
	text_lst = []
	stats_cited = []

	for folder in folders:
		# Searching just for H2 text which denotes the folder name of the publication
		if len(folder.find_all('h2')) > 0:
			folder_name = folder.text.split("\n")[2]
			folder_desc = folder.text.split("\n")[3]
			sub_folder_name = ''

		else:
			# Otherwise it's a subfolder
			sub_folder_name = folder.text.split("\n")[2]

		cards = folder.find_all("a", attrs={"class": "card card-section"})
		for card in cards:

			if 'View all' not in card.text:
				# Gets name of the card
				card_lst.append(card.text.split('\r\n')[1].strip())

				# Gets each card in each folder, finds it's URL link
				link = 'https://hansard.parliament.uk/' + card.attrs.get('href')
				folder_name_lst.append(folder_name)
				folder_desc_lst.append(folder_desc)
				sub_folder_name_lst.append(sub_folder_name)
				link_lst.append(link)

				# Goes to the relevant URL and downloads the txt file
				response = requests.get(link, timeout=5)
				page_content = Soup(response.content, "html.parser")
				download_url = 'https://hansard.parliament.uk' + page_content.find("a", attrs={"class": "icon-link"}).attrs.get('href')
				text = requests.get(download_url).content.decode("utf-8")

				# Searches through the text for paragraph where numerical values exist
				paras = text.split('\r')
				stats_cited_tmp = []
				for para in paras:
					if any(word in para for word in config.stats_search_terms):
						words = para.split(' ')
						for word in words:
							if word.isnumeric():
								stats_cited_tmp.append(para.strip('\n'))

				text_lst.append(text)
				stats_cited.append(stats_cited_tmp)

	df = pd.DataFrame(list(zip(folder_name_lst, folder_desc_lst, sub_folder_name_lst, card_lst, link_lst,
							   text_lst, stats_cited)),
					  columns=['Folder', 'Description', 'Subfolder', 'Card', 'Link', 'Text', 'Stats'])

	df['date_collected'] = datetime.now().strftime('%d/%m/%Y')

	# Keep a dataframe with the raw text in
	df_text = df.drop('Stats', 1)

	# Make a long dataframe with each paragraph in that has a statistic referenced
	df_stats = df.drop('Text', 1)
	df_stats = df_stats[~df_stats.Stats.str.len().eq(0)] # Drop empty Stats rows
	df_stats = df_stats.explode('Stats')
	df_stats = df_stats.drop_duplicates() # Drop duplicates because some sentences may have more than one statistic sourced


	if len(df) == 0:
		print(f"No records found from Hansard for {date}")
		return

	else:
		df_text = df_text[df_text.Card != ''] # Drop empty Card column entries as these will be repeats of Cards below
		df_text.to_csv(f"output/hansard-{date}.csv", index=False)

		df_stats = df_stats[df_stats.Card != ''] # Drop empty Card column entries as these will be repeats of Cards below
		df_stats.to_csv(f"output/hansard-{date}-stats.csv", index=False)

		print(f"Found {len(df_text)} records and {len(df_stats)} statistics mentioned in Hansard for {date}")
		return 'Complete'


if __name__ == '__main__':
	if len(sys.argv[1:]) == 0:
		date = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
	else:
		date = sys.argv[1:][0]
	scrape_hansard(date)