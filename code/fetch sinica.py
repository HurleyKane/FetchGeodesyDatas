from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager

from hello import hello

# 创建一个浏览器实例
options = Options()
service = Service(ChromeDriverManager().install())
options.binary_location = r'C:\Users\Administrator\AppData\Local\Google\Chrome\Bin\Google Chrome.exe' 
# service = Service(r"D:\sfotware\miniconda3\Scripts\chromedriver.exe")
driver = webdriver.Chrome(service=service, options = options)

try:
    # 打开网页
    driver.get("https://www.example.com")

    # 打印网页标题
    print("网页标题:", driver.title)

    # 示例：查找一个元素并打印其文本
    element = driver.find_element(By.TAG_NAME, "h1")
    print("元素文本:", element.text)

finally:
    # 关闭浏览器
    driver.quit()
