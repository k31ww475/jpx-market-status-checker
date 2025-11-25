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
