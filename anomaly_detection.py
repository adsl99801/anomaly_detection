import pandas as pd
from sklearn.ensemble import IsolationForest
from data_generator import create_sample_db
from visualization import plot_anomalies, print_anomaly_samples

# PostgreSQL 配置範例（若使用 SQLite 可忽略）
postgres_config = {
    'dbname': 'my-postgres',
    'user': 'admin',
    'password': '123456',
    'host': 'localhost',
    'port': '5432'  # 通常是 5432
}

# 1. 從資料庫讀取數據（可選擇 SQLite 或 PostgreSQL）
db_type = 'sqlite'  # 改為 'postgres' 以使用 PostgreSQL
conn = create_sample_db(db_type=db_type, db_config=postgres_config if db_type == 'postgres' else None)

# 根據資料庫類型讀取數據
if db_type == 'sqlite':
    df = pd.read_sql_query('SELECT * FROM transactions', conn)
elif db_type == 'postgres':
    df = pd.read_sql_query('SELECT * FROM transactions', conn, coerce_float=True)

# 2. 將日期轉為數值特徵以供異常檢測
df['trans_date'] = pd.to_datetime(df['trans_date'])
df['days_since'] = (df['trans_date'] - pd.to_datetime('2025-03-08')).dt.days  # 轉為相對於今天的偏移天數

# 3. 使用 Isolation Forest 檢測異常日期
iso_forest = IsolationForest(
    n_estimators=100,
    contamination=0.05,  # 假設 5% 的日期可能是異常
    random_state=42
)

# 只使用日期相關特徵進行檢測
X = df[['days_since']].values
pred = iso_forest.fit_predict(X)

# 4. 將預測結果加入 DataFrame
df['anomaly'] = pred  # -1 表示異常，1 表示正常

# 5. 統計異常數量
n_anomalies = len(df[df['anomaly'] == -1])
print(f"\n檢測到的異常日期數量: {n_anomalies}")
print(f"異常比例: {n_anomalies / len(df) * 100:.2f}%")

# 6. 可視化與異常樣本展示
plot_anomalies(df)
print_anomaly_samples(df)

# 關閉資料庫連線
conn.close()

if __name__ == "__main__":
    print("異常檢測完成")