import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as Soup
import pandas as pd


def scrape_hansard():
	yesterdays_date = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
	# getting the 'count' of the number of overall publications to determine number of pages
	url = 'https://hansard.parliament.uk/commons/' + yesterdays_date
	response = requests.get(url, timeout=5)
	page_content = Soup(response.content, "html.parser")
	folders = page_content.find_all("div", attrs={"class": "card-folder"})

	folder_name = ''
	folder_desc = ''

	folder_name_lst = []
	folder_desc_lst = []
	sub_folder_name_lst = []
	link_lst = []
	text_lst = []
	stats_lst = []

	for folder in folders:
		if len(folder.find_all('h2')) > 0:
			folder_name = folder.text.split("\n")[2]
			folder_desc = folder.text.split("\n")[3]
			sub_folder_name = ''

		else:
			sub_folder_name = folder.text.split("\n")[2]


		cards = folder.find_all("a", attrs={"class": "card card-section"})
		for card in cards:
			link = 'https://hansard.parliament.uk/' + card.attrs.get('href')
			folder_name_lst.append(folder_name)
			folder_desc_lst.append(folder_desc)
			sub_folder_name_lst.append(sub_folder_name)
			link_lst.append(link)

			response = requests.get(link, timeout=5)
			page_content = Soup(response.content, "html.parser")
			content = page_content.find("div", attrs={"class": "col-lg-9 primary-content"})
			paras = content.find_all("p")

			text_out = ''
			for para in paras:
				if len(para.text) > 5:
					text_out = text_out + ' ' + para.text
			text_lst.append(text_out)

			stats_lst.append([int(s) for s in text_out.split() if s.isdigit()])

	df = pd.DataFrame(list(zip(folder_name_lst, folder_desc_lst, sub_folder_name_lst, link_lst, text_lst, stats_lst)),
					  columns=['Folder', 'Description', 'Subfolder', 'Link', 'Text', 'Stats'])

	df['date_collected'] = datetime.now().strftime('%d/%m/%Y')

	df.to_csv("latest_run.csv")

	print(f"Found {len(df)} records from Hansard")
	return 'Complete'


if __name__ == '__main__':
	scrape_hansard()
