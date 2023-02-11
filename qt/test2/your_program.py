from selenium import webdriver

def a():
    a = webdriver.Chrome(r'D:\迅雷下载\chromedriver.exe')

    a.get('https://www.baidu.com/')
    print(a)
    print(str(a))
    return str(a)
# print(a.find_element_by_xpath('//*[@id="s-top-left"]').text)

    a.close()

if __name__ == '__main__':
    a()