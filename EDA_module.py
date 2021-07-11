import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# 색상 설정
palette1 = sns.color_palette('hls',8)
categorical = sns.color_palette('Set3', 10)
sbys = sns.color_palette('RdBu', 10)
sequential = sns.color_palette("GnBu", 10)
sequential2 = sns.color_palette("BuGn", 10)

def preprocessing_demension(demension):
    # 브랜드 카테고리 데이터 전처리 
    demension = demension.drop(['MyUnknownColumn'],axis=1) # 필요없는 컬럼 제거 
    demension = demension.drop_duplicates() # 중복된 데이터 제거 
    demension['car_fuel'] = demension['car_fuel'].str.replace('하브리드','하이브리드')  # car_fuel타입에 하이리브 -> 하이브리드로 수정
    demension['car_seg_size'] = demension['car_seg_size'].str.replace('세던','세단') # 세던 -> 세단으로 수정 
    # 컬럼명 재지정 
    demension.rename(columns={'Brand':'brand','model_pk':'model',
                              'car_seg_size':'car_type','car_seg':'segment','car_fuel':'fuel_type'},inplace=True)
    
    return demension


def preprocessing_kaida(kaida_df):
    # 월별 신규 등록 데이터 
    kaida_df['sales_type'] = kaida_df['sales_type'].apply(lambda x: x.strip())  
    kaida_df.drop(index=kaida_df[kaida_df['model'].str.contains('Total')].index, inplace=True) 
    kaida_df.drop_duplicates(inplace=True) 
    kaida_df['month'] = kaida_df['month'].apply(lambda x: x[:-1]) 
    kaida_df['value'] = kaida_df['value'].apply(lambda x: x.replace(",", "")) 
    kaida_df.reset_index(drop=True, inplace=True) 

    kaida_df['date'] = kaida_df['year'].astype('str') + "-" + kaida_df['month'] 
    kaida_df['date'] = pd.to_datetime(kaida_df['date'], format="%Y-%m", errors='raise') 
    kaida_df['date'] = kaida_df['date'].dt.strftime("%Y-%m") 

    kaida_df = kaida_df.astype({col: "int" for col in ['value', 'month', 'year']})

    # age컬럼 정수화 
    kaida_df['age'] = kaida_df['age'].str.replace('~19','20')
    kaida_df['age'] = kaida_df['age'].str.replace('20~29','20')
    kaida_df['age'] = kaida_df['age'].str.replace('30~39','30')
    kaida_df['age'] = kaida_df['age'].str.replace('40~49','40')
    kaida_df['age'] = kaida_df['age'].str.replace('50~59','50')
    kaida_df['age'] = kaida_df['age'].str.replace('60~69','60')
    kaida_df['age'] = kaida_df['age'].str.replace('70~','70')
    kaida_df['age'] = kaida_df['age'].str.replace('-','0')
    kaida_df['age'] = kaida_df['age'].astype(int)
    
    return kaida_df


# tv_daily 데이터셋 전처리
def tv_daily_df():
    TV_daily_0 = pd.read_csv("datas/TV_daily.csv", encoding='utf-8')
    TV_daily_0['Date'] = [d[:11] for d in TV_daily_0['Date']]
    TV_daily_0['YM'] = [d[:7] for d in TV_daily_0['Date']]
    TV_daily_0['Date'] = pd.to_datetime(TV_daily_0['Date'])
    TV_daily_0['Week'] = TV_daily_0['Date'].dt.dayofweek #월0 ~일6 #day_name()
    TV_daily_0['Month'] = [int(m[:-1]) for m in TV_daily_0['Month']]
    TV_daily_0['Sex'] = [s[0] if s != '개인' else '개인' for s in TV_daily_0['Target_Audience']]
    TV_daily_0['Age'] = [a[1:3] if a != '개인' else '개인' for a in TV_daily_0['Target_Audience']]
    
    return TV_daily_0


# 광고실행연도를 기준으로 한 데이터셋 생성 및 전처리
def making_ym_df(brand, sex='개인', age='개인'):
    TV_daily_0 = tv_daily_df()
    TV_daily_1 = TV_daily_0[TV_daily_0['Sex'] == sex][TV_daily_0['Age'] == age]
    df = TV_daily_1[TV_daily_1['Advertiser'] == brand]

    df_pv = pd.pivot_table(df, index=['Year','Month','Day','YM'],
                  aggfunc={'Adience':sum, 'GRP':sum, 'Week':'mean'}).reset_index()
    df_pv = pd.pivot_table(df_pv, index=['YM', 'Year','Month'],
                  aggfunc={'Day': 'count', 'Adience':sum, 'GRP':sum, 'Week':'mean'}).reset_index()
    df_pv_year = pd.pivot_table(df_pv, index=['Year'],
              aggfunc={'Day':sum, 'Adience':sum, 'GRP':sum, 'Week':'mean'})
    df_pv_year['Aud_avg'] = round(df_pv_year['Adience']/df_pv_year['Day'])
    df_pv_year['GRP_avg'] = df_pv_year['GRP']/df_pv_year['Day']
    
    return df_pv_year


