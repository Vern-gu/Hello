from urllib.request import *
from lxml import etree

header = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'
}


def getimage():
    page = input("请输入页数：")
    url = "https://tieba.baidu.com/p/772350816?pn=%s"%page
    request = Request(url,headers=header)
    html = urlopen(request).read().decode("utf-8")
    # print(html)
    content = etree.HTML(html)
    img_urls = content.xpath('//div[contains(@class,"p_content")]/cc/div//@src')
    # xpath的模糊搜索，使用contains方法，第一个属性为包含的标签，第二个属性为包含的关键字
    i = 1
    for img in img_urls:
        loadimage(img)
        print("正在下载第%d张图片" % i)
        i += 1
    print("感谢使用")


def loadimage(img):
    request = Request(img,headers=header)
    image = urlopen(request).read()
    img_name = img[-10:]
    with open("d:/img/"+img_name,"wb") as f:
        f.write(image)


if __name__ == "__main__":
    getimage()
