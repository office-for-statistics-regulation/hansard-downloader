## hansard downloader

Uses BeautifulSoup and requests packages to download data from [Hansard](https://hansard.parliament.uk/) for the specified days debate. Saves these into a dataframe.

### Getting

To clone locally use:

`git clone https://github.com/office-for-statistics-regulation/hansard-downloader`

### Setting

To install requirements `cd` to the cloned folder and use:

`pip install -r requirements.txt`

### Using

To run either use:

`python hansard-downloader.py`

to download yesterday's Hansard data. Or to specify a date use:

`python hansard-downloader.py YYYY-MM-DD`

The dataframe will be saved as a CSV file in the outputs folder.

### Example

A jupyter notebook example of the working code can be found in the notebook folder. 