# 타겟 시청자군 데이터셋 생성 및 전처리
def making_aud_df(brand, year=2020):
    TV_daily_0 = tv_daily_df()
    TV_daily_0 = TV_daily_0[TV_daily_0['Advertiser'] == brand][TV_daily_0['Year'] == year]
    aud_df = TV_daily_0.drop(TV_daily_0[TV_daily_0['Target_Audience'] == '개인'].index ,axis=0)
    aud_df_pv = pd.pivot_table(aud_df, index=['Target_Audience', 'Sex','Age','Year','Month','Day','YM'],
                   aggfunc={'Adience':sum, 'GRP':sum, 'Week':'mean'}).reset_index()
    aud_df_pv = pd.pivot_table(aud_df, index=['Target_Audience','Sex','Age','YM', 'Year','Month'],
                   aggfunc={'Day': pd.Series.nunique, 'Adience':sum, 'GRP':sum, 'Week':'mean'}).reset_index()
    aud_df_pv = pd.pivot_table(aud_df, index=['Year','Target_Audience','Sex','Age'],
                 aggfunc={'Day': sum, 'Adience':sum, 'GRP':sum}).reset_index()
    
    return aud_df_pv


# tv_daily_1 데이터셋 전처리 함수화
def tv_daily_df_1():
    TV_daily_0 = pd.read_csv("datas/TV_daily.csv", encoding='utf-8') # tv데일리 데이터 읽기
    TV_daily_0['Date'] = [d[:11] for d in TV_daily_0['Date']] 
    TV_daily_0['YM'] = [d[:7] for d in TV_daily_0['Date']] #
    TV_daily_0['Date'] = pd.to_datetime(TV_daily_0['Date'])
    TV_daily_0['Week'] = TV_daily_0['Date'].dt.dayofweek #월0 ~일6 #day_name()
    TV_daily_0['Month'] = [int(m[:-1]) for m in TV_daily_0['Month']]
    TV_daily_0['Sex'] = [s[0] if s != '개인' else '개인' for s in TV_daily_0['Target_Audience']]
    TV_daily_0['Age'] = [a[1:3] if a != '개인' else '개인' for a in TV_daily_0['Target_Audience']]
    
    return TV_daily_0


# 브랜드, 채널, 장르를 뽑은 함수
def making_ymch_df(brand, year=2020):
    TV_daily_0 = tv_daily_df_1()
    TV_daily_2 = TV_daily_0[TV_daily_0['Channel'] == channel][TV_daily_0['Genre'] == genre]
    df_1 = TV_daily_2[TV_daily_2["Advertiser"] == brand]
    df_pv_1 = pd.pivot_table(df_1, index=['Year','Month','Day','YM'],
                  aggfunc={'Adience':sum, 'GRP':sum, 'Week':'mean'}).reset_index()
    df_pv_1 = pd.pivot_table(df_pv_1, index=['YM', 'Year','Month'],
                  aggfunc={'Day': 'count', 'Adience':sum, 'GRP':sum, 'Week':'mean'}).reset_index()
    df_pv_year_1 = pd.pivot_table(df_pv_1, index=['Year'],
              aggfunc={'Day':sum, 'Adience':sum, 'GRP':sum, 'Week':'mean'})
    df_pv_year_1['Aud_avg'] = round(df_pv_year_1['Adience']/df_pv_year_1['Day'])
    df_pv_year_1['GRP_avg'] = df_pv_year_1['GRP']/df_pv_year_1['Day']
    
    return df_pv_year_1


