# import_rakuten_trade_history
settings.pyの`RAKUTEN_TRADE_HISTORY_CSV_DIR`に指定されているフォルダ内にある楽天証券の取引履歴csvファイルをDBに登録するコマンド
### 実行方法
`python manage.py import_rakuten_trade_history`

# download_yahoo_finance_csvfile
Yahooファイナンスの時系列データcsvをダウンロードする
### 実行方法
`python manage.py download_yahoo_finance_csvfile`

# import_yahoo_finance_csv
settings.pyの`YAHOO_FINANCE_CSV_DIR`に指定されているフォルダ内にあるYahooファイナンスの時系列データcsvファイルをDBに登録する
### 実行方法
`python manage.py import_yahoo_finance_csv`
