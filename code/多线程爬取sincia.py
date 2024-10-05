from Fetchlib.FetchFrame import FetchFrame
def download_data(code):
    url = "https://tgm.earth.sinica.edu.tw"
    download_dir = r"D:\data\project\TaiWan GPS\download" + "\code_" + code.split("/")[-1]
    frame2 = FetchFrame(home_url=url, download_dir=download_dir, IsHeadless=True)
    frame2.driver.get(url)
    frame2.load_cookies("中央研究院.pk1")
    frame2.driver.refresh()
    if frame2.status_join(judge_string="陈明锴"):
        print("login success")
    frame2.download_data(code, "download Time Series")
    frame2.driver.quit()
 
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

data = pd.read_csv("station_table.txt", index_col=0, header=0)
codes = ["/Tseries/" +code for code in data.Code.values if type(code) == str]

# 找出codes中为空的文件夹
import os
def get_file_name(path):
    return [f for f in os.listdir(path) if (os.path.exists(os.path.join(path, f))
                                            and not os.listdir(os.path.join(path, f))
                                            )]
# 找出已经没有下载的文件
# codes = get_file_name("./download")
# codes = ["/Tseries/" +code.split("_")[-1] for code in codes]
# 设置线程数量
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(download_data, codes)