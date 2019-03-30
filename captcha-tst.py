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
from subprocess import check_output
try:
    import Image
except ImportError:
    from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_tesseract_executable>'

value=Image.open("captcha.jpg")
text = pytesseract.image_to_string(value, config='')    
print("Captcha text:",text)

#print(pytesseract.image_to_string(Image.open('test.jpg')))
#print (os.path)

#Online captcha solving "https://2captcha.com/" "http://www.imagetyperz.com/"
#def 2captcha():


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
