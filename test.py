# -*- encoding: utf-8 -*-

import requests

r = requests.get('http://lab1.xseclab.com/base6_6082c908819e105c378eb93b6631c4d3/index.php', headers={'User Agent':'HAHA'})
r.encoding = 'utf-8'
print(r.text)