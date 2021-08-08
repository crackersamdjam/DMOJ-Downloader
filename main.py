import datetime
import json
import os
import re
import shutil
import string

lang_map = {
	'BF': 'c',
	'C': 'c',
	'CLANG': 'c',
	'CLANGX': 'cpp',
	'CPP': 'cpp',
	'GO': 'go',
	'JAVA': 'java',
	'NASM': 'asm',
	'PY': 'py',
	'PYPY': 'py',
	'TEXT': 'txt',
}

def get_extension(language):
	prefix = language.rstrip(string.digits) # removes digits after prefix
	if prefix not in lang_map:
		raise Exception(f'Unknown language "{language}"')
	return lang_map[prefix]

categories = {
	# also add link to the contest?
	'AC': 'Appleby Contest',
	'ACC': 'Another Contest',
	'APIO': 'Asia Pacific Informatics Olympiad',
	'BTOI': 'Baltic Olympiad in Informatics',
	'CCC': 'Canadian Computing Competition',
	'CCO': 'Canadian Computing Olympiad',
	'COCI': 'Croatian Open Competition in Informatics',
	'DMOPC': 'DMOJ Monthly Open Programming Contest (formerly Don Mills Open Programming Contest)',
	'DWITE': 'I dont know',
	'ECOO': 'Educational Computing Organization of Ontario Programming Contest',
	'IOI': 'International Olympiad in Informatics',
	'IOI': 'National Olympiad in Informatics (China)',
	'OCC': 'Olympiads Computing Contest',
	'UTSO': 'University of Toronto Schools Open Programming Contest',
	'VALENTINES': 'Valentine\'s Day Contest',
	'VMSS': 'Vincent Massey?',
	'VPEX': 'Victor\'s Programming Exhibition',
	'WAC': 'Wesley\'s Anger Contest',
	'WC': 'Woburn Challenge',
	'Uncategorized': 'Was not assigned anywhere',
}

def get_category(filename):
	prefix = re.search(r"[a-zA-Z]*", filename.upper()).group()
	if prefix in categories:
		return prefix
	#warnings.warn(f'Unknown category for "{filename}, prefix = {prefix}"')
	#raise Exception(f'Unknown category for "{filename}, prefix = {prefix}"')
	return 'Uncategorized'

def run():
	try:
		earlist_date = input('Enter earliest date as YYYY-MM-DD [empty for no limit]\n')
		earlist_date = datetime.datetime.strptime(earlist_date, '%Y-%m-%d').date() if earlist_date else datetime.date.min
		latest_date = input('Enter latest date as YYYY-MM-DD [empty for no limit]\n')
		latest_date = datetime.datetime.strptime(latest_date, '%Y-%m-%d').date() if latest_date else datetime.date.max
	except:
		print('Invalid date.')
		return

	if earlist_date > latest_date:
		print('Earliest date must be earlier than latest date.')
		return
	
	try:
		info = open('submissions/info.json', 'r').read()
		info = json.loads(info)
	except:
		print(f'{os.getcwd()}/submissions/info,json does not exist.')
		return

	if not os.path.exists('sorted'):
		os.mkdir('sorted')

	for i in categories:
		if os.path.exists(f'sorted/{i}'):
			shutil.rmtree(f'sorted/{i}')
		os.mkdir(f'sorted/{i}')
		f = open(f'sorted/{i}/README.md', 'w')
		f.write(f'## {categories[i]}')
		f.close()

	num = len(info)
	done = 0
	print(f'Working on your {num} DMOJ submissions.')

	for i in info:
		current = info[i]
		if current['result'] != 'AC':
			continue
		
		day = current['date'].split('T')[0]
		c = datetime.datetime.strptime(day, '%Y-%m-%d').date()
		
		if c < earlist_date or c > latest_date:
			continue
		
		# print(c)
		name = info[i]['problem']
		destination = get_category(name)
		extension = get_extension(current['language'])
		if not os.path.isfile(f'submissions/{i}.{extension}'):
			raise Exception(f'Can\'t find file submissions/{i}.{extension}')
		os.system(f'cp submissions/{i}.{extension} sorted/{destination}/{name}.{extension}')
		done += 1
		if done % 100 == 0:
			print(f'Completed {done}/{num} submissions.')
	print('All done!')


if __name__ == '__main__':
	run()
	print('Exiting.')

'''
Organize DMOJ solutions
Downloaded data from site
everything is in submissions/
the latest one is the last one that gets kept
'''
