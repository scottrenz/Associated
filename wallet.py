import hashlib
import requests

import sys
import json

if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()


    r = requests.get(url=node + "/chain")
     # Handle non-json response
    try:
        data = r.json()
        # print(data)
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(r)
    total = 0
    trans = []        
    for i in range(0,len(data['chain'])):
        if data['chain'][i]['transactions']:
            if id == data['chain'][i]['transactions'][0]['recipient']:
                total +=data['chain'][i]['transactions'][0]['amount']
                trans.append(data['chain'][i]['transactions'])
    print("Total amount of coins for "+ id,total)
    print('All transactions for '+id)
    for i in trans:
        print(i)

