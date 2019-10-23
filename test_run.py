import json
import xml.etree.ElementTree as ET

def test1():
    """json書き込み"""
    dic = {
        "profile0": {
            "first": "Tarou",
            "last": "Tanaka"
        },
        "profile1": {
            "first": "Hanako",
            "last": "Yamada"
        }
    }
    a = open('sample.json', 'w')
    json.dump(dic, a, indent=4)


def open_test1():
    """文章読み込みテスト"""
    file = open('scenario_data.json', 'r', encoding="utf-8")
    data = json.load(file)

    for i in range(2):
        print(f'{data["monologue" + str(i)]["text"]}')
        print(f'talker:({data["monologue" + str(i)]["talker"]})')


# test1()
# open_test1()


def open_test2(id):
    """xmlテスト"""
    tree = ET.parse('scenario_data.xml')
    elem = tree.getroot()
    root = tree.getroot()

    print(elem.tag)
    print(elem.get("id"))
    print('これがid指定:',elem.get("test0"))
    search = elem.get("id", "text0")

    for e in elem.getiterator():
        print(e.tag)

    for name in root.iter('evt'):
        print(name.text)

    print(root.attrib)

    for child in root:
        print(child.attrib)

    reg = ".//evt[@id='{}']"
    set_reg = reg.format(id)
    for e in root.findall(set_reg):
        print("これは検索した結果です:",e.text)

    # for e in root.findall(".//evt[@id='test0']"):
    #     print("これは検索した結果です:",e.text)

open_test2("test1")