# 타겟 채널 데이터셋 생성 및 전처리
def making_chn_df(brand, year=2020):
    
    TV_daily_0 = tv_daily_df_1()
    TV_daily_0 = TV_daily_0[TV_daily_0['Advertiser'] == brand][TV_daily_0['Year'] == year]
    chn_df_1 = TV_daily_0.drop(TV_daily_0[TV_daily_0['Target_Audience'] == '개인'].index ,axis=0)
    chn_df_pv_1 = pd.pivot_table(chn_df_1, index=['Target_Audience', 'Channel','Genre','Year','Month','Day','YM'],
                   aggfunc={'Adience':sum, 'GRP':sum, 'Week':'mean'}).reset_index()
    chn_df_pv_1 = pd.pivot_table(chn_df_1, index=['Target_Audience','Channel','Genre','YM', 'Year','Month'],
                   aggfunc={'Day': pd.Series.nunique, 'Adience':sum, 'GRP':sum, 'Week':'mean'}).reset_index()
    chn_df_pv_1 = pd.pivot_table(chn_df_1, index=['Year','Target_Audience','Channel','Genre'],
                 aggfunc={'Day': sum, 'Adience':sum, 'GRP':sum}).reset_index()
    
    return chn_df_pv_1


# 벤츠 당월 등록대수 
def sales_month(target_brand,date):
    sales = kaida_df[(kaida_df['brand']==target_brand)&
                     (kaida_df['date']==date)].groupby('month')['value'].agg(sum).reset_index()
    return sales


# 상위 5개 브랜드의 당월 시장점유율
def pie_major(year,month):
    major = kaida_df[(kaida_df['year']==year)&(kaida_df['month']==month)].groupby('brand').agg(sum).sort_values('value',ascending=False).head()
    plt.figure(figsize=(20,10))
    explode = (0.05, 0.05, 0.05, 0.05,0.05)
    colors = ['whitesmoke','red','lightgrey','darkgrey','dimgrey']
    plt.pie(major['value'],explode=explode, colors=colors,labels=major.index,autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title(f'외제차 상위 5개 브랜드의 {month}월 등록대수 비교')
    plt.show()


# 당월 브랜드 TOP3 모델 
def month_top3(year, month, brand): # int, str, Mercedes-Benz

    brand_df = kaida_df[(kaida_df['month'] == month) & (kaida_df['year'] == year) & (kaida_df['brand'] == brand)]
    brand_gb = brand_df.groupby(['model']).sum()
    brand_gb['percent'] = brand_gb['value'] / float(brand_gb.sum()['value']) * 100
    brand_gb = brand_gb.sort_values(by='value', ascending=False)[:3]
    percent = brand_gb['percent'].tolist()
    
    plt.figure(figsize=(10,8))
    plt.title(f'{year}-{month} {brand} Top 3 Models', fontsize=15)

    plot = sns.barplot(data=brand_gb, x=brand_gb.index, y='value', palette ='Set2')
    sns.despine(left = True, bottom = True)
    idx = 0
    
    for p in plot.patches:
        left, bottom, width, height = p.get_bbox().bounds
        plot.annotate(f'{round(percent[idx], 2)}%', (left + width / 2, height * 1.01), ha='center', fontsize=15)
        idx += 1


# 당월 판매 성별/연령별 주요고객 및 연령대별 주요고객
# 브랜드 주요 구매자 성비
def sales_type(target_brand,date):
    benz_type = kaida_df[(kaida_df['brand']==target_brand)&(kaida_df['date']==date)].groupby('sales_type').agg(sum)
    
    plt.figure(figsize=(20,10))
    explode = (0.05, 0.05, 0.05)
    colors = ['red','cadetblue','lightgrey']
    plt.pie(benz_type['value'],explode=explode, labels=benz_type.index, colors=colors,autopct='%1.1f%%', shadow=True, startangle=90)
    plt.show()


# 당월 브랜드차량 등록 연령대 비율(age)
def sales_age(target_brand,date):
    df = kaida_df[(kaida_df['brand']==target_brand)&(kaida_df['date']==date)
                  &(kaida_df['sales_type']!='법인')].groupby(['sales_type','age']).agg(sum).reset_index()
    for a in df['sales_type'].unique():
        plt.figure(figsize=(12,6))
        df_type = df[df['sales_type']==a]
        ax = sns.barplot(x=df_type['value']/df_type['value'].agg(sum)*100,y='age',orient='h',ci=False,data=df_type,palette=categorical)
        sns.despine(left = False, bottom = True)
        for p in ax.patches:
            x, y, width, height = p.get_bbox().bounds
            ax.text(width*1.01, y+height/2, "%.1f %%"%(width), va='center')
        plt.title(f'{date} 외제차 등록 {a} 연령대 비율')
        plt.show()


# 주요 연령대의 선호 (연료타입 / 사이즈 / 타입(해치백, 쿠페)
def segment_preference(target_brand, year, age,sex):

    plt.figure(figsize=(12,5))
    seg = kaida_dem[(kaida_dem['brand']==target_brand)&(kaida_dem['year']==year)&(kaida_dem['age']==age)
                    &(kaida_dem['sales_type']== sex)].groupby(['car_type']).agg(sum).sort_values('value',ascending=False).reset_index()
    seg['percent'] = seg['value'] / seg['value'].agg(sum)*100
    ax = sns.barplot(x='percent',y='car_type',ci=None,data=seg,palette=sequential)
    sns.despine(left = True, bottom = True)
    plt.title(f'{year}년 {age}대 {sex} 차종 선호도')

    for p in ax.patches:
            x, y, width, height = p.get_bbox().bounds
            ax.text(width*1.01, y+height/2, "%.1f %%"%(width), va='center')

    plt.show()


# 특정브랜드,성별의 연령대별 선호 차종/연료/세그먼트
def customer_preference(target_brand,sex,seg_type,palette_type):
    plt.subplots(figsize=(16,6))
    plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.5)

    for a in range(1,4):
        plt.subplot(1,3,a)
        target_age = (a+2)*10
        seg = kaida_dem[(kaida_dem['brand']==target_brand)&(kaida_dem['age']==target_age)
                        &(kaida_dem['sales_type']==sex)].groupby([seg_type]).agg(sum).sort_values('value',ascending=False).reset_index()
        ax = sns.barplot(x=seg_type,y='value',ci=None,data=seg,palette=palette_type)
        sns.despine(left = True, bottom = True)
        plt.title(f'{target_age}대 {sex} {seg_type} 선호도')
    
    plt.show()


