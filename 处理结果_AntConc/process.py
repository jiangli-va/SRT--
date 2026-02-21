import pandas as pd

# 使用绝对路径
file = r'c:\Users\Lenovo\Desktop\SRT\处理结果\处理结果.xlsx'
df_mi = pd.read_excel(file, sheet_name='忽然_MI')
df_t = pd.read_excel(file, sheet_name='忽然_t')

common = pd.merge(df_mi, df_t, on='Collocate', suffixes=('_MI', '_t'))

result = pd.DataFrame({
    'Rank by MI': common['Rank by MI'],
    'Rank by t': common['Rank by t'],
    'Freq': common['Freq_MI'],
    'Freq（L）': common['Freq（L）_MI'],
    'Freq（R）': common['Freq（R）_MI'],
    'MI': common['MI'],
    't': common['t'],
    'Collocate': common['Collocate']
})

result.to_excel(r'c:\Users\Lenovo\Desktop\SRT\处理结果\忽然_筛选.xlsx', index=False)
print('已生成忽然_筛选.xlsx')