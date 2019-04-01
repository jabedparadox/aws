#!/usr/bin/python
#!/usr/bin/python3
#!/usr/bin/env python
#!/usr/bin/env python3

# -*- coding: utf8 -*-
# aws captcha tst
# date                 :- 30/03/2019
# author               :- Md Jabed Ali(jabed)

import pytesseract
import sys
import os
import argparse
import requests
import time
from subprocess import check_output
try:
    import Image
except ImportError:
    from PIL import Image

apikey = " "
proxy = "127.0.0.1:0000"
website = " "
payload = {
	'method' : '',
	'key' : apikey,
	#'proxy':'127.0.0.1:0000',
    #'proxytype':"http/https",
	'body' : '',
	#'action': 'getbalance'
}

request = requests.Session()
pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_tesseract_executable>'

value=Image.open("captcha.jpg")
text = pytesseract.image_to_string(value, config='')    
print("Captcha text:",text)

#print(pytesseract.image_to_string(Image.open('test.jpg')))
#print (os.path)

#Online captcha solving "https://2captcha.com/" "http://www.imagetyperz.com/"
#def 2captcha():
	resp = requests.get("http://2captcha.com/in.php", params=payload)
	captchaid = (captchaid.text).split("|")[1]
	captans = requests.get("http://2captcha.com/res.php?key=" + apikey + "&action=get&id=" + captchaid).text
	while "CAPCHA_NOT_READY" in captans:
		captans = requests.get("http://2captcha.com/res.php?key=" + apikey + "&action=get&id=" + captchaid).text
		time.sleep()
	captans = captans.split("|")[1]
	#print(captans)
	return captans
		
def solvecaptcha(path):
	print("Resizing Image")
	check_output(['convert', path, '-resize', '600', path])
	return pytesseract.image_to_string(Image.open(path))

if __name__=="__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('path',help = 'Captcha path')
	args = argparser.parse_args()
	path = args.path
	print('Resolving Captcha')
	captcha_text = solvecaptcha(path)
	print('Extracted Text',captcha_text)
