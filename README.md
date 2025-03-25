簡報:  https://app.presentations.ai/view/FN2mlC

1.異常檢測專案
這個專案使用 Python 和 Isolation Forest 算法，從資料庫中的日期欄位檢測異常數據點。支援 SQLite 和 PostgreSQL 兩種資料庫，並提供散點圖可視化。

2.功能
數據生成：模擬交易數據，包括正常和異常日期。
異常檢測：使用 Scikit-learn 的 Isolation Forest 檢測異常日期。
可視化：生成散點圖。
模組化設計：分為數據生成、異常檢測和可視化三個模組。

3.檔案結構
data_generator.py：生成模擬數據並創建資料庫。
anomaly_detection.py：執行異常檢測並整合流程。
visualization.py：繪製散點圖並顯示異常樣本。

4.環境需求
Python 3.9+
Conda（建議使用 Anaconda 或 Miniconda）

5.postgre sql 用podman pod建立

6.參考指令
https://gist.github.com/LucaRottiers/6a6fb28ec9d98cffb125d722842a87ef

podman machine start  
podman ps -a  
podman restart c4f9ffebeff2  

https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf  

conda env list  
conda activate myenv  
