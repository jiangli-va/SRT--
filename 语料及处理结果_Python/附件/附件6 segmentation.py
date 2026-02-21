import os
import jieba.posseg as pseg


def process_line(line: str) -> str:
    if not line:
        return ''
    return ' '.join(f"{w.word}/{w.flag}" for w in pseg.cut(line))


def process_file(input_path: str, output_path: str = None):
    if output_path is None:
        output_path = input_path + '.segpos.txt'
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(input_path, 'r', encoding='utf-8') as fin, open(output_path, 'w', encoding='utf-8') as fout:
        for line in fin:
            line = line.strip()
            fout.write(process_line(line) + '\n')
    return output_path


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='按行读取文件并用 jieba 做分词+词性标注')
    parser.add_argument('input', help='输入文件路径（每行一条文本）')
    parser.add_argument('--output', '-o', help='输出文件路径（默认 input + .segpos.txt）')
    args = parser.parse_args()

    out_path = process_file(args.input, args.output)
    print('写入：', out_path)