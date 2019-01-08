from __future__ import print_function
import csv
import requests
import sys
import os # mkdir
import shutil # rmtree
import matplotlib
import pdb
import math
import datetime
import time
from datetime import datetime
from datetime import timedelta
matplotlib.use('agg')
from matplotlib import pyplot
from pathlib import Path
from functools import reduce
import _thread

# code based on:
# https://www.robustperception.io/prometheus-query-results-as-csv and
# https://medium.com/@aneeshputtur/export-data-from-prometheus-to-csv-b19689d780aa

metric_count = 0

def main():
  if len(sys.argv) != 7:
    print('Usage: {0} http://localhost:30000 duration(1m,2h,...) destination_dir_path begin_test_day (dd/mm/aa) begin_test_hour (hh:mm:ss) step'.format(sys.argv[0]))
    sys.exit(1)

  prometheus_url = sys.argv[1]
  duration=sys.argv[2][:-1]
  time_unity = sys.argv[2][-1]
  destination_dir_path=sys.argv[3]
  begin_test_day = sys.argv[4]
  begin_test_hour=sys.argv[5]
  step=int(sys.argv[6])

  create_dir(destination_dir_path)
  data_folder = Path(destination_dir_path)
  start = datetime.strptime(begin_test_day + ' ' + begin_test_hour, "%d/%m/%y %H:%M:%S")
  start_formated, end_formated = format_start_end_time(start, duration, time_unity)
  metric_names=get_metrix_names(prometheus_url)

  
  for metric_name in metric_names:
    try:
      print("Metrics already evaluated: {0} of {1}".format(metric_count, len(metric_names)))

      time_series = get_metric_time_series(prometheus_url, metric_name, start_formated, end_formated)

      for index, time_serie in enumerate(time_series):
        thread.start_new_thread(generate_time_serie_csv, (prometheus_url, time_serie, start_formated, end_formated, step, metric_name, index, data_folder))

    except Exception as e:
      print("\nNao foi possivel gerar "+ metric_name)
      print("Exception: ")
      print(e)

def generate_time_serie_csv(prometheus_url, time_serie, start_formated, end_formated, step, metric_name, index, data_folder):
  results = request_time_serie_values(prometheus_url, time_serie, start_formated, end_formated, step)

  if 'result' in results and len(results['result']) > 0:
    result = results['result'][0]
  elif 'result' in results:
    result = results['result']
    print("Single results: {0}".format(str(results)))
  else:
    raise Exception("result with unknwon form: {0}".format(str(result)))

  if 'metric' in result and 'values' in result: 
    file_name = metric_name + str(index) + '.csv'
    file_name = data_folder / file_name

    with open(str(file_name), 'w') as csvfile:
      metric_info = result['metric']
      headers = [i for i in metric_info.keys()]
      headers.sort()
      static_values = [metric_info[key] for key in headers]

      writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
      writer.writerow(['timestamp'] + headers + ['value'])

      for value in result['values']:
        csv_row = [value[0]] + static_values +  [value[1]]
        writer.writerow(csv_row)

  global metric_count
  metric_count = metric_count + 1 

def format_start_end_time(start, duration, time_unity):
  duration_int = int(duration) * getFormatInSeconds(time_unity)
  offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
  offset = offset / (-3600)
  offsetFormatted = '.000' + convertToHourFormat(offset)
  end_test_date = start + timedelta(seconds=duration_int)
  start_formated = start.isoformat() + offsetFormatted
  end_formated = end_test_date.isoformat() + offsetFormatted
  return start_formated, end_formated

def make_request(url, error_message, params={}):
  response = requests.get(url, params=params, timeout=120)
  data = response.json()['data']

  if not response or response.status_code != requests.codes.ok or not data:
    raise Exception(error_message + "\nURL: " + url + "\nParams: " + params + "\nReponse: " + response)

  return data

def request_time_serie_values(url, time_serie, start, end, step):
  endpoint = '{0}/api/v1/query_range'.format(url)
  metric_name = time_serie.pop('__name__')
  prometheus_query = create_prom_query(metric_name, time_serie)
  params = {'query': prometheus_query, 'start': start, 'end': end, 'step': str(step) + 's' }
  data = make_request(endpoint, "It wasn't possible to retrive time serie values", params)

  return data

def create_prom_query (metric_name, time_serie):
  prometheus_query = ""
  for label, value in time_serie.items():
    pair = label.replace("'","") + "=" + '"' + value + '"'
    prometheus_query = prometheus_query + pair + ","
  prometheus_query = prometheus_query[0:len(prometheus_query) - 1]
  prometheus_query = metric_name+ "{" + prometheus_query + "}"
  return prometheus_query

def get_metrix_names(url):
  endpoint = '{0}/api/v1/label/__name__/values'.format(url)

  return make_request(endpoint, "It wasn't possible to get the metrics names.")

def get_metric_time_series(url, metric_name, start, end):
  endpoint = '{0}/api/v1/series'.format(url)
  request_params={'match[]': metric_name, 'start': start, 'end': end }

  return make_request(endpoint, "It wasn't possible to get the time series set.", params=request_params)

def create_dir(destination_dir_path):
  try:
    shutil.rmtree(destination_dir_path)
  except Exception as e:
    print("Directory not deleted")
  try:
    os.mkdir(destination_dir_path)
  except Exception as e:
    print("Error at the creation of directory")
    sys.exit(1)

def get_hour_in_minutes(begin_test_hour):
  hour = int(begin_test_hour.split(':')[0])
  return ((24 - hour) * 60)

def get_minute(begin_test_hour):
  return (int(begin_test_hour.split(':')[1]))

def convertToHourFormat(offsetParam):
  hourFormat = '+' if (offsetParam > 0) else '-'
  offset = abs(int(offsetParam))
  hourFormat = hourFormat + str(offset).zfill(2) + ':00'
  return hourFormat

def getFormatInSeconds(timeFormat):
  if timeFormat == 'h':
    return 3600
  if timeFormat == 'm':
    return 60
  return 1

if __name__ == "__main__":
  main()
