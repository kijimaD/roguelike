import json


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
open_test1()
