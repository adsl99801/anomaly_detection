# 創建新環境
conda create -n myenv python=3.9

# 啟用環境
conda activate myenv

# 安裝所有套件
conda install -c conda-forge psycopg2
conda install pandas numpy scikit-learn matplotlib
conda install sqlalchemy 
# conda install -c conda-forge mplcursors
conda install -c plotly plotly

# podman machine init
# podman machine start
podman pull docker.io/library/postgres
podman run -d --name my-postgres -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=123456 -e POSTGRES_DB=mydatabase -p 5432:5432 postgres


#簽報書會取得過去一年交易值,用此模型電文會有異常值,
#多因子