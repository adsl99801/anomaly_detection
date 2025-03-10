import numpy as np
from datetime import datetime, timedelta
import sqlite3
import psycopg2
from visualization import vi
def main():
    # 用來存儲每個數字的列表
    numbers_list = []

    # 用來計算總和
    total_sum = 0
    

    # 進行迴圈 950 次
    for _ in range(950):
        days_back = np.random.randint(0, 365)
        today = datetime(2025, 3, 8)  # 假設當前日期為 2025-03-08
        date = today - timedelta(days=days_back)
        x1 = date.strftime('%Y-%m-%d')
        print(x1)

# 驗證程式是否在主程式執行
if __name__ == "__main__":
    main()