import psycopg2
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
def create_sample_db(db_config):
    """
    創建 PostgreSQL 資料庫並生成模擬數據
    :param db_config: PostgreSQL 連線配置（字典）
    :return: 資料庫連線物件
    """
    # 連接到 PostgreSQL
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # 建立 transactions 表（若不存在）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            trans_date TEXT,
            amount REAL,
            customer_id INTEGER,
            merchant_id INTEGER,
            payment_method TEXT,
            transaction_type TEXT,
            currency TEXT,
            location TEXT,
            status TEXT,
            credit_limit REAL,
            installment_plan TEXT,
            fraud_flag INTEGER
        )
    ''')

    # 生成模擬數據
    n_transactions = 1000
    base_date = datetime(2025, 3, 8)
    customers = np.random.randint(1, 101, n_transactions).tolist()  # 轉為 Python 列表
    merchants = np.random.randint(1, 51, n_transactions).tolist()   # 轉為 Python 列表
    amounts = np.random.uniform(10, 10000, n_transactions).round(2).tolist()  # 轉為 Python 列表
    payment_methods = np.random.choice(['credit_card', 'debit_card', 'cash'], n_transactions).tolist()
    transaction_types = np.random.choice(['purchase', 'refund', 'transfer'], n_transactions).tolist()
    currencies = np.random.choice(['TWD', 'USD', 'EUR'], n_transactions).tolist()
    locations = np.random.choice(['Taipei', 'New York', 'London', 'Tokyo'], n_transactions).tolist()
    statuses = np.random.choice(['completed', 'pending', 'failed'], n_transactions).tolist()
    credit_limits = np.random.uniform(5000, 50000, n_transactions).round(2).tolist()  # 轉為 Python 列表
    installment_plans = np.random.choice(['none', '3_months', '6_months'], n_transactions).tolist()
    fraud_flags = np.random.choice([0, 1], n_transactions, p=[0.95, 0.05]).tolist()  # 轉為 Python 列表

    # 日期生成（包含異常日期）
    dates = []
    for _ in range(n_transactions):
        if np.random.random() < 0.05:
            delta = np.random.choice([timedelta(days=np.random.randint(365, 730)),
                                     timedelta(days=-np.random.randint(365, 730))])
        else:
            delta = timedelta(days=np.random.randint(-180, 180))
        dates.append((base_date + delta).isoformat())

    # 插入數據
    data = list(zip(dates, amounts, customers, merchants, payment_methods, transaction_types,
                    currencies, locations, statuses, credit_limits, installment_plans, fraud_flags))
    try:
        cursor.executemany('''
            INSERT INTO transactions (trans_date, amount, customer_id, merchant_id, payment_method, 
                                     transaction_type, currency, location, status, credit_limit, 
                                     installment_plan, fraud_flag)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', data)
        print(f"插入影響的行數: {cursor.rowcount}")
    except psycopg2.Error as e:
        print(f"插入失敗: {e}")

    conn.commit()
    return conn

if __name__ == "__main__":
    with open('config.json', 'r') as config_file:
        db_config = json.load(config_file)
    conn = create_sample_db(db_config)
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    print(df.head())
    conn.close()