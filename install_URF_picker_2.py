# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 12:07:51 2022

@author: Ben-Gaming
"""

import os
import urllib.request

path_array = os.path.realpath(__file__).split('\\')[:-1]
path = '\\'.join(path_array) + '\\'
if path_array[-1] != "URF picker 2":
    try:
        os.mkdir(path + "URF picker 2")
        path += "URF picker 2\\"
        os.replace(os.path.realpath(__file__), path + "install_URF_picker_2.py")
    except Exception as e:
        input(e)
        raise SystemExit
        
if not os.path.exists(path + "URF_picker_2.pyw"):
    response = urllib.request.urlopen(
        'https://raw.githubusercontent.com/bepalmet/URF-picker-2/main/URF_picker_2.pyw'
        ).read().decode('utf-8').replace('\n', '')
    
    
    with open(path + "URF_picker_2.pyw", 'w') as file:
        file.write(response)
    #os.system('python' + path + 'URF_picker_2.py')
else:
    input("Already installed. Press Enter to exit")
    raise SystemExit