import re
import math
from collections import Counter
import csv

def calculate_t_value(corpus_file):
    # 读取语料文件
    with open(corpus_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 将文本分割成"词/词性"的列表
    # 匹配"任意非空格字符+/任意非空格字符"的模式，包括标点符号
    word_pos_pairs = re.findall(r'([^/\s]+/[^\s]+)', text)
    
    N = len(word_pos_pairs)  # 语料库大小
    print(f"语料库总词数 N = {N}")
    
    # 目标词是"突然/ad"
    target_word = "忽然/d"
    
    # 统计词频
    word_freq = Counter(word_pos_pairs)
    print(f"'{target_word}' 单独出现频数 f({target_word}) = {word_freq[target_word]}")
    
    # 找到所有"突然/ad"的位置
    target_positions = []
    for i, word_pos in enumerate(word_pos_pairs):
        if word_pos == target_word:
            target_positions.append(i)
    
    print(f"找到 '{target_word}' 出现次数: {len(target_positions)}")
    
    # 计算跨距(-5,5)内的共现词
    window_size = 5
    collocation_counter = Counter()
    left_collocation_counter = Counter()
    right_collocation_counter = Counter()
    
    for pos in target_positions:
        # 左边窗口(-5,-1]
        left_start = max(0, pos - window_size)
        left_end = pos
        for i in range(left_start, left_end):
            coll_word = word_pos_pairs[i]
            collocation_counter[coll_word] += 1
            left_collocation_counter[coll_word] += 1
        
        # 右边窗口(pos+1, pos+window_size]
        right_start = pos + 1
        right_end = min(N, pos + window_size + 1)
        for i in range(right_start, right_end):
            coll_word = word_pos_pairs[i]
            collocation_counter[coll_word] += 1
            right_collocation_counter[coll_word] += 1
    
    # 移除目标词本身（如果出现）
    if target_word in collocation_counter:
        del collocation_counter[target_word]
    if target_word in left_collocation_counter:
        del left_collocation_counter[target_word]
    if target_word in right_collocation_counter:
        del right_collocation_counter[target_word]
    
    # 计算T值
    t_values = []
    f_target = word_freq[target_word]
    P_target = f_target / N
    
    for word, f_xy in collocation_counter.items():
        # 计算各项概率
        f_x = word_freq[word]
        P_x = f_x / N
        P_xy = f_xy / N
        
        # 计算分子
        numerator = P_xy - (P_x * P_target)
        
        # 计算分母
        if P_xy > 0:
            denominator = math.sqrt(P_xy / N)
        else:
            denominator = 0.0001  # 避免除零
            
        # 计算T值
        t_value = numerator / denominator if denominator != 0 else 0
        
        # 获取左右频数
        f_left = left_collocation_counter.get(word, 0)
        f_right = right_collocation_counter.get(word, 0)
        
        t_values.append({
            'word': word,
            't_value': t_value,
            'freq': f_xy,
            'freq_left': f_left,
            'freq_right': f_right,
            'P_x': P_x,
            'P_xy': P_xy
        })
    
    # 按T值排序
    t_values.sort(key=lambda x: x['t_value'], reverse=True)
    
    return t_values, N, f_target

def save_to_csv(t_values, output_file):
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(['Rank by t', 'Freq', 'Freq(L)', 'Freq(R)', 't值', '搭配词'])
        
        # 写入数据
        for rank, item in enumerate(t_values, 1):
            writer.writerow([
                rank,
                item['freq'],
                item['freq_left'],
                item['freq_right'],
                f"{item['t_value']:.6f}",
                item['word']
            ])

# 主程序
corpus_file = r"C:\Users\Lenovo\Desktop\SRT\语料及处理结果_Python\忽然-文学_segpos.txt"
output_file = r"C:\Users\Lenovo\Desktop\SRT\语料及处理结果_Python\忽然-文学_T值.csv"

try:
    print("开始计算T值...")
    print("注意：处理单元为'词/词性'整体，包括标点符号")
    t_values, N, f_target = calculate_t_value(corpus_file)
    
    print(f"\n统计结果:")
    print(f"语料库大小: {N}")
    print(f"'突然/ad'出现频数: {f_target}")
    print(f"共现词数量: {len(t_values)}")
    
    # 显示前20个结果
    print("\n前20个搭配词:")
    print(f"{'Rank':<6} {'搭配词':<20} {'T值':<12} {'频数':<8} {'左频':<8} {'右频':<8}")
    print("-" * 80)
    for i, item in enumerate(t_values[:20]):
        word_display = item['word'][:18] + "..." if len(item['word']) > 18 else item['word']
        print(f"{i+1:<6} {word_display:<20} {item['t_value']:<12.6f} {item['freq']:<8} {item['freq_left']:<8} {item['freq_right']:<8}")
    
    # 保存所有结果到CSV
    save_to_csv(t_values, output_file)
    print(f"\n结果已保存到: {output_file}")
    
    # 打印一些统计信息
    if t_values:
        print(f"\n最高T值: {t_values[0]['t_value']:.6f} ({t_values[0]['word']})")
        print(f"最低T值: {t_values[-1]['t_value']:.6f} ({t_values[-1]['word']})")
        print(f"平均T值: {sum(item['t_value'] for item in t_values)/len(t_values):.6f}")
        
except FileNotFoundError:
    print(f"错误: 找不到文件 {corpus_file}")
    print("请检查文件路径是否正确。")
except Exception as e:
    print(f"发生错误: {str(e)}")
    import traceback
    traceback.print_exc()