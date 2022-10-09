# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 00:36:59 2022

@author: Ben-Gaming
"""

import os
import urllib.request

path = '\\'.join(os.path.realpath(__file__).split('\\')[:-1]) + '\\'

response = urllib.request.urlopen(
    'https://raw.githubusercontent.com/bepalmet/URF-picker-2/main/URF_picker_2.pyw'
    ).read().decode('utf-8').replace('\n', '')

with open(path, 'w') as file:
    file.write(response)
