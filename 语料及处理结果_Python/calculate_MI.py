import math
import csv
import re
from collections import defaultdict, Counter
from pathlib import Path

def calculate_mi_improved(file_path, window_size=5, sort_by='mi'):
    """
    MI值计算：
    - 使用正则表达式精确提取词/词性格式
    - 使用标准MI公式：MI = log2((AB * N) / (A * B))
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='gbk') as f:
            content = f.read()

    # 使用正则表达式提取 词/词性 格式
    tokens = re.findall(r'([^/\s]+/[^\s]+)', content)
    N = len(tokens)
    token_freq = Counter(tokens)

    # 查找所有"忽然/d"的位置
    target_word = "突然/ad"   # 或 忽然/d,根据需要修改
    sudden_positions = [i for i, token in enumerate(tokens) if token == target_word]
    A = len(sudden_positions)

    if A == 0:
        print(f"未找到'{target_word}'")
        return []

    print(f"语料库总token数 N = {N}")
    print(f"'{target_word}'的总频次 A = {A}")
    print(f"窗口大小: (-{window_size}, {window_size})")

    # 统计搭配信息
    collocate_stats = defaultdict(lambda: {'total': 0, 'left': 0, 'right': 0})

    for pos in sudden_positions:
        # 左侧窗口
        left_start = max(0, pos - window_size)
        for i in range(left_start, pos):
            collocate = tokens[i]
            collocate_stats[collocate]['total'] += 1
            collocate_stats[collocate]['left'] += 1
        
        # 右侧窗口
        right_end = min(N, pos + window_size + 1)
        for i in range(pos + 1, right_end):
            collocate = tokens[i]
            collocate_stats[collocate]['total'] += 1
            collocate_stats[collocate]['right'] += 1

    # 计算MI值
    results = []
    for collocate, counts in collocate_stats.items():
        AB = counts['total']
        B = token_freq.get(collocate, 0)

        if AB > 0 and B > 0:
            mi_value = math.log2((AB * N) / (A * B))
            results.append({
                'collocate': collocate,
                'AB': AB,
                'left_freq': counts['left'],
                'right_freq': counts['right'],
                'B': B,
                'mi_value': mi_value
            })

    # 按指定方式排序
    if sort_by == 'mi':
        results.sort(key=lambda x: x['mi_value'], reverse=True)
    else:  # 按共现频数排序
        results.sort(key=lambda x: x['AB'], reverse=True)

    return results

def save_mi_results_csv(results, output_path, sort_type):
    """保存结果到CSV文件"""
    if not results:
        print("无搭配词结果。")
        return False
    
    try:
        with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['rank', '搭配词', '共现频数', '全局频率', '左侧', '右侧', 'MI值'])
            writer.writeheader()
            for i, r in enumerate(results, 1):
                writer.writerow({
                    'rank': i,
                    '搭配词': r['collocate'],
                    '共现频数': r['AB'],
                    '全局频率': r['B'],
                    '左侧': r['left_freq'],
                    '右侧': r['right_freq'],
                    'MI值': round(r['mi_value'], 4)
                })
        print(f"✓ {sort_type}排序结果已保存: {output_path}")
        return True
    except Exception as e:
        print(f"保存失败: {e}")
        return False

def main():
    # 根据需要设置文件路径
    base_path = r"C:\Users\Lenovo\Desktop\SRT\语料及处理结果_Python\突然-文学_segpos.txt"
    output = r"C:\Users\Lenovo\Desktop\SRT\语料及处理结果_Python\突然-文学_MI.csv"
    
    print(f"处理文件: {base_path}\n")

    # 计算MI值
    print("正在计算MI值...\n")
    mi_results = calculate_mi_improved(base_path, window_size=5, sort_by='freq')

    if mi_results:
        print(f"\n找到 {len(mi_results)} 个搭配词。")

        # 显示前20位按MI值排序的结果
        print("\n" + "=" * 80)
        print(f"{'排名':<6}{'搭配词':<20}{'共现频数':<12}{'全局频率':<12}{'左':<6}{'右':<6}{'MI值':<10}")
        print("-" * 80)
        
        results_by_mi = sorted(mi_results, key=lambda x: x['mi_value'], reverse=True)
        for i, r in enumerate(results_by_mi[:20], 1):
            print(f"{i:<6}{r['collocate']:<20}{r['AB']:<12}{r['B']:<12}{r['left_freq']:<6}{r['right_freq']:<6}{r['mi_value']:<10.4f}")

        # 保存排序结果
        print("\n" + "=" * 80)
        print("保存结果文件...")
        print("=" * 80)
        save_mi_results_csv(results_by_mi, output, "MI值")
    else:
        print("未找到搭配词。")

if __name__ == "__main__":
    main()
