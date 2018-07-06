import requests
import re
import pymysql
import uuid
import random
import time
import datetime

class ErShouFangInfoBean(object):
    def __init__(self,detailUrl,title,houseAddressInfo,housePositionInfo,followInfo,tagInfo,priceInfo):
        #详情url
        self.detailUrl = detailUrl
        #标题
        self.title = str(title).replace(' ',"")
        #小区名
        self.villageName = houseAddressInfo[0][1]
        #小区url
        self.villageDetailUrl = houseAddressInfo[0][0]
        # 两种情况
        # 5室2厅 | 168.11平米 | 北 | 精装 | 有电梯
        # 5室1厅 | 178.75平米 | 南 北 | 其他
        # 4室2厅 | 153.49平米 | 南 | 毛坯
        tmpList = houseAddressInfo[0][2].lstrip()[1:].split("|")
        #几室几厅
        self.severalRoomsAndRooms = tmpList[0]
        #平方米
        self.squareMeter = tmpList[1]
        #方位
        self.direction = tmpList[2]
        #精装 毛坯 简装
        if tmpList[3].find("精装") or tmpList[3].find("简装") \
            or tmpList[3].find("毛坯") or tmpList[3].find("其他"):
            self.decorationStatus = tmpList[3]
        else:
            self.decorationStatus = None
        #有无电梯
        if len(tmpList) == 5:
            if tmpList[4] == "有电梯":
                self.hasElevator = '1'
            else:
                self.hasElevator = '0'
        else:
            self.hasElevator = "-1"
        #楼层
        self.floor = str(housePositionInfo[0][0]).replace(' ',"")
        #地区
        self.area = housePositionInfo[0][2]
        #地区url
        self.areaUrl = str(housePositionInfo[0][1])
        #关注人数
        self.followCount = "共"+re.match('\d+人',followInfo[0][0]).group(0)
        #带看次数
        self.hasVisitCount = re.match('(.*?)(\d+)次',followInfo[0][1]).group(2)
        #发布时间
        publistTime = re.match('\d+(天|个月|年)', followInfo[0][2].strip())
        if publistTime is not None:
            self.pulishTime = publistTime.group(0)
        else:
            self.pulishTime = ""

        if tagInfo[0][1] != '' and tagInfo[0][1] == "subway":
            #交通
            self.subway = str(tagInfo[0][2])
        if tagInfo[0][1] != '' and tagInfo[0][1] == "taxfree":
            # taxfree
            self.taxfree = str(tagInfo[0][2])
        if tagInfo[0][1] != '' and tagInfo[0][1] == "haskey":
            # haskey
            self.haskey = str(tagInfo[0][2])
        if tagInfo[0][4] != '' and tagInfo[0][4] == "subway":
            # 交通
            self.subway = str(tagInfo[0][5])
        if tagInfo[0][4] != '' and tagInfo[0][4] == "taxfree":
            # taxfree
            self.taxfree = str(tagInfo[0][5])
        if tagInfo[0][4] != '' and tagInfo[0][4] == "haskey":
            # haskey
            self.haskey = str(tagInfo[0][5])

        if tagInfo[0][7] != '' and tagInfo[0][7] == "subway":
            # 交通
            self.subway = str(tagInfo[0][8])
        if tagInfo[0][7] != '' and tagInfo[0][7] == "taxfree":
            # taxfree
            self.taxfree = str(tagInfo[0][8])
        if tagInfo[0][7] != '' and tagInfo[0][7] == "haskey":
            # haskey
            self.haskey = str(tagInfo[0][8])
        try:
            if self.subway is None:
                self.subway = "无地铁"
        except Exception:
            self.subway = "无地铁"
        try:
            if self.haskey is None:
                self.haskey = "无钥匙"
        except Exception:
            self.haskey = "无钥匙"
        try:
            if self.taxfree is None:
                self.taxfree = "无房本"
        except Exception as e:
            self.taxfree = "无房本"

        #总价
        self.amountPrice = str(priceInfo[0][0] + priceInfo[0][1])
        #单价
        self.price = str(priceInfo[0][2])



