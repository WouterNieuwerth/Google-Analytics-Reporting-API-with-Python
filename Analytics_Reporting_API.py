#@title
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 11:54:03 2019

@author: wouternieuwerth
"""

#------------------------------------------------------------------------------
import pandas as pd

def response_to_df(response):
  """
  Takes a Google Analytics v4 API response and returns it as a Pandas DataFrame.
  """
  list = []
  # get report data
  for report in response.get('reports', []):
    # set column headers
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])
    
    for row in rows:
        # create dict for each row
        dict = {}
        dimensions = row.get('dimensions', [])
        dateRangeValues = row.get('metrics', [])

        # fill dict with dimension header (key) and dimension value (value)
        for header, dimension in zip(dimensionHeaders, dimensions):
          dict[header] = dimension

        # fill dict with metric header (key) and metric value (value)
        for i, values in enumerate(dateRangeValues):
          for metric, value in zip(metricHeaders, values.get('values')):
            #set int as int, float a float
            if ',' in value or '.' in value:
              dict[metric.get('name')] = float(value)
            else:
              dict[metric.get('name')] = int(value)

        list.append(dict)
    
    df = pd.DataFrame(list)
    return df

#------------------------------------------------------------------------------
import random
import time
from apiclient.errors import HttpError

def makeRequestWithExponentialBackoff(analytics, request):
  """Wrapper to request Google Analytics data with exponential backoff.

  The makeRequest method accepts the analytics service object, makes API
  requests and returns the response. If any error occurs, the makeRequest
  method is retried using exponential backoff.

  Args:
    analytics: The analytics service object

  Returns:
    The API response from the makeRequest method.
  """
  for n in range(0, 5):
    try:
      return get_report(analytics, request)

    except HttpError as error:
      if error.resp.reason in ['userRateLimitExceeded', 'quotaExceeded',
                               'internalServerError', 'backendError']:
        time.sleep((2 ** n) + random.random())
      else:
        break

  print ("There has been an error, the request never succeeded.")

#------------------------------------------------------------------------------
from oauth2client.service_account import ServiceAccountCredentials
from geheim import secrets
secrets = secrets()
SERVICE_ACCOUNT_EMAIL = secrets['SERVICE_ACCOUNT_EMAIL']
KEY_FILE_LOCATION = secrets['KEY_FILE_LOCATION']
SCOPES = secrets['SCOPES']
import httplib2
from apiclient.discovery import build
DISCOVERY_URI = secrets['DISCOVERY_URI']

def initialize_analyticsreporting():
  """Initializes an analyticsreporting service object.

  Returns:
    analytics an authorized analyticsreporting service object.
  """

  credentials = ServiceAccountCredentials.from_json_keyfile_name('gaCredentials.json', scopes=SCOPES)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)

  return analytics

#------------------------------------------------------------------------------
def get_report(analytics, request):
  """ Use the Analytics Service Object to query the Analytics Reporting API V4. """
  return analytics.reports().batchGet(
      body=request
  ).execute()

#------------------------------------------------------------------------------
def print_response(response):
  """Parses and prints the Analytics Reporting API V4 response"""

  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])

    for row in rows:
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        print ( header + ': ' + dimension )

      for i, values in enumerate(dateRangeValues):
        print ('Date range (' + str(i) + ')' )
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print ( metricHeader.get('name') + ': ' + value )
