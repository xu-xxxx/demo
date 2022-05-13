import requests

import re
import json,collections



data = {
        'bank': '口座振込',
        'mile': 'マイル',
        'suika':'スカイコイン',
        'gift': 'GIFT',
        'paypal': 'Paypal'
    } 

decoder =  json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
print(decoder.decode(json.dumps(data)))

p = re.compile('[\u30A1-\u30FF]+')
print(p.fullmatch('アイウエオァィゥェォ'))
print(">>>>>>>>>>>>>>>")
print(p.fullmatch('アイウエオ'))
print(">>>>>>>>>>>>>>>")
print(p.fullmatch('日本語'))
print(">>>>>>>>>>>>>>>")
print(p.fullmatch('カタカナ'))
print(">>>>>>>>>>>>>>>")
print(p.fullmatch('ｶﾀｶﾅ'))
print(">>>>>>>>>>>>>>>")

# <re.Match object; span=(0, 10), match='アイウエオァィゥェォ'>

p = re.compile('[\ァ-ヿ]+')
print(p.fullmatch('アイウエオァィゥェォ'))
# <re.Match object; span=(0, 10), match='アイウエオァィゥェォ'>

p = re.compile('[\uFF66-\uFF9F]+')
print(p.fullmatch('ｱｲｳｴｵｧｨｩｪｫ'))
# <re.Match object; span=(0, 10), match='ｱｲｳｴｵｧｨｩｪｫ'>

p = re.compile('[ｦ-ﾟ]+')
print(p.fullmatch('ｱｲｳｴｵｧｨｩｪｫ'))
# <re.Match object; span=(0, 10), match='ｱｲｳｴｵｧｨｩｪｫ'>




pattern = r'\b\d{4}/\d{2}/\d{2}\b'
# result = re.findall(pattern, '2021/03/160 あいうえお')
# print(result)  # []
# result = re.findall(pattern, 'あ 2021/03/160 あいうえお')
# print(result)  # []
# result = re.findall(pattern, '2021/03/16 あいうえお')
# print(result)  # ['2021/03/16']
# result = re.findall(pattern, 'あ 2021/03/16 あいうえお')
# print(result)  # ['2021/03/16']


#pattern = r'2022/02/22'
#pattern = r'(20[0-9]{2})/([1-9]|1[0-2])/([1-9]|[12][0-9]|3[01])'
#pattern = r'[12]\d{3}/(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])'
#pattern = r'(20[0-9]{2})/([1-9]|1[0-2])/([1-9]|[12][0-9]|3[01])'
pattern = r'[12]\d{3}[/\-年](0?[1-9]|1[0-2])[/\-月](0?[1-9]|[12][0-9]|3[01])日?$'

string = r'2099/02/30'
prog = re.compile(pattern)
result = prog.match(string)
if result:
    print(result.group())



def get_receipts():
    headers = {'Content-type': 'application/json'}
    r = requests.get('http://localhost:5555/receipt_types')

    print(f"statusCode: {r.status_code}")
    print(r.text)
    resp_dict = r.json()
    print(resp_dict)
    for key in resp_dict:  print(f"{key}: {resp_dict[key]}")


if __name__ == '__main__':
    #get_receipts()
    pass