# 브랜드 Z차트를 통한 최근 12개월 판매추이
def make_z_chart(brand, date):
    z_chart_df = kaida_df.groupby(['brand', 'date']).agg('sum')['value'].reset_index()
    z_chart_df = z_chart_df[z_chart_df['brand'] == brand]
    z_chart_df = z_chart_df[z_chart_df['date'] < date]
    
    z_chart_df2 = z_chart_df.tail(12).reset_index(drop=True)
    
    ls = []
    prev = 0
    for value in z_chart_df2['value'].values:
        curr = prev + value
        prev = curr
        ls.append(curr)
    
    z_chart_df2['매출누계'] = ls
    
    ls_2 = []
    for num in range(z_chart_df.shape[0] - 11, z_chart_df.shape[0] + 1):
        idx = num - 12
        ls_2.append(z_chart_df['value'].values[idx:num].sum())
        
    z_chart_df2['이동년계'] = ls_2
    
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    sns.pointplot(data=z_chart_df2, x='date', y='value', ax=ax)
    sns.pointplot(data=z_chart_df2, x='date', y='매출누계', ax=ax, color='r')
    sns.pointplot(data=z_chart_df2, x='date', y='이동년계', ax=ax, color='gray')

    plt.title(f"{brand} 최근 12개월의 신규 등록대수 z-chart", fontsize=20)
    plt.ylabel(None)

    plt.show()


# 브랜드별 네이버 쿼리 전월대비, 전년대비 비교  
def query_compare(year, month, brand): 
    total_df = query_df.groupby(['YM', 'Month', 'Year']).sum()['Count_query']
    total_df = total_df.reset_index()
    total_df.rename(columns = {'Count_query' : 'Total'}, inplace = True)
    total_df = total_df.drop('YM', axis=1)

    brand_query = query_df[query_df['Brand'] == brand]
    brand_gb = brand_query.groupby(['YM']).sum()['Count_query']
    brand_gb = brand_gb.reset_index()

    brand_query = pd.concat([brand_gb, total_df], axis=1)
  
    target_year = brand_query[(brand_query['Year'] == year) & (brand_query['Month'] == month)] # 현재
    compare_lastm = brand_query[(brand_query['Year'] == year) & (brand_query['Month'] == month - 1)] # 지난달
    compare_lasty = brand_query[(brand_query['Year'] == year - 1) & (brand_query['Month'] == month)] # 작년 이번달
    
    monthly = pd.concat([target_year, compare_lastm], axis=0)
    yearly = pd.concat([target_year, compare_lasty], axis=0)
    

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    sns.set_color_codes('pastel')
    fig.set_size_inches(12, 10)
    
    sns.barplot(y = 'Total', x = 'YM', data=monthly,
                label = 'Total', color = 'g', edgecolor = 'w', ax=ax1)
    sns.set_color_codes('muted')
    sns.barplot(y = 'Count_query', x = 'YM', data = monthly,
                label = 'total query', color = 'b', edgecolor = 'w', ax=ax1)
    
    sns.set_color_codes('pastel')
    sns.barplot(y = 'Total', x = 'YM', data=yearly,
                label = 'total query', color = 'g', edgecolor = 'w', ax=ax2)
    sns.set_color_codes('muted')
    sns.barplot(y = 'Count_query', x = 'YM', data = yearly,
                label = f'{brand} total query', color = 'b', edgecolor = 'w', ax=ax2)
    
    sns.despine(left = True, bottom = True)
    ax1.set(title=f'Last Month {brand} naver query')
    ax2.set(title=f'Last Year {brand} naver query')
    ax1.set_ylim(ax2.get_ylim())
    
    ax2.legend(loc='upper right', bbox_to_anchor=(1.05, 1.0))
    plt.show()


