#!/usr/bin/python3

import subprocess
import io
import sys
import os
import fnmatch

p = ''
for file in os.listdir('.'):
  if fnmatch.fnmatch(file, '*.pdf'):
    temp = file.split('.')
    filename = p.join(('./text/',temp[0], '.txt'))

    subprocess.run(['pdftotext', file, filename])

