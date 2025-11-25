# jpx-market-status-checker
A Python script to check the current Japan Exchange (JPX) market status, including business day and trading hours, outputting results in JSON format.
# JPX Market Status Checker

## 概要

このスクリプトは、現在の**日本取引所グループ (JPX)** の市場開場状況（営業日および取引時間）を判定し、結果をJSON形式で出力します。主に市場が開いているか閉まっているかを確認するためのユーティリティです。

`pandas-market-calendars` ライブラリを利用して、土日祝日を考慮した正確な営業日判定を行います。ライブラリが存在しない場合は、土日のみを判定するフォールバック処理に切り替わります。

## 動作要件

* Python 3.8 以上

## 依存ライブラリ

以下の外部ライブラリが必要です。

```bash
pip install pandas pandas-market-calendars
標準ライブラリ:

    json

    os

    datetime

外部ライブラリ:

    pandas

    pandas-market-calendars

ファイル構成

ファイル名	説明
businessday.py	メインの市場状況判定スクリプトです。
market_status.json	スクリプト実行後に出力される、現在の市場状況を示すJSONファイルです。

使用方法

    依存ライブラリのインストール:
    Bash

pip install pandas pandas-market-calendars

スクリプトの実行:
Bash

    python businessday.py

    出力:

        実行結果は標準出力にもJSON形式で表示されます。

        スクリプトと同じディレクトリに market_status.json ファイルが生成されます。

JSON出力例

JSON

{
  "timestamp": "2025-11-26T12:34:56.789000+09:00",
  "market_times": {
    "morning_session_start": "09:00",
    "morning_session_end": "11:30",
    "afternoon_session_start": "12:30",
    "afternoon_session_end": "15:30",
    "timezone": "Asia/Tokyo"
  },
  "is_market_day": true,
  "market_day_method": "pandas_market_calendars",
  "is_trading_hour": true,
  "market_status": "open",
  "warning": null
}
