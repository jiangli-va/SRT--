import pandas as pd

MI_FILE = "突然-文学_MI.csv"
T_FILE  = "突然-文学_T值.csv"
OUT_LEFT = "突然-left.csv"
OUT_RIGHT = "突然-right.csv"
MI_THRESHOLD = 3.0
T_THRESHOLD  = 2.33

# 读取数据
# MI文件：列名 'rank', '搭配词', '共现频数', '全局频率', '左侧', '右侧', 'MI值'
df_mi = pd.read_csv(MI_FILE, encoding='utf-8-sig')
# 重命名列为英文，方便操作
df_mi.rename(columns={
    'rank': 'rank_mi',
    '搭配词': 'collocate',
    '共现频数': 'freq',
    '左侧': 'freqL_mi',
    '右侧': 'freqR_mi',
    'MI值': 'mi'
}, inplace=True)
# 只保留需要的列
df_mi = df_mi[['rank_mi', 'collocate', 'freq', 'freqL_mi', 'freqR_mi', 'mi']]

# T值文件：列名 'Rank by t', 'Freq', 'Freq(L)', 'Freq(R)', 't值', '搭配词'
df_t = pd.read_csv(T_FILE, encoding='utf-8-sig')
df_t.rename(columns={
    'Rank by t': 'rank_t',
    'Freq': 'freq',
    'Freq(L)': 'freqL_t',
    'Freq(R)': 'freqR_t',
    't值': 't',
    '搭配词': 'collocate'
}, inplace=True)
df_t = df_t[['rank_t', 'collocate', 'freq', 't']]  # 只取排名、搭配词、t值，总频次用于核对（可选）

# 合并与筛选 
# 仅保留两个文件都存在的搭配词
df_merged = pd.merge(df_mi, df_t, on='collocate', how='inner')

# 筛选 MI > 3 且 T > 2.33
df_filtered = df_merged[(df_merged['mi'] > MI_THRESHOLD) & (df_merged['t'] > T_THRESHOLD)].copy()

# 此时 df_filtered 包含列：rank_mi, collocate, freq_x (MI文件的频数), freqL_mi, freqR_mi, mi, rank_t, freq_y (T文件的频数), t
df_filtered.rename(columns={'freq_x': 'freq'}, inplace=True)
df_filtered.drop(columns=['freq_y'], inplace=True)

# 构造左侧高频词文件 
df_left = df_filtered[['rank_mi', 'rank_t', 'freq', 'freqL_mi', 'mi', 't', 'collocate']].copy()
df_left.rename(columns={'freqL_mi': 'Freq(L)'}, inplace=True)
# 按 Freq(L) 降序排序
df_left.sort_values('Freq(L)', ascending=False, inplace=True)
# 输出 CSV
df_left.to_csv(OUT_LEFT, index=False, encoding='utf-8-sig')

# 构造右侧高频词文件
df_right = df_filtered[['rank_mi', 'rank_t', 'freq', 'freqR_mi', 'mi', 't', 'collocate']].copy()
df_right.rename(columns={'freqR_mi': 'Freq(R)'}, inplace=True)
# 按 Freq(R) 降序排序
df_right.sort_values('Freq(R)', ascending=False, inplace=True)
# 输出 CSV
df_right.to_csv(OUT_RIGHT, index=False, encoding='utf-8-sig')

print(f"处理完成！共筛选出 {len(df_filtered)} 个满足条件的搭配词。")
print(f"左侧文件已保存为：{OUT_LEFT}")
print(f"右侧文件已保存为：{OUT_RIGHT}")