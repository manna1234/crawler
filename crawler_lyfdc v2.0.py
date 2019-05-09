# -*- coding: utf-8 -*-
"""
Created on Wed May 17 13:06:53 2017
解析龙岩市房地产信息网的楼盘信息 http://www.fjlyfdc.com.cn
--该网址已经失效，需要迁移http://222.78.94.14/ZL/House/ListProject 楼盘项目大全
@author: manna
使用 urllib.request 、 bs4等库
# python3.5 测试通过。
"""

import requests
from bs4 import BeautifulSoup
import csv


def SaveFile(content, filename):
    with open(filename, "a") as f:
        f.write(str(content) + "\n")


# 解析内容页
def spyder_content(url, p):
    print(url)
    html = getHtmlText(url)
    html = BeautifulSoup(html, "lxml")

    table = html.find(name='table', class_="tablestyles")

    tr = table.find_all(name='tr', limit=50, recursive=False)

    tr1 = tr[1].find_all(name='td', limit=4, recursive=False)
    p["预售许可证"] = tr1[1].get_text()

    tr4 = tr[4].find_all(name='td', limit=4, recursive=False)
    p["土地面积"] = tr4[1].get_text()

    tr5 = tr[5].find_all(name='td', limit=4, recursive=False)
    p["占地面积"] = tr5[1].get_text()
    p["建筑面积"] = tr5[3].get_text()

    tr6 = tr[6].find_all(name='td', limit=4, recursive=False)
    p["容积率"] = tr6[1].get_text()
    p["绿地率"] = tr6[3].get_text()

    tr7 = tr[7].find_all(name='td', limit=4, recursive=False)
    p["建筑密度"] = tr7[1].get_text()
    p["工程投资"] = tr7[3].get_text()

    tr8 = tr[8].find_all(name='td', limit=4, recursive=False)
    p["开工日期"] = tr8[1].get_text()
    p["竣工日期"] = tr8[3].get_text()

    print("建筑密度:{}, 工程投资:{}, 开工日期:{}, 竣工日期:{}".format(p["建筑密度"], p["工程投资"], p["开工日期"], p["竣工日期"]))

    # list_1=['住宅套数','住宅面积','商业套数','商业面积','写字楼套数','写字楼面积', '车库车位套数','车库车位面积','其他套数','其他面积']
    tr12 = tr[12].find_all(name='td', limit=15, recursive=False)
    p["批准销售"] = [tr.get_text() for tr in tr12[1:11]]

    tr13 = tr[13].find_all(name='td', limit=15, recursive=False)
    p["可售统计"] = [tr.get_text() for tr in tr13[1:11]]

    tr14 = tr[14].find_all(name='td', limit=15, recursive=False)
    p["已售统计"] = [tr.get_text() for tr in tr14[1:11]]

    print("批准销售:{}, 可售统计:{}, 已售统计:{}".format(p["批准销售"], p["可售统计"], p["已售统计"]))
    return p


# 解析列表页
def spyder_list(text, website):
    html = BeautifulSoup(text, "lxml")

    table = html.find(name='table', class_="tablestyles text-center")
    print(table)

    for tr in table.find_all(name='tr', limit=30, recursive=False):
        p = {}
        td = tr.find_all(name='td', limit=4, recursive=False)
        print('---------------')
        if td:
            # 项目基本信息
            p["开发企业"] = td[0].get_text()
            p["项目名称"] = td[1].get_text().strip()
            p["项目坐落"] = td[2].get_text()
            p["项目用途"] = td[3].get_text()
            p["URL"] = website + td[1].find(name='a').get('href')
            print(p["项目名称"])

            p = spyder_content(p["URL"], p)

            row_0 = [p[key] for key in p if key not in ['批准销售', '可售统计', '已售统计']]

            row_1 = [r1 for r1 in p['批准销售']]
            row_2 = [r2 for r2 in p['可售统计']]
            row_3 = [r3 for r3 in p['已售统计']]

            writer.writerow(row_0 + row_1 + row_2 + row_3)


def getHtmlText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"


if __name__ == "__main__":
    website = 'http://222.78.94.14'

    with open('a.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for page in range(1, 2):
            url = website + '/ZL/House/ListProject?pagenumber={}&pagesize=15'.format(str(page))
            print(url)
            text = getHtmlText(url)
            spyder_list(text, website)
