import pandas as pd
import configparser
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from sqlalchemy import create_engine


config = configparser.ConfigParser()
config.read("../../data.ini")
info = config["db"]

client = create_engine(f'mysql://{info["user"]}:{info["password"]}@{info["host"]}/{info["db"]}?charset=utf8')

# 월별 신규 등록 데이터 
kaida_df = pd.read_sql('SELECT * FROM kaida', con=client) 
# 브랜드 카테고리 데이터 
demension = pd.read_sql('SELECT * FROM demension_upload', con=client) 
# 네이버 일별 검색량 데이터
query_df = pd.read_sql('SELECT * FROM naver_query', con=client) 
# 일별 TV 광고 데이터 (년도, 월, 일, 날짜, 광고주, 채널, 장르, 주 타겟 시청자(연령대), 시청자수, GRP(총시청률) 컬럼 선택)
TV_daily_0 = pd.read_sql("SELECT  Year, Month, Day, Date, Advertiser, Channel, Genre, Target_Audience, Adience, GRP FROM mydb.TV_daily", con=client)


# 데이터셋 저장
datasets = {"kaida": kaida_df, "demension": demension, "naver_query": query_df, "TV_daily": TV_daily_0}

for title, dataset in datasets.items():
    dataset.to_csv(f'datas/{}.csv', encoding='utf-8', header=True)