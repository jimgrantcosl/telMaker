import os
import xml.etree.ElementTree as ET

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainWindow import *

class MyWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow,self).__init__(parent)
        self.setupUi(self)

def initTelfile():
    if os.path.exists('output.tel'):
        os.remove('output.tel')
def telWritelines(tellines):
    with open("output.tel",'a') as fTel:
        fTel.writelines(tellines)
def xmlToTel():
    initTelfile()
    dirpath = os.path.join(os.path.dirname(__file__), "TelTemplate.xml")
    tree = ET.ElementTree(file=dirpath)
    root = tree.getroot()
    for teldef in root.findall("./TelemetryDefinition"):
        telWritelines(teldef.text)
        telWritelines('\n')
    for fidinfo in root.findall("./FIDInfo"):
        for fidname in fidinfo.attrib.values():
            for fiddes in root.findall(".//*[@name='"+fidname+"']/FIDDescription"):
                telWritelines(fiddes.text)
                telWritelines('\n')
            for fidinfo in root.findall(".//*[@name='"+fidname+"']/FIDNum"):
                telWritelines(fidinfo.text)
                telWritelines('\n')
            for fidecc in root.findall(".//*[@name='"+fidname+"']/FIDECC"):
                telWritelines(fidecc.text)
                telWritelines('\n')
            for fiddata in root.findall(".//*[@name='"+fidname+"']/FIDData"):
                for fidval in fiddata.attrib.values():
                    for datainit in root.findall(".//*[@desc='"+fidval+"']/DataInit"):
                        telWritelines(datainit.text)
                        telWritelines(' ')
                    for subnodeitem in root.findall(".//*[@desc='"+fidval+"']/SubNodeItem"):
                        telWritelines(subnodeitem.text)
                        telWritelines(' ')
                    for dataparity in root.findall(".//*[@desc='" + fidval + "']/Parity"):
                        telWritelines(dataparity.text)
                        telWritelines(' ')
                    for subnodeseq in root.findall(".//*[@desc='" + fidval + "']/SubNodeSeq"):
                        telWritelines(subnodeseq.text)
                        telWritelines(' ')
                    for subnodeseqattr in root.findall(".//*[@desc='" + fidval + "']/SubNodeSeqAttr"):
                        telWritelines(subnodeseqattr.text)
                        telWritelines(' ')
                    for nodedescription in root.findall(".//*[@desc='" + fidval + "']/NodeDescription"):
                        telWritelines(nodedescription.text)
                        telWritelines(' ')
                    for subnodedescription in root.findall(".//*[@desc='" + fidval + "']/SubNodeDescrpition"):
                        telWritelines(subnodedescription.text)
                        telWritelines(' ')
                    for subnodeitemalias in root.findall(".//*[@desc='" + fidval + "']/SubNodeItemAlias"):
                        telWritelines(subnodeitemalias.text)
                        telWritelines(' ')
                    telWritelines('\n')
            for fidend in root.findall(".//*[@name='"+fidname+"']/FIDEnd"):
                telWritelines(fidend.text)
                telWritelines(' ')
            telWritelines('\n')
    for teldefend in root.findall("TelemetryDefinitionEnd"):
        telWritelines(teldefend.text)
        telWritelines('\n')

def write_xml():
    root = ET.Element("Telemetry")
    root.tail="\n"
    # 生成根元素
    # 生成子元素 A
    teldef = ET.Element("TelemetryDefinition")
    teldef.text="$$TELEMETRY_DEFINITION ONTRAK"
    teldef.tail="\n"
    fidinfo = ET.Element("FIDInfo")
    fidinfo.set("name", "2400")
    fidinfo.tail="\n"

    fiddes = ET.SubElement(fidinfo, "FIDDescription")
    fiddes.text = "$$SURVEY DIM RAW"
    fiddes.tail = "\n"

    fidnum = ET.SubElement(fidinfo, "FIDNum")
    fidnum.text = "FID 2400"
    fidnum.tail = "\n"

    fidecc = ET.SubElement(fidinfo, "FIDECC")
    fidecc.text = "FID_ERROR_ENCODE ECC_7_4"
    fidecc.tail = "\n"

    fiddata = ET.SubElement(fidinfo, "FIDData")
    fiddata.set("desc", "DIM_INCX")
    fiddata.tail = "\n"

    datainit = ET.SubElement(fiddata, "DataInit")
    datainit.text = "DATA"
    datainit.tail = "\n"

    subnodeitem = ET.SubElement(fiddata, "SubNodeItem")
    subnodeitem.text = "DIM_INCX"
    subnodeitem.tail = "\n"

    parity = ET.SubElement(fiddata, "Parity")
    parity.text = "EVEN_PARITY"
    parity.tail = "\n"

    subnodeseq = ET.SubElement(fiddata, "SubNodeSeq")
    subnodeseq.text = "1"
    subnodeseq.tail = "\n"

    subnodeseqattr = ET.SubElement(fiddata, "SubNodeSeqAttr")
    subnodeseqattr.text = "0"
    subnodeseqattr.tail = "\n"

    nodedescription = ET.SubElement(fiddata, "NodeDescription")
    nodedescription.text = "COSLDrillogNode"
    nodedescription.tail = "\n"

    subnodedescrpition = ET.SubElement(fiddata, "SubNodeDescrpition")
    subnodedescrpition.text = "DIMSvyCmd"
    subnodedescrpition.tail = "\n"

    subnodeitemalias = ET.SubElement(fiddata, "SubNodeItemAlias")
    subnodeitemalias.text = "DIM_INCA"
    subnodeitemalias.tail = "\n"

    fidend = ET.SubElement(fidinfo, "FIDEnd")
    fidend.text = "$$END"
    fidend.tail = "\n"


    teldefend = ET.Element("TelemetryDefinitionEnd")
    teldefend.text = "$$END"
    teldefend.tail="\n"

    # 将a和b 组成一个元组传入extend()方法中，元素 A和B作为根元素的子元素
    root.extend((teldef, fidinfo, teldefend))
    trees = ET.ElementTree(root)
    trees.write(os.path.join(os.path.dirname(__file__), "toTelTemplate.xml"))

def readNode():

    dirpath = os.path.join(os.path.dirname(__file__), "Node1.xml")
    tree = ET.ElementTree(file=dirpath)
    root = tree.getroot()
    for node in root.findall("./Node"):
        for nodename in node.attrib.values():
            print(nodename)
            for subnodename in root.findall(".//*[@Nodename='" + nodename + "']/Subnode"):
                for subnodename in subnodename.attrib.values():
                    print("  -->",subnodename)
                    for subnodeitem in root.findall(".//*[@SubNodeName='" + subnodename + "']/SubNodeItem"):
                        print("    -->name:",subnodeitem.text,"alias:",list(subnodeitem.attrib.values())[0])
            # for subnodename in root.findall(".//*[@SubNodeName='" + nodename + "']/Subnode"):
            #                                (".//*[@name='" + fidname + "']/FIDDescription"):

if __name__ == '__main__':
    xmlToTel()
    write_xml()
    readNode()
    # app = QApplication(sys.argv)
    # myWin = MyWindow()
    # myWin.show()
    # sys.exit(app.exec_())
