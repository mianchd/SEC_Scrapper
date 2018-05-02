import csv
import re
import requests
import sys

def getCIK(list_):

	URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
	CIK_RE = re.compile(r'.*CIK=(\d{10}).*')

	cik_dict = {}
	for Symbol in list_[10:20]:
		try:
			f = requests.get(URL.format(Symbol), stream = True)
		except:
			print("Problem connecting to the SEC Server")

		results = CIK_RE.findall(f.text)
		if len(results):
			cik_dict[str(Symbol).lower()] = str(results[0])
		print('Got CIK: {} for Symbol: {}'.format(str(results[0]), str(Symbol)))
	
	return cik_dict

# Pass pointer to the dictionary to update it
def getCIK_update(dict_list, writer_):

	URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
	CIK_RE = re.compile(r'.*CIK=(\d{10}).*')

	for company in dict_list:
		# try:
		f = requests.get(URL.format(company['Symbol']), stream = True)
		# except:
		# 	print("Problem connecting to the SEC Server")
		# 	sys.exit()

		results = CIK_RE.findall(f.text)
		if len(results):
			company['CIK'] = str(results[0])
		else:
			company['CIK'] = str(0000000000)
		print('Got CIK: {} for Symbol: {}'.format(company['CIK'], company['Symbol'])) # company['CIK']
		try:
			writer_.writerow(company)
		except:
			print("Couldn't write {}".format(company))

# symbols_list = []
symbols_names_dict_list = []
with open('company_symbols_and_names_new.csv') as csvDataFile:
	csvReader = csv.DictReader(csvDataFile)
	for row in csvReader:
		symbols_names_dict_list.append(row)

# symbols_list = []
# for company in symbols_names_dict_list:
# 	symbols_list.append(company['Symbol'])

# getCIK_update(symbols_names_dict_list)



temp_dict_list = [
		{'Symbol':'AAPL', 'Name':'Apple Inc.', 'CIK':'000000211'},
		{'Symbol':'MSFT', 'Name':'Microsoft Corp.', 'CIK':'000641654'},
		{'Symbol':'GOOL', 'Name':'Google Inc.', 'CIK':'0000311133'}
		]
# temp_dict = {'MSFT':'000465466','AAPL':'12341234','GOOL':'000345234'}

with open('test1.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)

    # Writing as dictionary using list of dictionaries (one dictionary per company)
    fieldnames = ('Symbol', 'Name', 'CIK')
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    # for row in symbols_names_dict_list:
    #     writer.writerow(row)
    getCIK_update(symbols_names_dict_list, writer)
    # Single dictionary with all companies as Symbol:CIK pairs
    # for key, value in temp_dict.items():
    #    writer.writerow([key,value])

print("Data Saved to File")