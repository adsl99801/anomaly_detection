import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
def plot_anomalies(df):
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(12, 6))
    plt.scatter(
        df['trans_date'][df['anomaly'] == 1],
        df['amount'][df['anomaly'] == 1],
        c='blue', label='正常日期', alpha=0.5
    )
    plt.scatter(
        df['trans_date'][df['anomaly'] == -1],
        df['amount'][df['anomaly'] == -1],
        c='red', label='異常日期', alpha=0.5
    )
    plt.xlabel('(Transaction Date)')
    plt.ylabel('(Amount)')
    plt.title('日期異常檢測')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def print_anomaly_samples(df,n=20):
    print("\n異常日期樣本（前n個）：")
    print(df[df['anomaly'] == -1][['id', 'trans_date', 'amount']].head(n))