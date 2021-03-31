from datetime import datetime, timedelta
import sys

import requests
from bs4 import BeautifulSoup as Soup
import pandas as pd


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
			# Gets name of the card
			card_lst.append(card.text.split('\r\n')[1].strip())

			# Gets each card in each folder, finds it's URL link
			link = 'https://hansard.parliament.uk/' + card.attrs.get('href')
			folder_name_lst.append(folder_name)
			folder_desc_lst.append(folder_desc)
			sub_folder_name_lst.append(sub_folder_name)
			link_lst.append(link)

			# Goes to the relevant URL
			response = requests.get(link, timeout=5)
			page_content = Soup(response.content, "html.parser")
			content = page_content.find("div", attrs={"class": "col-lg-9 primary-content"})
			paras = content.find_all("p")

			text_out = ''
			for para in paras:
				# Collects all relevant text for the page
				if len(para.text) > 5:
					text_out = text_out + ' ' + para.text
			text_lst.append(text_out)

	df = pd.DataFrame(list(zip(folder_name_lst, folder_desc_lst, sub_folder_name_lst, card_lst, link_lst,
							   text_lst)),
					  columns=['Folder', 'Description', 'Subfolder', 'Card', 'Link', 'Text'])

	df['date_collected'] = datetime.now().strftime('%d/%m/%Y')

	if len(df) == 0:
		print(f"No records found from Hansard for {date}")
		return

	else:
		df = df[df.Card != ''] #Drop empty Card column entries as these will be repeats of Cards below
		df.to_csv(f"output/hansard-{date}.csv", index=False)
		print(f"Found {len(df)} records from Hansard for {date}")
		return 'Complete'


if __name__ == '__main__':
	if len(sys.argv[1:]) == 0:
		date = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
	else:
		date = sys.argv[1:][0]
	scrape_hansard(date)