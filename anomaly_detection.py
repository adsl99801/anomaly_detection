import json
import pandas as pd
from sklearn.ensemble import IsolationForest
from data_generator import create_sample_db
from visualization import plot_anomalies, print_anomaly_samples

# 從 config.json 讀取 PostgreSQL 配置
with open('config.json', 'r') as config_file:
    postgres_config = json.load(config_file)

# 連線並讀取數據
conn = create_sample_db(postgres_config)
df = pd.read_sql_query('SELECT * FROM transactions', conn, coerce_float=True)

# 日期轉換
df['trans_date'] = pd.to_datetime(df['trans_date'])
df['days_since'] = (df['trans_date'] - pd.to_datetime('2025-03-08')).dt.days

# 使用多個特徵進行異常檢測
X = df[['days_since', 'amount', 'credit_limit']].values

# 異常檢測 (contamination=0.05)
iso_forest = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
df['anomaly'] = iso_forest.fit_predict(X)

# 統計與輸出
n_anomalies = len(df[df['anomaly'] == -1])
print(f"\ncontamination=0.05:")
print(f"檢測到的異常數量: {n_anomalies}")
print(f"異常比例: {n_anomalies / len(df) * 100:.2f}%")
print_anomaly_samples(df)

# 繪製一張散點圖
plot_anomalies(df, title='異常檢測 (contamination=0.05)')

conn.close()

if __name__ == "__main__":
    print("異常檢測完成")