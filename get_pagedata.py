import pandas as pd
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
pass_ = 'notasecret'

# ここに自分のサービスアカウントとVIEWIDを文字型で指定する
SERVICE_ACCOUNT_EMAIL = ''
VIEW_ID = ''

# ダウンロードしたjsonファイルのパス
KEY_FILE_LOCATION = ""


def get_service(api_name='analytics', api_version='v4', scopes=SCOPES, key_file_location=KEY_FILE_LOCATION):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        key_file_location, scopes=scopes)

    # Build the service object.
    service = build('analyticsreporting', 'v4', credentials=credentials)

    return service


def get_report(analytics):
    # Use the Analytics Service Object to query the Analytics Reporting API V4.
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'pageSize': 300,
                    'dateRanges': [
                        {'startDate': '30daysAgo', 'endDate': 'today'}
                    ],
                    'metrics': [
                        {'expression': 'ga:pageviews'}, {
                            'expression': 'ga:avgTimeOnPage'}
                    ],
                    'dimensions': [
                        {'name': 'ga:pagePath'}, {'name': 'ga:pageTitle'}
                    ],

                }]
        }
    ).execute()


def main():

    # 関数を実行してデータを取得する
    analytics = get_service()
    response = get_report(analytics)

    # 取得した各データ（URL・ページタイトル・ページビュー・滞在時間）を二次元配列にする
    data = [[i['dimensions'][0], i['dimensions'][1], i['metrics'][0]['values'][0],
             i['metrics'][0]['values'][1]] for i in response['reports'][0]['data']['rows']]

    # データフレームの生成
    df = pd.DataFrame(data, columns=['url', 'pagetitle',
                                     'pageviews', 'page_ontime'])

    # ファイルの書き出し
    # encoding="cp932"→日本語文字化け対策, errors="ignore"→エンコードエラー対策
    with open("./mysite_data.csv", mode="w", encoding="cp932", errors="ignore", newline="") as f:
        df.to_csv(f, index=False)


if __name__ == '__main__':
    main()
