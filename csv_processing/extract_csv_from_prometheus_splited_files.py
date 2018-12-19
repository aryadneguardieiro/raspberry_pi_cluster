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

# code based on:
# https://www.robustperception.io/prometheus-query-results-as-csv and
# https://medium.com/@aneeshputtur/export-data-from-prometheus-to-csv-b19689d780aa

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
  start_formated, end_formated = formart_start_end_time(start, duration, time_unity)
  metric_names=get_metrix_names(prometheus_url)

  for metric_name in metric_names:
    try:
      time_series = get_metric_time_series(prometheus_url, metric_name, start_formated, end_formated)

      for index, time_serie in enumerate(time_series):
        #open a new thread for processing each time serie?
        values = request_time_serie_values(prometheus_url, time_serie, start_formated, end_formated)

        file_name = metric_name + index + '.csv' # a concatenation is not used here because of the special chars that the values can have
        file_name = data_folder / file_name

        with open(file_name, 'w') as csvfile:
          writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
          writer.writerow(['name', headers, 'timestamp', 'value'])

          for timestamp,value in result['values']:
            csv_row.append(tag)
            csv_row.append(timestamp)
            csv_row.append(value)
            writer.writerow(csv_row)

    except Exception as e:
      print("\nNao foi possivel gerar "+ metric_name)
      print("Exception: ")
      print(e)

def formart_start_end_time(start, duration, time_unity):
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
    print("error_message")
    print("Url: " + url)
    print("Params: " + params)
    print("Response: ")
    print(response)
    sys.exit(1)

  return data

def request_time_serie_values(url, time_serie, start, end):
  endpoint = '{0}/api/v1/label/query_range'.format(url)
  prometheus_query = str(time_serie).replace(':', '=').replace("'",'"')
  params = {'query': prometheus_query, 'start': start, 'end': end }

  pdb.set_trace()

  return make_request(endpoint, "It wasn't possible to retrive time serie values", params)


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

# time_series is a list like: [{{'metric': {label1: 'lala', ...}, 'value': [['timestamp', 'value'], ... ]}}]
# so each time_serie is a dic containing metric's labels 'metric': {label1: 'lala', ...} 
# and a list of tuples with timestamps and values [['timestamp', 'value'], ...]
def request_time_serie_values():
  request_params = {'query': c_ntrixName, 'start': start_formated, 'end': end_formated, 'step': '1s'}
  response = s.get('{0}/api/v1/query_range'.format(sys.argv[1]), params=request_params, timeout=120)
  return response.json()['data']['result']['values']

if __name__ == "__main__":
  main()
