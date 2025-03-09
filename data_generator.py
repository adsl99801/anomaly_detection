import numpy as np
from datetime import datetime, timedelta
import sqlite3
import psycopg2

def create_sample_db(db_type='sqlite', db_config=None):
    """
    創建模擬資料庫並生成數據
    :param db_type: 'sqlite' 或 'postgres'
    :param db_config: PostgreSQL 連線配置（字典），僅在 db_type='postgres' 時需要
    :return: 資料庫連線物件
    """
    if db_type == 'sqlite':
        conn = sqlite3.connect(':memory:')
        # SQLite 使用 INTEGER PRIMARY KEY AUTOINCREMENT
        create_table_query = '''
            CREATE TABLE transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trans_date TEXT,
                amount REAL
            )
        '''
    elif db_type == 'postgres':
        if not db_config:
            raise ValueError("PostgreSQL 需要提供 db_config")
        conn = psycopg2.connect(**db_config)
        # PostgreSQL 使用 SERIAL 實現自動遞增
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                trans_date TEXT,
                amount REAL
            )
        '''
    else:
        raise ValueError("僅支援 'sqlite' 或 'postgres'")

    # 創建表
    if db_type == 'sqlite':
        conn.execute(create_table_query)
    elif db_type == 'postgres':
        with conn.cursor() as cur:
            cur.execute(create_table_query)
        conn.commit()

    # 生成模擬數據
    np.random.seed(42)
    dates = []
    amounts = []
    today = datetime(2025, 3, 9)  # 假設當前日期
    
    # 生成 950 筆正常交易日期（過去一年內）
    for _ in range(950):
        days_back = np.random.randint(0, 365)
        date = today - timedelta(days=days_back)
        dates.append(date.strftime('%Y-%m-%d'))
        amounts.append(np.random.lognormal(10, 0.5))
    
    # 添加 50 筆異常日期（未來日期或過遠的過去）
    for _ in range(50):
        if np.random.rand() > 0.5:
            # 未來日期
            future_days = np.random.randint(1, 100)
            date = today + timedelta(days=future_days)
        else:
            # 過遠的過去（超過10年）
            past_days = np.random.randint(3650, 5000)
            date = today - timedelta(days=past_days)
        dates.append(date.strftime('%Y-%m-%d'))
        amounts.append(np.random.lognormal(10, 0.5))
    
    # 插入數據（不再提供 id，讓資料庫自動生成）
    data = list(zip(dates, amounts))  # 移除 id
    insert_query = 'INSERT INTO transactions (trans_date, amount) VALUES (%s, %s)'
    if db_type == 'sqlite':
        conn.executemany(insert_query.replace('%s', '?'), data)
        conn.commit()
    elif db_type == 'postgres':
        with conn.cursor() as cur:
            cur.executemany(insert_query, data)
        conn.commit()
    
    return conn