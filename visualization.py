import plotly.express as px

def plot_anomalies(df, title='異常檢測圖3'):
    """使用 Plotly Express 繪製 3D 散點圖，支援懸停顯示詳細資料"""

    # 將 anomaly 映射為顏色
    df['color'] = df['anomaly'].map({1: 'blue', -1: 'red'})

    # 繪製 3D 散點圖
    fig = px.scatter_3d(
        df,
        x='trans_date',
        y='amount',
        z='credit_limit',
        color='color',
        color_discrete_map={'blue': 'blue', 'red': 'red'},
        labels={'trans_date': '交易日期 (Transaction Date)', 'amount': '金額 (Amount)', 'credit_limit': '信用額度 (Credit Limit)', 'color': '狀態'
                },
        title=title,
        hover_data=['id', 'trans_date', 'amount',  'credit_limit']  # 懸停顯示的欄位
    )

    # 調整透明度
    fig.update_traces(marker=dict(opacity=0.5))

    # 更新圖例名稱
    fig.for_each_trace(lambda t: t.update(name='正常' if t.name == 'blue' else '異常'))

    fig.show()

def plot_2d_anomalies(df, title='交異常檢測圖2'):
    """使用 Plotly Express 繪製 2D 散點圖，顯示 trans_date 和 amount"""
    
    # 將 anomaly 映射為顏色
    df['color'] = df['anomaly'].map({1: 'blue', -1: 'red'})

    # 繪製 2D 散點圖
    fig = px.scatter(
        df,
        x='trans_date',
        y='amount',
        color='color',
        color_discrete_map={'blue': 'blue', 'red': 'red'},
        labels={'trans_date': '交易日期 (Transaction Date)', 'amount': '金額 (Amount)', 'color': '狀態'},
        title=title,
        hover_data=['id', 'trans_date', 'amount']  # 懸停顯示的欄位
    )

    # 調整透明度與點的大小
    fig.update_traces(marker=dict(size=3, opacity=0.6))

    # 更新圖例名稱
    fig.for_each_trace(lambda t: t.update(name='正常' if t.name == 'blue' else '異常'))

    fig.show()

def print_anomaly_samples(df):
    print("\n異常日期樣本（前20個）：")
    print(df[df['anomaly'] == -1][['id', 'trans_date', 'amount', 'credit_limit']].head(20))
