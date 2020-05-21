import os
import requests
from selenium import webdriver
from pyquery import PyQuery as pq
# driver = webdriver.PhantomJS()
# 其他浏览器把 Chrome 换名就行
option = webdriver.ChromeOptions()
# 设置无头浏览器，就是隐藏界面后台运行
option.headless = True
# 新版 Selenium 需要下载相应浏览器的driver
exe_path = r"C:\Users\Tao\Projects\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(executable_path=exe_path,
                          chrome_options=option)


"""
组成部分
1. Downloader 下载页面          requests
2. HTMLParser 解析页面          pyquery     lxml
3. DataModel 字段 - element     业务逻辑

1. 先下载页面，如果没有更新过应该不在下载第二次
2. 这个拆分可以方便逻辑的扩展
"""


class Model(object):
    """
    基类, 用来显示类的信息
    """
    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class Movie(Model):
    """
    存储电影信息
    """
    def __init__(self):
        self.name = ''
        self.score = 0
        self.quote = ''
        self.cover_url = ''
        self.ranking = 0


def cached_url(url):
    """
    缓存，避免重复下载网页
    """
    folder = 'cached'
    filename = url.split('=', 1)[-1] + '.html'
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as fin:
            s = fin.read()
            return s
    else:
        # 创建 cached 文件夹
        if not os.path.exists(folder):
            os.makedirs(folder)

        driver.get(url)
        # return driver.page_source
        # 发送网络请求，把结果写入到文件夹中
        with open(path, 'wb') as fout:
            fout.write(driver.page_source.encode())
        content = driver.page_source
        return content


def movie_from_div(div):
    """
    从一个 div 里面获取到一个电影信息
    """
    e = pq(div)

    # 小作用域变量用单字符
    m = Movie()
    m.name = e('.title').text()
    m.score = e('.rating_num').text()
    m.quote = e('.inq').text()
    m.cover_url = e('img').attr('src')
    m.ranking = e('.pic').find('em').text()

    return m


def movies_from_url(url):
    """
    从 url 中下载网页并解析出页面内所有的电影
    只会下载一次
    """
    page = cached_url(url)
    # 1. 解析 dom
    # 2. 找到父节点
    # 3. 每个子节点拿一个 movie
    e = pq(page)
    # pring(page.decode())
    items = e('.item')
    # 调用 movie_from_div
    movies = [movie_from_div(it) for it in items]
    return movies


def download_image(url):
    folder = 'img'
    name = url.split('/')[-1]
    path = os.path.join(folder, name)

    if not os.path.exists(folder):
        os.makedirs(folder)
    if os.path.exists(path):
        return

    headers = {
        'user-agent': '''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8''',
    }
    # 发送网络请求, 把结果写入到文件夹中
    r = requests.get(url, headers)
    with open(path, 'wb') as f:
        f.write(r.content)


def main():
    for i in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start={}'.format(i)
        movies = movies_from_url(url)
        print('top250 movies', movies)
        [download_image(m.cover_url) for m in movies]


if __name__ == '__main__':
    main()
