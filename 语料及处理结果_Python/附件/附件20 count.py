import pandas as pd

# 读取文件前100行（已按Freq(L)降序排序）
# df = pd.read_csv("突然-left.csv", encoding='utf-8-sig', nrows=100)
# df = pd.read_csv("突然-right.csv", encoding='utf-8-sig', nrows=100)
# df = pd.read_csv("忽然-left.csv", encoding='utf-8-sig', nrows=100)
df = pd.read_csv("忽然-right.csv", encoding='utf-8-sig', nrows=100)

# 提取词性标记（取最后一个'/'后的部分）
def get_pos(word):
    if '/' in word:
        return word.split('/')[-1]
    else:
        return '无'

df['词性标记'] = df['collocate'].apply(get_pos)

# 分组统计
grouped = df.groupby('词性标记').agg(
    词数=('collocate', 'count'),
    频数=('Freq(R)', 'sum')
).reset_index()

# 计算总频数（前100词的右频之和）
total_freq = df['Freq(R)'].sum()

# 添加占比列
grouped['占比'] = (grouped['频数'] / total_freq) * 100

# 按频数降序排序输出
grouped = grouped.sort_values('频数', ascending=False)

# 打印结果
print(grouped.to_string(index=False))
print(f"总频数（前100词的右频之和）: {total_freq}")