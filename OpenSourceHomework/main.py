import requests
import csv
import matplotlib.pyplot as plt
import re
import os

path = "中国各省疫情数据"
if not os.path.exists(path):
    os.mkdir(path)


def get_messgaes(province):
    province = province #当前省份
    # 在中国各省疫情数据下创建每个省份(直辖市, 自治区...)的单独文件夹
    path_everyProvince = path + '/' + province
    if not os.path.exists(path_everyProvince):
        os.mkdir(path_everyProvince)
    # 爬取数据并且保存到csv文件中
    f = open(path_everyProvince + '/' + "{}疫情数据.csv".format(province), mode="w", newline="", encoding="utf-8-sig")
    csv_write = csv.writer(f)
    csv_write.writerow(['日期', '总确诊数', '新增确诊数', '总治愈数', '新增治愈数', '总死亡数', '新增死亡数'])
    url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province={}&'.format(province)
    headers = {
        'Host': 'api.inews.qq.com',
        'Origin': 'https: // news.qq.com',
        'Referer': 'https: // news.qq.com /',
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / '
                        '96.0.4664.110Safari / 537.36Edg / 96.0.1054.62 '
    }
    response = requests.post(url=url, headers=headers)
    response.encoding = response.apparent_encoding
    # print(response)
    datas = response.json()['data']

    dates = []  # 日期
    confirms = []  # 确诊数

    with open(path_everyProvince + '/' + "{}疫情数据.csv".format(province), mode="a+", newline="",
              encoding="utf-8-sig") as f:
        csv_write = csv.writer(f)
        flag = 1
        for data in datas:
            csv_write.writerow(
                [str(data['year']) + '年' + data['date'], data['confirm'], data['newConfirm'], data['heal'],
                 data['newHeal'], data['dead'], data['newDead']])
            #由于爬取到的数据太多，完全显示在图中会导致x轴的文字聚拢在一起，看不清楚，所以设置一个flag，来控制画图时每隔20天为一个数据点
            if (flag % 20 == 0):
                dates.append(str(data['year']) + '年' + data['date'])
                confirms.append(data['confirm'])
            flag += 1
    f.close()
    #画图
    draw_pictures(dates, confirms, province, path_everyProvince)


def draw_pictures(dates, confirms, province, path_everyProvince):
    # 数据可视化
    # print(dates)
    # print(confirms)
    plt.figure(figsize=(12, 8))
    plt.plot(dates, confirms, label="确诊")
    plt.xlabel("日期")
    plt.ylabel("确诊数")
    plt.xticks(rotation=90)  # 横坐标每个值旋转90度
    plt.title("{}确诊数折线图".format(province))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend()
    plt.savefig(path_everyProvince + '/' + '{}.png'.format(province))
    plt.show()


if __name__ == '__main__':
    # 爬取各省的中文名称
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_city_list_order&callback'
    response = requests.get(url=url)
    response.encoding = response.apparent_encoding
    # print(response.json()['data'])
    # print(len(response.json()['data']))
    datas = response.json()['data']
    provinces = re.findall('"province": "(.*?)"', datas)
    citys = re.findall('"city": "(.*?)"', datas)
    # print(provinces)
    # print(citys)
    for province in provinces:
        get_messgaes(province)
        print("{}信息已经爬取完毕".format(province))