# 브랜드 연도별 audience, GRP 추이 그래프
def yearly_plot(brand):
    df_pv_year = making_ym_df(brand)
    fig, ax = plt.subplots(2, 2, figsize=(12, 8))
    x = df_pv_year.index.to_list()
    
    sns.barplot(data=df_pv_year, x=x, y='Adience', ax=ax[0,0], palette="Blues_d")
    sns.pointplot(data=df_pv_year, x=x, y='GRP', ax=ax[0,1], color='gray')
    sns.barplot(data=df_pv_year, x=x, y='Aud_avg', ax=ax[1,0], palette="Blues_d")
    sns.pointplot(data=df_pv_year, x=x, y='GRP_avg', ax=ax[1,1], color='gray')

    ax[0,0].set_title("Yearly Audience")
    ax[0,1].set_title("Yearly GRP")
    ax[1,0].set_title("Daily Avearge Audience")
    ax[1,1].set_title("Daily Avearge GRP")

    fig.tight_layout()
    plt.show()


# 브랜드 특정 연도의 나이/성별에 따른 시청자 구성
def aud_ratio(brand, year=2020):
    
    aud_df_pv = making_aud_df(brand, year)
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    x_men = aud_df_pv[aud_df_pv['Sex']=='남']['Age'].to_list()
    y_men = aud_df_pv[aud_df_pv['Sex']=='남']['GRP'].to_list()
    x_women = aud_df_pv[aud_df_pv['Sex']=='여']['Age'].to_list()
    y_women = aud_df_pv[aud_df_pv['Sex']=='여']['GRP'].to_list()
    sns.barplot(x_men, y_men, label='Men', ax=ax, color="#ABC4EF")
    sns.barplot(x_women, y_women, label='Women', bottom=y_men, ax=ax, color="#F38394")
    
    ax.set_xlabel('age')
    ax.set_ylabel('GRPs')
    ax.set_title('GRPs by age and gender')
    ax.legend()

    plt.show()


# 특정연도 / 특정브랜드 ABC 그래프 (연령대 기준)
def aud_ABC(brand, year=2020):
    aud_df_pv = making_aud_df(brand, year)
    aud_df_pv = aud_df_pv.sort_values(by='GRP', ascending=False)
    aud_df_pv['GRP_per'] = [g/sum(aud_df_pv['GRP'])*100 for g in aud_df_pv['GRP']]
    aud_df_pv['GRP_per_cum'] = [sum(aud_df_pv['GRP_per'].iloc[:i+1]) for i in range(len(aud_df_pv))]
    
    fig, ax1 = plt.subplots(figsize=(10,6))
    sns.set_style("white")
    ax1.set_title('ABC analysis of Audiences', fontsize=20)
    x = aud_df_pv['Target_Audience'].to_list()
    y = aud_df_pv['GRP_per'].to_list()
    y_cum = aud_df_pv['GRP_per_cum'].to_list()

    ax1.set_ylabel('Composition ratio %',fontsize=13)
    ax1 = sns.barplot(x, y, palette='summer')

    ax1.tick_params(axis='y')
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Cumulative composition ratio %',fontsize=13)
    sns.lineplot(x, y_cum, color='red')
    ax2.tick_params(axis='y')
    
    plt.show()


# 데이터 불러오기
kaida_df = pd.read_csv("datas/kaida.csv")
demension = pd.read_csv("datas/demension.csv")
query_df = pd.read_csv("datas/naver_query.csv")
TV_daily_0 = pd.read_csv("datas/TV_daily.csv")

# 전처리
kaida_df = preprocessing_kaida(kaida_df)
demension = preprocessing_demension(demension)

# Merge: kaida + demension 
kaida_merge = kaida_df.copy()
kaida_merge = kaida_merge.drop(columns='brand')
kaida_dem = pd.merge(kaida_merge,demension,how='left',on=['model'])