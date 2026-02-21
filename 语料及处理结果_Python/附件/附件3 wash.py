import re

def remove_b_and_u_tags(text):
    # 1. 去除<B>...</B>及其中内容
    text = re.sub(r'<B>.*?</B>', '', text, flags=re.DOTALL)
    # 2. 去除<U>忽然</U>标签，只保留“忽然”
    text = re.sub(r'<U>\s*忽然\s*</U>', '忽然', text)
    # 3. 去除其他<U>...</U>及其中内容（不是“忽然”）
    text = re.sub(r'<U>.*?</U>', '', text, flags=re.DOTALL)
    return text

def main(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"文件 {input_file} 未找到！")
        return

    new_content = remove_b_and_u_tags(content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"处理完成，结果已保存到 {output_file}")

if __name__ == '__main__':
    main('忽然-文学.txt', '忽然-文学_modified.txt')