class Mysql(object):
    def __init__(self,url,username,password):
        self.db = pymysql.connect(host=url,user=username,passwd=password,db="lianjia",charset="utf8")
        self.cursor = self.db.cursor()
    def createHouseBasicInfoTable(self):
        sql = "create table houseBasicInfo(id varchar(200) not null primary key,detailUrl varchar(200) not null ,title varchar(500) not null,villageName varchar(200),villageDetailUrl varchar(200),severalRoomsAndRooms varchar(50),squareMeter varchar(20),direction varchar(20),decorationStatus varchar(20),hasElevator varchar(10),floor varchar(100),area varchar(50),areaUrl varchar(60),followCount varchar(5),hasVisitCount varchar(5),pulishTime varchar(10),subway varchar(20),taxfree varchar(20),haskey varchar(20),amountPrice varchar(10),price varchar(30))"
        self.cursor.execute("drop table if exists houseBasicInfo")
        self.cursor.execute(sql)
    def insertHouseBasicInfo(self,houseInfoBean):
        id = str(uuid.uuid1())
        insertSql = "insert into housebasicinfo(id,detailUrl,title,villageName,villageDetailUrl,severalRoomsAndRooms,squareMeter," \
                    "direction,decorationStatus,hasElevator,floor,area,areaUrl,followCount,hasVisitCount,pulishTime," \
                    "subway,taxfree,haskey,amountPrice,price) values("\
                    +"'"+id+"'"+","+"'"+houseInfoBean.detailUrl+"'"+","+"'"+houseInfoBean.title+"'"+","\
                    +"'"+houseInfoBean.villageName+"'"+","+"'"+houseInfoBean.villageDetailUrl+"'"+","\
                    +"'"+houseInfoBean.severalRoomsAndRooms+"'"+","+"'"+houseInfoBean.squareMeter+"'"+","\
                    +"'"+houseInfoBean.direction+"'"+","+"'"+houseInfoBean.decorationStatus+"'"+","+"'"+houseInfoBean.hasElevator+"'"+","+"'"+houseInfoBean.floor+"'"+","+"'"+houseInfoBean.area\
                    +"'"+","+"'"+houseInfoBean.areaUrl+"'"+","+"'"+houseInfoBean.followCount\
                    +"'"+","+"'"+houseInfoBean.hasVisitCount+"'"+","+"'"+houseInfoBean.pulishTime+"'"+","+"'"+houseInfoBean.subway+"'"+","+"'"+houseInfoBean.taxfree\
                    +"'"+","+"'"+houseInfoBean.haskey+"'"+","+"'"+houseInfoBean.amountPrice+"'"+","+"'"+houseInfoBean.price+"')"
        print(insertSql)
        print("开始时间："+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.cursor.execute(insertSql)
        self.db.commit()
        print("结束时间：" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))



headers = {"Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    "Accept-Language": "en-US,en;q=0.9",
    "Host": "cs.lianjia.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Cookie":"select_city=430100; all-lj=c60bf575348a3bc08fb27ee73be8c666; lianjia_uuid=ba449656-bf3b-45ab-b9ae-a997a23cd801; TY_SESSION_ID=bc3e77e5-5dbf-456c-95e2-56f1235b65c1; _smt_uid=5b3e3630.30ec7bc1; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1530803761; UM_distinctid=1646b03b1932c7-0060abbe2a74b9-5e442e19-100200-1646b03b1954d1; _jzqc=1; _jzqx=1.1530803763.1530803763.1.jzqsr=cs%2Elianjia%2Ecom|jzqct=/.-; _jzqckmp=1; _jzqy=1.1530803764.1530803764.1.jzqsr=baidu.-; _qzjc=1; _ga=GA1.2.228796767.1530803767; _gid=GA1.2.1670144435.1530803767; lianjia_ssid=e7c16967-261b-4a4f-8796-e4a8ff72e2c9; CNZZDATA1255849590=1308287498-1530801852-https%253A%252F%252Fwww.baidu.com%252F%7C1530875470; CNZZDATA1254525948=2010740866-1530800802-https%253A%252F%252Fwww.baidu.com%252F%7C1530876402; CNZZDATA1255633284=839588307-1530800185-https%253A%252F%252Fwww.baidu.com%252F%7C1530875789; CNZZDATA1255604082=1604249253-1530803514-https%253A%252F%252Fwww.baidu.com%252F%7C1530879116; _jzqa=1.1793164360814349600.1530803763.1530803763.1530880831.2; _gat=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; _qzja=1.1563955562.1530803763692.1530803763692.1530880830344.1530880830344.1530880858996.0.0.0.3.2; _qzjb=1.1530880830344.2.0.0.0; _qzjto=2.1.0; _jzqb=1.2.10.1530880831.1; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1530880864"
}

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

