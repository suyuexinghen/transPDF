import re
import sys
import subprocess

#please install poppler-utils to provide 'pdftotext'
#apt install poppler-utils


# 调用pdftotext将PDF转换成文本
input_file = sys.argv[1]
output_file = 'input.txt'
subprocess.run(['pdftotext', input_file, output_file])

# 读取文件内容
with open(output_file, 'r', encoding='utf-8') as f:
    text = f.read()
# 将文本按行切分
lines = text.split('\n')

# 合并相邻的英文句子
result = []
i = 0
while i < len(lines):
    line = lines[i].strip()
    if re.match(r'[a-zA-Z]', line):
        if i < len(lines) - 1:
            next_line = lines[i + 1].strip()
            while re.match(r'[a-zA-Z]', next_line) and i < len(lines) - 1:
                line += ' ' + next_line
                i += 1
                next_line = lines[i + 1].strip()
    result.append(line)
    i += 1

# 将处理后的文本写入文件
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(result))

