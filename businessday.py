import json
import os
from datetime import datetime, timedelta, timezone, time

# 外部ライブラリのインポート（エラーハンドリング付き）
try:
    import pandas as pd
    import pandas_market_calendars as mcal
    HAS_PANDAS_MCAL = True
except ImportError:
    HAS_PANDAS_MCAL = False

# --- 定義変数 (マジックナンバーの排除) ---
# カレンダー名
JPX = 'JPX'

# タイムゾーン
TIMEZONE_JST = timezone(timedelta(hours=9))

# フォーマット
DATE_FORMAT_YMD = '%Y-%m-%d'
TIME_FORMAT_HM = '%H:%M'

# 取引時間定義（前場・後場）
MORNING_SESSION_START = time(9, 0)
MORNING_SESSION_END = time(11, 30)
AFTERNOON_SESSION_START = time(12, 30)
AFTERNOON_SESSION_END = time(15, 30)

# ステータス定数
STATUS_OPEN = "open"
STATUS_CLOSED = "closed"

# 判定メソッド名
METHOD_CALENDAR = "pandas_market_calendars"
METHOD_FALLBACK = "weekday_fallback"

# 警告メッセージ
WARNING_NO_LIBRARY = "pandas_market_calendars not available; using weekday-only check (holidays NOT detected)."

def get_current_jst_time() -> datetime:
    """
    現在時刻を日本時間(JST)で取得
    
    Returns:
        datetime: JST timezone付きの現在日時
    """
    return datetime.now(TIMEZONE_JST)

def is_jpx_market_day_mcal(date_to_check: datetime) -> bool:
    """
    pandas_market_calendarsを使用した営業日判定
    
    Args:
        date_to_check: 判定対象の日時
        
    Returns:
        bool: 営業日の場合True、それ以外False
    """
    jpx_calendar = mcal.get_calendar(JPX)
    naive_timestamp = pd.Timestamp(date_to_check).tz_localize(None)
    start_date = naive_timestamp.normalize() - pd.Timedelta(days=1)
    end_date = naive_timestamp.normalize() + pd.Timedelta(days=1)
    market_days = jpx_calendar.valid_days(start_date=start_date, end_date=end_date)
    target_date_str = naive_timestamp.strftime(DATE_FORMAT_YMD)
    return target_date_str in market_days.strftime(DATE_FORMAT_YMD).tolist()

def is_jpx_market_day_fallback(date_to_check: datetime) -> bool:
    """
    土日のみ判定（祝日考慮なし）
    
    Args:
        date_to_check: 判定対象の日時
        
    Returns:
        bool: 平日の場合True、土日の場合False
    """
    return date_to_check.weekday() < 5

def is_jpx_trading_hour(current_time: time) -> bool:
    """
    取引時間内判定（前場・後場）
    
    Args:
        current_time: 判定対象の時刻
        
    Returns:
        bool: 取引時間内の場合True、それ以外False
    """
    is_morning_session = MORNING_SESSION_START <= current_time < MORNING_SESSION_END
    is_afternoon_session = AFTERNOON_SESSION_START <= current_time < AFTERNOON_SESSION_END
    return is_morning_session or is_afternoon_session

def main() -> None:
    """
    メイン処理
    現在の市場状態を判定してJSON形式で出力
    """
    current_datetime = get_current_jst_time()
    current_time = current_datetime.time()
    
    # 営業日判定
    is_market_day = False
    method = METHOD_FALLBACK
    warning = None
    
    if HAS_PANDAS_MCAL:
        try:
            is_market_day = is_jpx_market_day_mcal(current_datetime)
            method = METHOD_CALENDAR
        except Exception as error:
            is_market_day = is_jpx_market_day_fallback(current_datetime)
            warning = f"Calendar error: {str(error)}. Using fallback."
    else:
        is_market_day = is_jpx_market_day_fallback(current_datetime)
        warning = WARNING_NO_LIBRARY
    
    # 取引時間判定
    is_trading = is_market_day and is_jpx_trading_hour(current_time)
    
    # JSON出力データ構築
    output = {
        "timestamp": current_datetime.isoformat(),
        "market_times": {
            "morning_session_start": MORNING_SESSION_START.strftime(TIME_FORMAT_HM),
            "morning_session_end": MORNING_SESSION_END.strftime(TIME_FORMAT_HM),
            "afternoon_session_start": AFTERNOON_SESSION_START.strftime(TIME_FORMAT_HM),
            "afternoon_session_end": AFTERNOON_SESSION_END.strftime(TIME_FORMAT_HM),
            "timezone": "Asia/Tokyo"
        },
        "is_market_day": is_market_day,
        "market_day_method": method,
        "is_trading_hour": is_trading,
        "market_status": STATUS_OPEN if is_trading else STATUS_CLOSED,
        "warning": warning
    }
    
    # JSON出力（標準出力）
    json_output = json.dumps(output, indent=2, ensure_ascii=False)
    print(json_output)
    
    # JSONファイル出力
    output_file = os.path.join(os.path.dirname(__file__), "market_status.json")
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(json_output)

if __name__ == '__main__':
    main()