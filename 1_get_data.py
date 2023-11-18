import pandas as pd
from econdata import BCRP, FRED, YFinance
import warnings
warnings.simplefilter('ignore')


fechaini     = '2015-01-01'
fechafin     = '2023-11-18' # Be exact in the last day of the month
fred_key     = '####################################' # https://fred.stlouisfed.org/docs/api/api_key.html


# Data ###################################################################################################
codes = pd.read_excel('series.xlsx', sheet_name='Series')

''' Group of variables
codes[['Group', 'Description']].groupby('Group', sort=False).count()
'''

codes_bcrp = codes.loc[codes['Source'] == 'BCRP']
codes_fred = codes.loc[codes['Source'] == 'FRED']
codes_yf   = codes.loc[codes['Source'] == 'YF'  ]

codes_bcrp_mensual = codes_bcrp.loc[codes['Frequency'] == 'Mensual']
codes_fred_mensual = codes_fred.loc[codes['Frequency'] == 'Mensual']
codes_yf_diario    = codes_yf.loc  [codes['Frequency'] == 'Diario' ]

dict_bcrp_mensual = list(codes_bcrp_mensual[['Code', 'Description']].set_index('Code').to_dict().values())[0]
dict_fred_mensual = list(codes_fred_mensual[['Code', 'Description']].set_index('Code').to_dict().values())[0]
dict_yf_diario    = list(codes_yf_diario   [['Code', 'Description']].set_index('Code').to_dict().values())[0]



# Importation #############################################################################################
rango_fechas = pd.period_range(fechaini, fechafin, freq='M')

# Get data
df_bcrp_mensual  = BCRP.get_data(dict_bcrp_mensual, fechaini=fechaini, fechafin=fechafin)
df_fred_mensual  = FRED.get_data(dict_fred_mensual, api_key=fred_key, fechaini=fechaini, fechafin=fechafin)
df_yf_diario     = YFinance.get_data(dict_yf_diario, fechaini=fechaini, fechafin=fechafin)

# Date format
df_bcrp_mensual.index = pd.to_datetime(df_bcrp_mensual.index).strftime('%Y-%m')
df_fred_mensual.index = pd.to_datetime(df_fred_mensual.index).strftime('%Y-%m')
df_yf_diario.index = pd.to_datetime(df_yf_diario.index)
df_yf_diario = df_yf_diario.resample('M', axis = 0).mean()
df_yf_diario.index = df_yf_diario.index.strftime('%Y-%m')



# Join ####################################################################################################
df = pd.concat(
    [
        df_bcrp_mensual,
        df_fred_mensual,
        df_yf_diario
    ],
    axis = 1
)

df.index = rango_fechas


# GDP
gdp = BCRP.get_data(
    {'PN02538AQ': 'Real GDP'},
    fechaini='1980Q1',
    fechafin='2023Q2'
)
gdp

# Save at the first days after the closing date of the month
df.to_pickle('Data/monthly/data_2023_11.pkl')   # 202308 completed. 202309 preliminar
gdp.to_pickle('Data/quarterly/gdp_2023_11.pkl')

# df.to_csv('Data/monthly/data_2023_07.csv', encoding='UTF-8')
# gdp.to_csv('Data/quarterly/gdp_2023_07.csv', encoding='UTF-8')
