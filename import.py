#!/usr/bin/python2


from cStringIO import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from xml.dom.minidom import Document
import glob
import re
import os


def convert_pdf(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    fp = file(path, 'rb')
    process_pdf(rsrcmgr, device, fp)
    fp.close()
    device.close()

    str = retstr.getvalue()
    retstr.close()
    return str


def findnth(haystack, needle, n):
    parts = haystack.split(needle, n + 1)
    if len(parts) <= n + 1:
        return - 1
    return len(haystack) - len(parts[-1]) - len(needle)


def parsePacket(filepath, xml, doc):
    print "Converting " + filepath + " ..."
    content = convert_pdf(filepath)
    qtag = []
    atag = []
    question = []
    answer = []

    maincard = doc.createElement("packet")
    maincard.setAttribute("id", filepath)
    xml.appendChild(maincard)

    for number in range(1, 21):
        contentsub = content[content.find("\n" + str(number) + ". ") + 4:findnth(content, "ANSWER", number - 1)]
        if len(contentsub) == 0:
            contentsub = content[content.find(str(number) + ". ") + 3:findnth(content, "ANSWER", number - 1)]
        contentsub2 = content[findnth(content, "ANSWER:", number - 1) + 8:findnth(content, "<", number - 1)]
        qtag.append(doc.createElement("q" + str(number)))
        question.append(doc.createTextNode(" ".join(contentsub.splitlines())))
        maincard.appendChild(qtag[number - 1])
        qtag[number - 1].appendChild(question[number - 1])
        atag.append(doc.createElement("a" + str(number)))
        answer.append(doc.createTextNode(os.linesep.join([s for s in contentsub2.splitlines() if s])))
        maincard.appendChild(atag[number - 1])
        atag[number - 1].appendChild(answer[number - 1])


def main():
    doc = Document()
    xml = doc.createElement("xml")
    doc.appendChild(xml)

    filelist = glob.glob('*.pdf')
    for filepath in filelist:
        parsePacket(filepath, xml, doc)
    correct = re.sub('&quot;', '"', doc.toprettyxml(indent="  "))
    xml_file = open("output.xml", "w")
    xml_file.write(correct)
    xml_file.close()


if __name__ == "__main__":
    main()
