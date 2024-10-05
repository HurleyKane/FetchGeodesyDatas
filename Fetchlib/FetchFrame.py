from __future__ import annotations
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# from webdriver_manager.chrome import ChromeDriverManager  # 用于管理启动器

import os
import time
import pickle
import pandas as pd


def wait_for_downloads(download_dir, file_type:str= ".txt", timeout=60):
    seconds = 0
    while seconds < timeout:
        if any(fname.endswith(file_type) for fname in os.listdir(download_dir)):  # 根据文件扩展名检查
            return True
        time.sleep(1)
        seconds += 1
    return False

class FetchFrame:
    __slots__ = ("driver", "home_url", "download_dir")
    def __init__(
        self,
        home_url:str,
        exe_browser_path:str = None,
        download_dir:str = None,
        IsHeadless:bool = False
    ):        
        self.home_url = home_url
        self.download_dir = download_dir
        service = Service(executable_path=r"chromedriver.exe")
        browser_options = Options()
        if exe_browser_path is not None:
            browser_options.binary_location = exe_browser_path
        if download_dir is not None:  # 配置下载路径
            if not os.path.exists(download_dir):
                os.mkdir(download_dir)
            prefs = {"download.default_directory": download_dir}
            browser_options.add_experimental_option("prefs", prefs)
        if IsHeadless:
            browser_options.add_argument("--headless=old")
            browser_options.add_argument("--disable-gpu")  # 禁用 GPU 加速
            browser_options.add_argument("--window-size=1920x1080")  # 设置窗口大小
            browser_options.add_argument("--no-sandbox")  # 对于 Docker 或者 root 用户
            browser_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=service, options=browser_options)
        print("init successfully")
    
    def save_cookies(self, filename:str="cookies.pk1"):
        with open(filename, "wb") as f:
            pickle.dump(self.driver.get_cookies(), f)

    def load_cookies(
            self,
            filename:str
            ):
        with open(filename, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        print("load cookies successfully")

    def status_join(self, judge_string:str)->bool:
        if judge_string in self.driver.page_source:  # 根据实际页面内容调整
            return True
        else:
            return False

    def join_username_password(
            self,
            judge_string:str,
            join_url : str = None,
            username_dict:dict = {'email':'chmingkai@whu.edu.cn'},
            password_dict:dict = {'password':'chen19970719'},
    )->None:
        """
        judge_string:str = "successfully", 登录成功时的一些字符串,用于判断是否登录
        cookies:如果不为None,则加载cookies
        """
        driver = self.driver
        if join_url is None: join_url = self.home_url + "/login"
        
        # 打开登录页面
        driver.get(join_url)
        # 找到用户名和密码输入框并输入信息
        username_input = driver.find_element(By.NAME, list(username_dict.keys())[0])
        password_input = driver.find_element(By.NAME, list(password_dict.keys())[0])

        username_input.send_keys(list(username_dict.values())[0])  # 您的用户名
        password_input.send_keys(list(password_dict.values())[0])  # 您的密码

        # 提交表单
        password_input.send_keys(Keys.RETURN)
        # login_button = driver.find_element(By.NAME, 'submit')
        # login_button.click()

        # 等待页面加载
        time.sleep(2)

        # 检查登录是否成功
        if self.status_join(judge_string):
            print("Login successful!")
        else:
            print("Login failed!")
    
    def fetch_table(
            self,
            target_name:str,
            table_name:str="table",
            table_header:str="thead",
        ) -> pd.DataFrame:
        target_url = self.home_url + "/" + target_name
        driver = self.driver
        driver.get(target_url)
        try:
            table = driver.find_element(By.ID, table_name)
        except:
            print("No table found!")
            return None
        header_row = table.find_element(By.TAG_NAME, table_header).find_elements(By.TAG_NAME, "th")
        columns = [header.get_attribute("innerText") for header in header_row]
        data = []
        from tqdm import tqdm
        if table.text is not None:
            table_row = table.find_elements(By.TAG_NAME, "tr")
            with tqdm(total=len(table_row), desc="fetching table...") as pbar:
                for row in table_row:
                    data_row = row.find_elements(By.TAG_NAME, "td")
                    data_row = [data.get_attribute("innerText") for data in data_row if data.get_attribute("innerText") != ""]
                    data.append(data_row)
                    pbar.update(1)
        df = pd.DataFrame(data, columns=columns)
        return df
    
    def download_data(self, target_name:str, link_name:str, mode="js_link", file_type=".txt") -> None:
        """
        mode: "js_link" is JavaScript link 
        """
        self.driver.get(self.home_url+target_name)
        # 如果该文件夹下存在任意文件，则不进行下载
        if any(fname.endswith(file_type) for fname in os.listdir(self.download_dir)):
            print("File already exists!")
        if mode == "js_link":
            download_link =self.driver.find_element(By.LINK_TEXT, link_name)
            self.driver.execute_script("arguments[0].click();",download_link)
            if wait_for_downloads(self.download_dir, file_type=file_type, timeout=30):
                print("Download completed!")
        else:
            print("mode not supported!")
    

if __name__ == "__main__":
    pass