def getWebSiteContentFromUrl(url):
    headers["User-Agent"] = random.choice(USER_AGENTS)
    result = requests.get(url,headers=headers)
    content = result.content
    return content;

def parseContent(content):
    pattern = re.compile('<li class="clear">(.*?)</li>', re.S)
    content = content.decode("utf-8")
    list = pattern.findall(content)
    pageList = []
    for item in list:
        detailUrl = re.findall('href=\"(.*?\.html)\" target=\"_blank\"', item).__getitem__(0)
        title = re.findall('<div class="title"><a .*?>(.*?)</a></div>', item)[0]
        houseAddressInfo = re.findall(
            '<div class=\"houseInfo\"><span class=\"houseIcon\"></span><a href=\"(.*?)\" .*?>(.*?)</a>(.*?)</div>',
            item, re.S)
        housePositionInfo = re.findall(
            '<div class="positionInfo"><span class="positionIcon"></span>(.*?)<a href=\"(.*)\" target=\"_blank\">(.*?)</a></div>',
            item)
        followInfo = re.findall('<div class="followInfo"><span class="starIcon"></span>(.*?)/(.*?)/(.*?)</div>', item);
        tagInfo = re.findall(
            '<div class="tag">(<span class="(.*?)">(.*?)</span>){0,1}(<span class="(.*?)">(.*?)</span>){0,1}(<span class="(.*?)">(.*?)</span>){0,1}</div>',
            item)
        priceInfo = re.findall(
            '<div class="priceInfo">.*?<span>(.*?)</span>(.*?)</div>.*<span>(.*?)</span></div></div>', item)

        esfInfoBean = ErShouFangInfoBean(detailUrl,title,houseAddressInfo,housePositionInfo,followInfo,tagInfo,priceInfo);
        pageList.append(esfInfoBean)
    return pageList

if __name__ == '__main__':
    baseUrl = "https://cs.lianjia.com/ershoufang/pg"
    ershoufangStartUrl = "https://cs.lianjia.com/ershoufang/pg1"
    rand = random.randint(3,20)
    time.sleep(rand)
    content = getWebSiteContentFromUrl(ershoufangStartUrl)
    allPageCount = re.findall('"totalPage":(\d+)', content.decode("utf-8"))[0]
    mysql = Mysql("127.0.0.1", "root", "root")
    mysql.createHouseBasicInfoTable()
    for i in range(int(allPageCount)-1):
        rand = random.randint(3, 20)
        time.sleep(rand)
        url = baseUrl + str(i+1)
        print("-------------------url------------------")
        print(url)
        print("-------------------url------------------")
        content = getWebSiteContentFromUrl(url)
        beanList = parseContent(content)
        print("--------------------------beanList-------------------------")
        print(beanList)
        print("--------------------------beanList-------------------------")
        for houseInfoBean in beanList:
            try:
                mysql.insertHouseBasicInfo(houseInfoBean)
            except Exception as e:
                print(e)
                print("----------------------------------------------------------")
                print(houseInfoBean)
                print("----------------------------------------------------------")
                continue







