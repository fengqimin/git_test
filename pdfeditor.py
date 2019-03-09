"""
A simple python script to edit pdf files.

@author: QImin Feng
"""

import PyPDF2
import os
import re


class PDFEditor:
    def __init__(self, pdf_file_path, password=''):
        pass


def extract_text(file_path, start=0, end=0):
    """提取文本，很可能出错"""
    assert end >= start
    text = []
    with open(file_path, 'rb') as fp:
        pdfReader = PyPDF2.PdfFileReader(fp)

        for page_num in range(pdfReader.numPages):
            page = pdfReader.getPage(page_num)
            text.append(page.extractText())
    if end == 0:
        return text[start:]
    return text[start:end]


def rotate(in_file_path, out_file_path, rotation):
    """旋转pdf页"""
    in_file = open(in_file_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(in_file)
    pdfWriter = PyPDF2.PdfFileWriter()

    for page in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(page)
        pageObj.rotateClockwise(rotation)

        pdfWriter.addPage(pageObj)

    out_file = open(out_file_path, 'wb')
    pdfWriter.write(out_file)

    in_file.close()
    out_file.close()


def crop(input_file: str, start: int = 0, *, end: int, output_file='output.pdf'):
    """裁剪pdf文件"""
    pdfFileWriter = PyPDF2.PdfFileWriter()  # 获取 PdfFileReader 对象
    pdfFileReader = PyPDF2.PdfFileReader(open(input_file, 'rb'))
    # 文档总页数
    numPages = pdfFileReader.getNumPages()
    assert end >= start and end <= numPages

    # 添加完每页，再一起保存至文件中
    for index in range(start, end):
        pageObj = pdfFileReader.getPage(index)
        pdfFileWriter.addPage(pageObj)
    # 保存
    pdfFileWriter.write(open(output_file, 'wb'))


def split(input_file: str, split_nums: list, output_files: list = []):
    """分割pdf文件
    split(r'D:\My Projects\Python\Application\data\test.pdf', [1, 5, 10])
    """
    # 文档总页数
    pdfFileReader = PyPDF2.PdfFileReader(open(input_file, 'rb'))
    numPages = pdfFileReader.getNumPages()
    if len(output_files) != 0:
        assert len(split_nums)+1 == len(output_files)
    assert split_nums[-1] <= numPages

    if len(output_files) == 0:
        for i in range(len(split_nums)+1):
            output_files.append('output%r.pdf' % i)

    start = 0
    # 根据分割的页码进行裁剪
    for i in range(len(split_nums)):
        crop(input_file, start=start,
             end=split_nums[i], output_file=output_files[i])
        start = split_nums[i]
    # 裁剪最后一个分割
    crop(input_file, start, end=numPages, output_file=output_files[-1])


def merge(files_or_dir, output_file):
    """合并pdf文件"""
    # 创建一个pdf文件合并对象
    pdf_merger = PyPDF2.PdfFileMerger()
    pattern = re.compile(r"(?i)\.pdf$")

    if os.path.isdir(files_or_dir):
        files = []
        for path in os.listdir(files_or_dir):
            if pattern.search(path) and not re.search(path, output_file):
                files.append(os.path.join(files_or_dir, path))
    else:
        files = files_or_dir

    # 逐个添加pdf
    for pdf in files:
        with open(pdf, 'rb') as fr:
            pdf_merger.append(fr)

    # 将内存中合并的pdf文件写入
    with open(output_file, 'wb') as fw:
        pdf_merger.write(fw)


def add_watermark(watermark_file, in_file, output_file):
    """从水印文件中增加水印"""

    def _add(wm_file, page_object):
        # 打开水印pdf文件
        wm_file_obj = open(wm_file, 'rb')

        # 创建pdfReader对象，把打开的水印pdf传入
        _reader = PyPDF2.PdfFileReader(wm_file_obj)

        # 将水印pdf的首页与传入的原始pdf的页进行合并
        page_object.mergePage(_reader.getPage(0))

        wm_file_obj.close()
        return page_object

    # 创建reader对象
    pdfReader = PyPDF2.PdfFileReader(open(in_file, 'rb'))

    # 创建一个指向新的pdf文件的指针
    pdfWriter = PyPDF2.PdfFileWriter()

    # 通过迭代将水印添加到原始pdf的每一页
    for page in range(pdfReader.numPages):
        wmPageObj = _add(watermark_file, pdfReader.getPage(page))
        # 将合并后的即添加了水印的page对象添加到pdfWriter
        pdfWriter.addPage(wmPageObj)

    # 将已经添加完水印的pdfWriter对象写入文件
    pdfWriter.write(open(output_file, 'wb'))


if __name__ == "__main__":
    split(r'D:\My Projects\Python\Application\data\test.pdf', [1, 5, 10])

