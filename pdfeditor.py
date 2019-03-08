"""
A simple python script to edit pdf files.

@author: QImin Feng
"""

import PyPDF2
import os
import re

class PDFEditor:
    def __init__(self):
        pass
    
    def merge(self, in_files, out_file):
        '''
        合并文档
        :param in_files: 要合并的文档的 list
        :param out_file: 合并后的输出文件
        :return:
        '''        
        pdfFileWriter = PyPDF2.PdfFileWriter()
        for file in in_files:
            # 依次循环打开要合并文件
            pdfReader = PyPDF2.PdfFileReader(open(file, 'rb'))
            numPages = pdfReader.getNumPages()
            for index in range(0, numPages):
                pageObj = pdfReader.getPage(index)
                pdfFileWriter.addPage(pageObj)

            # 最后,统一写入到输出文件中
            pdfFileWriter.write(open(out_file, 'wb'))
    
    def split(self,start,end):
        readFile = '1.pdf'
        outFile = '1-copy.pdf'
        pdfFileWriter = PyPDF2.PdfFileWriter()

        # 获取 PdfFileReader 对象
        pdfFileReader = PyPDF2.PdfFileReader(readFile)  
        # 或者这个方式：pdfFileReader = PdfFileReader(open(readFile, 'rb'))
        # 文档总页数
        numPages = pdfFileReader.getNumPages()

        for index in range(5):
            pageObj = pdfFileReader.getPage(index)
            pdfFileWriter.addPage(pageObj)
        # 添加完每页，再一起保存至文件中
        pdfFileWriter.write(open(outFile, 'wb'))

    

def main():
    # find all the pdf files in current directory.
    mypath = os.getcwd()
    print(mypath)
    pattern = r"\.pdf$"
    file_names_lst = [os.path.join(mypath,f) for f in os.listdir(mypath) if re.search(pattern, f, re.IGNORECASE) and not re.search(r'Merged.pdf',f)]
    print(file_names_lst)
    # merge the file.
    opened_file = [open(file_name,'rb') for file_name in file_names_lst]
    pdfFM = PyPDF2.PdfFileMerger()
    for file in opened_file:
        pdfFM.append(file)

    # output the file.
    with open(mypath + "\\Merged.pdf", 'wb') as write_out_file:
        pdfFM.write(write_out_file)

    # close all the input files.
    for file in opened_file:
        file.close()

def splitPdf(index_page):
    readFile = '1.pdf'
    outFile = '1-copy.pdf'
    pdfFileWriter = PyPDF2.PdfFileWriter()

    # 获取 PdfFileReader 对象
    pdfFileReader = PyPDF2.PdfFileReader(readFile)  # 或者这个方式：pdfFileReader = PdfFileReader(open(readFile, 'rb'))
    # 文档总页数
    numPages = pdfFileReader.getNumPages()

    for index in range(5):
        pageObj = pdfFileReader.getPage(index)
        pdfFileWriter.addPage(pageObj)
    # 添加完每页，再一起保存至文件中
    pdfFileWriter.write(open(outFile, 'wb'))


def mergePdf(inFileList, outFile):
    '''
    合并文档
    :param inFileList: 要合并的文档的 list
    :param outFile:    合并后的输出文件
    :return:
    '''
    pdfFileWriter = PyPDF2.PdfFileWriter()
    for inFile in inFileList:
        # 依次循环打开要合并文件
        pdfReader = PyPDF2.PdfFileReader(open(inFile, 'rb'))
        numPages = pdfReader.getNumPages()
        for index in range(0, numPages):
            pageObj = pdfReader.getPage(index)
            pdfFileWriter.addPage(pageObj)

        # 最后,统一写入到输出文件中
        pdfFileWriter.write(open(outFile, 'wb'))


if __name__ == '__main__':
    main()
        
