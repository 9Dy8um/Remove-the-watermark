from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import ContentStream
from PyPDF2.generic import NameObject
# from PyPDF2.generic import b_
def b_(s):
    if type(s) == bytes:
        return s
    else:
        try:
            r = s.encode("latin-1")
            return r
        except Exception:
            r = s.encode("utf-8")
            return r

input_file = 'input.pdf'  # 需要去除水印的pdf文件
output_file = 'out.pdf'  # 去除水印之后的pdf文件
with open(input_file, "rb") as f:
    reader = PdfReader(f, "rb")
    writer = PdfWriter()
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        content_object = page.get_contents()
        content = ContentStream(content_object, reader)
        for index, (operands, operator) in enumerate(content.operations):
            # 判断是否为需要去除的目标，扫描全能王的水印包括一个二维码图像 (['/X1'], b'Do')和一串文本
            if operator == b_('Do') and operands[0] == '/X1' or operator == b_('Tj'):
                del content.operations[index]
        page.__setitem__(NameObject('/Contents'), content)
        writer.add_page(page)
    with open(output_file, "wb") as output_file:
        writer.write(output_file)

