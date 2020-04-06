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

# save_moving_average
DBに登録されているデータから移動平均線を算出してDBに登録
### 実行方法
`python manage.py save_moving_average`

# backtesting_library_sample
25日移動平均線と75日移動平均線のゴールデンクロスで購入し、デッドクロスで売却した場合のバックテストを実行するSample
### 実行方法
`python manage.py backtesting_library_sample`

### 実行結果
```
Start                     2019-01-04 00:00:00
End                       2020-03-19 00:00:00
Duration                    440 days 00:00:00
Exposure [%]                          38.4091
Equity Final [$]                      19210.1
Equity Peak [$]                       33578.3
Return [%]                            92.1006
Buy & Hold Return [%]                 103.172
Max. Drawdown [%]                    -46.0655
Avg. Drawdown [%]                     -3.3627
Max. Drawdown Duration      174 days 00:00:00
Avg. Drawdown Duration       12 days 00:00:00
# Trades                                    1
Win Rate [%]                              100
Best Trade [%]                        57.0629
Worst Trade [%]                       57.0629
Avg. Trade [%]                        57.0629
Max. Trade Duration         169 days 00:00:00
Avg. Trade Duration         169 days 00:00:00
Expectancy [%]                            NaN
SQN                                       NaN
Sharpe Ratio                              NaN
Sortino Ratio                             NaN
Calmar Ratio                          1.23873
_strategy                            SmaCross
dtype: object
```
<img src="https://github.com/fjunya/README_IMAGE/blob/master/kabu_100/backtesting_library_sample.png?raw=true">

