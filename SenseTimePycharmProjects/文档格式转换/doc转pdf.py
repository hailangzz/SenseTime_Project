from docx2pdf import convert

import subprocess

def convert_to_pdf(input_file, output_file):
    command = ['libreoffice', '--headless', '--convert-to', 'pdf', input_file, '--outdir', output_file]
    subprocess.run(command)

# 将docx文件转换为pdf文件
convert_to_pdf('/home/SENSETIME/zhangzhuo/Documents/标注规范——说明文档/animal/RoadSemantics动物标注规范-20230708.docx', '/home/SENSETIME/zhangzhuo/Documents/标注规范——说明文档/animal/RoadSemantics动物标注规范-20230708.pdf')


# 将doc文件转换为pdf文件
#convert("/home/SENSETIME/zhangzhuo/Documents/交通灯分类标注文档v50.docx", "/home/SENSETIME/zhangzhuo/Documents/交通灯分类标注文档v50.pdf")
