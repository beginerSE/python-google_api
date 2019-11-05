"""Hello Analytics Reporting API V4."""

import argparse
import os
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')

KEY_FILE_LOCATION = ""
SERVICE_ACCOUNT_EMAIL = ''
VIEW_ID = ''


def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.
    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report(analytics):
    # Use the Analytics Service Object to query the Analytics Reporting API V4.
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'pageSize': 10,
                    'dateRanges': [
                        {'startDate': '7daysAgo', 'endDate': 'today'}
                    ],
                    'metrics': [
                        {'expression': 'ga:pageviews'},
                    ],
                    'dimensions': [
                        {'name': 'ga:pagePath'}, {'name': 'ga:pageTitle'}
                    ],
                    'orderBys': [
                        {'fieldName': 'ga:pageviews', 'sortOrder': 'DESCENDING'},
                    ]
                }]
        }
    ).execute()


def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response."""
    for report in response.get('reports', []):
        rows = report.get('data', {}).get('rows', [])
        for row in rows:
            print(row)


analytics = initialize_analyticsreporting()
response = get_report(analytics)
print_response(response)
