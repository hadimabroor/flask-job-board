import re

def trim(s):
	re.sub('[\s+]', '', s)