import argparse
import os
import re

import PyPDF2


def add_watermark(*, watermark_file, input_file, output_file=None):
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

    if watermark_file is None:
        print('watermark file is None.')
    assert input_file, 'File is None'
    assert output_file, 'File is None'

    # 创建reader对象
    pdf_reader = PyPDF2.PdfFileReader(open(input_file, 'rb'))

    # 创建一个指向新的pdf文件的指针
    pdf_writer = PyPDF2.PdfFileWriter()

    # 通过迭代将水印添加到原始pdf的每一页
    for page in range(pdf_reader.numPages):
        wm_page_obj = _add(watermark_file, pdf_reader.getPage(page))
        # 将合并后的即添加了水印的page对象添加到pdfWriter
        pdf_writer.addPage(wm_page_obj)

    # 将已经添加完水印的pdfWriter对象写入文件
    pdf_writer.write(open(output_file, 'wb'))


def crop(*, input_file: str, output_file=None, start_page: int, end_page: int):
    """裁剪pdf文件"""
    pdf_file_writer = PyPDF2.PdfFileWriter()  # 获取 PdfFileReader 对象
    pdf_file_reader = PyPDF2.PdfFileReader(open(input_file, 'rb'))
    # 文档总页数
    num_pages = pdf_file_reader.getNumPages()
    assert start_page <= end_page <= num_pages
    if output_file is None:
        output_file = 'cropped.pdf'
    # 添加完每页，再一起保存至文件中
    for index in range(start_page, end_page):
        page_obj = pdf_file_reader.getPage(index)
        pdf_file_writer.addPage(page_obj)
    # 保存
    pdf_file_writer.write(open(output_file, 'wb'))


def extract_text(*, input_file, start_page=0, end_page=0):
    """提取文本，很可能出错"""
    assert end_page >= start_page
    text = []
    with open(input_file, 'rb') as fp:
        pdf_reader = PyPDF2.PdfFileReader(fp)

        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text.append(page.extractText())
    if end_page == 0:
        return text[start_page:]
    return text[start_page:end_page]


def merge(*, files_or_dir: list = None, output_file: str = None):
    """合并pdf文件"""
    # 创建一个pdf文件合并对象
    pdf_merger = PyPDF2.PdfFileMerger()
    pattern = re.compile(r"(?i)\.pdf$")
    if files_or_dir is None:
        files_or_dir = '.'
    if output_file is None:
        output_file = 'merged.pdf'

    if files_or_dir[0] == '.':
        files = []
        for path in os.listdir(files_or_dir[0]):
            if pattern.search(path) and not re.search(path, output_file):
                files.append(os.path.join(files_or_dir[0], path))
    else:
        files = files_or_dir

    # 逐个添加pdf
    for pdf_file in files:
        pdf_merger.append(open(pdf_file, 'rb'))

    # 将内存中合并的pdf文件写入
    pdf_merger.write(open(output_file, 'wb'))


def rotate(*, input_file, output_file=None, rotation):
    """旋转pdf页"""
    in_file = open(input_file, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(in_file)
    pdf_writer = PyPDF2.PdfFileWriter()
    if output_file is None:
        output_file = 'rotated.pdf'

    for page in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page)
        page_obj.rotateClockwise(rotation)

        pdf_writer.addPage(page_obj)

    out_file = open(output_file, 'wb')
    pdf_writer.write(out_file)

    in_file.close()
    out_file.close()


def split(*, input_file: str, split_nums: list, output_files: list = None):
    """分割pdf文件
    """
    # 文档总页数
    pdf_file_reader = PyPDF2.PdfFileReader(open(input_file, 'rb'))
    num_pages = pdf_file_reader.getNumPages()
    if len(output_files) != 0:
        assert len(split_nums) + 1 == len(output_files)
    assert split_nums[-1] <= num_pages

    if output_files is None:
        for i in range(len(split_nums) + 1):
            output_files.append('output%r.pdf' % i)

    start = 0
    # 根据分割的页码进行裁剪
    for i in range(len(split_nums)):
        crop(input_file=input_file, start_page=start, end_page=split_nums[i], output_file=output_files[i])
        start = split_nums[i]
    # 裁剪最后一个分割
    crop(input_file=input_file, start_page=start, end_page=num_pages, output_file=output_files[-1])


OPERATION = {
    'add': add_watermark,
    'crop': crop,
    'extract': extract_text,
    'merge': merge,
    'rotate': rotate,
    'split': split,
}


def cmdline():
    parser = argparse.ArgumentParser(description="PDF Editor")
    parser.add_argument(
        'opt', metavar='OPERATION',
        help='Operation:add, crop, extract, merge, rotate, split')
    parser.add_argument(
        '--input', '-i', action='store', nargs='+', dest='input_files',
        help='input pdf files path')
    parser.add_argument(
        '--output', '-o', action='store', nargs='*', dest='output_files',
        help="output pdf files path")
    parser.add_argument(
        '--start', '-s', action='store', type=int, dest='start_page_number',
        default=0, help="start page number")
    parser.add_argument(
        '--end', '-e', action='store', type=int, dest='end_page_number',
        help="end page number")
    parser.add_argument(
        '--rotation', '-r', action='store', type=float, dest='rotation',
        help="rotation angle")
    parser.add_argument(
        '--num', '-n', action='store', nargs='+', type=list, dest='split_nums',
        help="split page numbers")
    parser.add_argument(
        '--watermark', '-w', action='store', dest='watermark_file',
        help='watermark pdf file path')

    args = parser.parse_args()
    if not args.opt:
        print('Use --help for command line help')
        return
    if args.opt not in ('add', 'crop', 'extract', 'merge', 'rotate', 'split'):
        print("Supported operations:'add', 'crop', 'extract', 'merge', 'rotate', 'split'")
        print('Use --help for command line help')
        return

    print(args)

    def _editor():
        input_file_path = args.input_files
        output_file_path = args.output_files
        watermark_file_path = args.watermark_file
        split_nums = args.split_nums
        rotation = args.rotation
        start_page_number = args.start_page_number
        end_page_number = args.end_page_number

        if args.opt == 'add':
            add_watermark(watermark_file=watermark_file_path[0],
                          input_file=output_file_path[0] if output_file_path else None,
                          output_file=output_file_path)
        elif args.opt == 'crop':
            crop(input_file=input_file_path[0],
                 output_file=output_file_path[0] if output_file_path else None,
                 start_page=start_page_number,
                 end_page=end_page_number)
        elif args.opt == 'extract':
            text = extract_text(input_file=input_file_path[0],
                                start_page=start_page_number,
                                end_page=end_page_number)
            print(text)
        elif args.opt == 'merge':
            merge(files_or_dir=input_file_path,
                  output_file=output_file_path[0] if output_file_path else None)
        elif args.opt == 'rotate':
            rotate(input_file=input_file_path[0],
                   output_file=output_file_path[0] if output_file_path else None,
                   rotation=rotation)
        elif args.opt == 'split':
            split(input_file=input_file_path[0],
                  output_files=output_file_path,
                  split_nums=split_nums)

    _editor()


if __name__ == "__main__":
    cmdline()
