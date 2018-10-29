from __future__ import print_function
import csv
import requests
import sys
import os # mkdir
import shutil # rmtree
import matplotlib
import pdb
import datetime
import math
from datetime import datetime
matplotlib.use('agg')
from matplotlib import pyplot

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
    except OSError:
        print("Directory not deleted")
    try:
        os.mkdir(path)
    except OSError:
        print("Error at the creation of directory")
        sys.exit(1)

def get_hour_in_minutes(end_hour_test):
    hour = int(end_hour_test.split(':')[0])
    return ((24 - hour) * 60)

def get_minute(end_hour_test):
    return (int(end_hour_test.split(':')[1]))

"""
Prometheus hourly data as csv.
"""

if len(sys.argv) != 6:
    print('Usage: {0} http://localhost:30000 interval(1m,2h,...) dir_path end_test_day (dd/mm/aa) end_test_hour (hh:mm:ss)'.format(sys.argv[0]))
    sys.exit(1)

metrixNames=GetMetrixNames(sys.argv[1])
interval=sys.argv[2]
path=sys.argv[3]
end_hour_test=sys.argv[5]
create_dir(path)
s = requests.Session()
offset_til_midnight = get_hour_in_minutes(end_hour_test) - get_minute(end_hour_test)
end_test_date = datetime.strptime(sys.argv[4]+ ' ' + sys.argv[5], "%d/%m/%y %H:%M:%S")
current = 0
total = len(metrixNames)

for metrixName in metrixNames:
    if '_bucket' not in metrixName and '_sum' not in metrixName and '_count' not in metrixName:
        with open(path + '/' + metrixName + '.csv', 'w') as csvfile:
            now = datetime.utcnow()
            #offset = str(offset_til_midnight + (now.hour * 60) + now.minute + days_shift * 3600) + "m";
            time_delta = datetime.now() - end_test_date
            offset = time_delta.days*1440 + math.ceil(time_delta.seconds/60)
            offset = str(offset)+'m'
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            try:
                response = s.get('{0}/api/v1/query'.format(sys.argv[1]), params={'query': metrixName+'['+interval+'] offset ' + offset}, timeout=60)
                results = response.json()['data']['result']
                labelnames = set()

                for result in results:
                    labelnames.update(result['metric'].keys())

                # Canonicalize
                labelnames.discard('__name__')
                labelnames = sorted(labelnames)

                # Write the samples.
                writer.writerow(['name'] + labelnames + ['timestamp', 'value'])

                time_series = {}

                for result in results:
                    for value in result['values']:
                        l = [result['metric'].get('__name__', '')]
                        tag = result['metric'].get('__name__', '')

                        for label in labelnames:
                            l.append(result['metric'].get(label, ''))
                            tag = tag +'_'+ result['metric'].get(label, '')
                        l.append(value[0])
                        l.append(value[1])
                        writer.writerow(l)

                        if tag in time_series:
                           if time_series[tag]['x'][-1] != value[0] and time_series[tag]['y'][-1] != value[1]:
                               time_series[tag]['x'] = time_series[tag]['x'] + [value[0]]
                               time_series[tag]['y'] = time_series[tag]['y'] + [value[1]]
                        else:
                            time_series[tag] = {'x': [value[0]], 'y': [value[1]]}
                current = current + 1
                percentage = current/total * 100
                print(str(math.ceil(percentage)) + "% arquivos gerados (" +str(current) + "/" + str(total) + ")")
            except:
                print("Nao foi possivel gerar "+ metrixName)
