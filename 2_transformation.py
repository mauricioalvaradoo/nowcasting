import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import STL
from sklearn.preprocessing import StandardScaler


df    = pd.read_pickle('Data/monthly/data_2023_08.pkl')
gdp   = pd.read_pickle('Data/quarterly/gdp_2023_08.pkl')
codes = pd.read_excel('series.xlsx')
df_c  = pd.DataFrame(index=df.index, columns=df.columns)


# Transformations #############################################################
'''
1: Levels
2: First Difference to the Levels
3: Logarithm
4: First Difference to the Logarithm
+ : Season-Trend decomposition using LOESS (STL)
'''


dict_transf = list(
    codes[['Description', 'Tcode']].set_index('Description').to_dict().values()
)[0]


for k, v in dict_transf.items():
    
    X = df[k].dropna()

    if  str(v) == '1':
        df_c[k] = X

    elif str(v) == '1+':
        df_c[k] = STL(X, period=12).fit().trend
    
    elif str(v) == '2':
        df_c[k] = X - X.shift(1)
    
    elif str(v) == '2+':
        X = STL(X, period=12).fit().trend
        df_c[k] = X - X.shift(1)
    
    elif str(v) == '3':
        df_c[k] = np.log(X)
    
    elif str(v) == '3+':
        X = STL(X, period=12).fit().trend
        df_c[k] = np.log(X)

    elif str(v) == '4':
        df_c[k] = np.log(X) - np.log(X).shift(1)
    
    elif str(v) == '4+':
        X = STL(X, period=12).fit().trend
        df_c[k] = np.log(X) - np.log(X).shift(1)
    else:
        pass


scaler = StandardScaler()
Y = scaler.fit_transform(df_c)
df_scaled = pd.DataFrame(Y, columns=df_c.columns, index=df_c.index)


# GDP Growth
gdp['GDP Growth'] = ( gdp['Real GDP']/gdp['Real GDP'].shift(4) - 1 ) * 100



# Saving ######################################################################
df_scaled.to_pickle('Data/monthly/data_st_2023_08.pkl')
gdp.to_pickle('Data/quarterly/gdp_st_2023_08.pkl')

# df_scaled.to_csv('Data/monthly/data_st_2023_07.csv', encoding='UTF-8')
# gdp.to_csv('Data/quarterly/gdp_st_2023_07.csv', encoding='UTF-8')