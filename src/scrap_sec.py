"""
Program that scraps SEC website for companies 
searching various fillings for keyword matches
"""

__author__ = 'Mian A. Shah'
__description__ = 'SEC EDGAR Report Generation Program'

import os
import sys
import logging
import argparse
import time
import csv
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

logger = None

if not os.path.isfile('./geckodriver.exe'):
	print("Please make sure 'geckodriver.exe' exist in current directory")
	sys.exit(0)

os.environ['MOZ_HEADLESS'] = '1'

keywords = ['lawsuit', 'litigation']

formlist = ['10-K', '8-K', '10-Q']

def read_company_dict():
	"""
	Function that reads CSV file for list of companies
	Supplied by command line argument.
	"""
	company_dict = []

	default_input_file = 'generated_file_with_CIKs.csv'

	parser = argparse.ArgumentParser()
	parser.add_argument("--input",
						dest="input_file",
						required=False,
						default=default_input_file,
						help="Input File Containing List of Companies")

	args = parser.parse_args()

	print("Using {} as input".format(args.input_file))

	try:
		with open(args.input_file) as csvDataFile:
			csvReader = csv.DictReader(csvDataFile)
			for row in csvReader:
				if int(row['CIK']) > 0:
					company_dict.append(row)
			return company_dict
	except FileNotFoundError as e:
		print("Please make sure the current directory has {} \n \t\t\t\t\t\t\tOR\nPlease provide the path to input file as --input_file".format(default_input_file))
		sys.exit(0)


def get_statistics(company_dict, writer_):
	"""
	Main Function that scraps the Website and writes found data to disk.
	"""
	browser = webdriver.Firefox()
	total_companies = len(company_dict)
	companies_done = 0
	for company in company_dict:
		print('----------------------------------------------------------------------')
		print("Processing {} with CIK: {}".format(company['Name'], company['CIK']))
		logger.debug("Processing {} with CIK: {}".format(company['Name'], company['CIK']))
		for form_type in formlist:
			url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='+company['CIK']+'&type='+form_type+'&dateb=&owner=exclude&count=40'
			browser.get(url)
		 
			try:
				browser.find_element_by_id('documentsbutton').click()
				logger.debug("Document found for {}".format(form_type))
				# Can get multiple instances of same form for different periods
				
			except NoSuchElementException as e: 
				logger.error("{} Not Found.".format(form_type))
				print("{} Not Found.".format(form_type))
				continue

			try:
				Dates = {}
				Dates['filing_date'] = browser.find_element_by_xpath("//div[@class='formContent']/div[1]/div[2]").text
				Dates['report_period'] = browser.find_element_by_xpath("//div[@class='formContent']/div[2]/div[2]").text
			except NoSuchElementException as e:
				logger.error("error occurred on {} when obtaining Dates for {}\n{}".format(browser.current_url, form_type, e))
				print("Couldn't retrieve Dates")
				continue

			try:
				link = browser.find_element_by_xpath("//table[@class='tableFile']/tbody/tr[2]/td[3]/a").text
				# browser.find_element_by_partial_link_text(re.findall(r'\d+', form_type)[0]).click()
				browser.find_element_by_link_text(link).click()
				logger.debug("Document leads to link: {}".format(link))
			except NoSuchElementException as e:
				logger.error("Error: When finding link for {}\n{}".format(form_type, e))
				continue

			html_source = browser.page_source.lower()
			# This just gets the text instead of the raw page source but is much slower
			# html_source = browser.find_element_by_xpath("//*").text # get text inside all elements - try only p
			keywords_dict = {}	
			for keyword in keywords:
				keywords_dict[keyword] = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(keyword), html_source))
			html_source = None

			Form_dict = {}
			Form_dict['dates'] = Dates
			Form_dict['keywords_stats'] = keywords_dict
			Form_dict['URL'] = browser.current_url
			company[form_type]= [Form_dict] # Each form has 2 dictionaries and 1 URL
			# can make a dictionary of froms and assign it to new company key "Forms_Data"
		
		if '10-K' in company:
			writer_.writerow(company)
			logger.debug("Data successfully writen for {}\n".format(company['Name']))
		else:
			print("Data writing operation aborted.")
			logger.warning("Data Writing Aborted for {}--------X\n".format(company['Name']))
		
		companies_done+=1
		print("{} processed.\t|\tProgress: {}/{}".format(company['Name'], companies_done, total_companies))
		
	browser.quit()

def main():

	start_time = time.time()
	x = read_company_dict()
	print("Got the Companies")

	time_format = '%d-%b-%Y_%H-%M-%S'
	report_time = time.strftime(time_format)

	new_dir = 'Report__{}'.format(report_time)
	os.makedirs(new_dir)

	logging.basicConfig(
		format='%(asctime)s -- %(message)s',
		datefmt=time_format, 
		filename='{}/debug_{}.log'.format(new_dir, report_time), 
		level=logging.WARNING, 
		filemode='w')

	global logger
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)

	with open('{}/CSV_Report_{}.csv'.format(new_dir, report_time), 'w') as csv_file:
		writer = csv.writer(csv_file)
		fieldnames = ('Symbol', 'Name', 'CIK', '10-K', '10-Q', '8-K')
		writer = csv.DictWriter(csv_file, lineterminator='\n', fieldnames=fieldnames)
		writer.writeheader()
		get_statistics(x, writer)
	total_time = time.time() - start_time
	print("Time taken to complete report: {}".format(total_time))
	logger.debug("Time taken to complete report: {}".format(total_time))

if __name__ == '__main__':
	main()
