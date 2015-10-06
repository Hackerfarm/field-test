import requests

#url = 'http://field-test.iv-labs.org/post'
url = 'http://localhost:4489/post'
values = {'identity' : 'bond/james/bond',
          'content' : "{'temperature':28, 'trap':0, 'water':25}"}


r = requests.post(url, data=values)

print r
