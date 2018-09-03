import csv
import requests
import sys
import ipdb # for debug. Ex: python -m ipdb cvs_export.py http://localhost:30000 30s dir_path
import os # mkdir 
import shutil # rmtree

# code based on: 
# https://www.robustperception.io/prometheus-query-results-as-csv and 
# https://medium.com/@aneeshputtur/export-data-from-prometheus-to-csv-b19689d780aa

def GetMetrixNames(url):
    response = requests.get('{0}/api/v1/label/__name__/values'.format(url))
    names = response.json()['data']
    #Return metrix names
    return names

def create_dir(path):
    try:  
        shutil.rmtree(path)
    try:
        os.mkdir(path)
    except OSError:  
        print("Error at the creation of directory")
        sys.exit(1)

"""
Prometheus hourly data as csv.
"""

if len(sys.argv) != 4:
    print('Usage: {0} http://localhost:9090 interval(1m,2h,...) dir_path'.format(sys.argv[0]))
    sys.exit(1)

metrixNames=GetMetrixNames(sys.argv[1])
interval=sys.argv[2]
path=sys.argv[3]

for metrixName in metrixNames[0:1]:
    create_dir(path)
    
    with open(path + '/' + metrixName + '.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        
        response = requests.get('{0}/api/v1/query'.format(sys.argv[1]), params={'query': metrixName+'['+interval+']'})
        results = response.json()['data']['result']
        
        # Build a list of all labelnames used.
        #gets all keys and discard __name__
        labelnames = set()

        for result in results:
            labelnames.update(result['metric'].keys())

        # Canonicalize
        labelnames.discard('__name__')
        labelnames = sorted(labelnames)

        # Write the samples.
        writer.writerow(['name', 'timestamp', 'value'] + labelnames)

        for result in results:
            for value in result['values']:
                l = [result['metric'].get('__name__', '')]
                l.append(value[0])
                l.append(value[1])
                for label in labelnames:
                    l.append(result['metric'].get(label, ''))
                writer.writerow(l)
