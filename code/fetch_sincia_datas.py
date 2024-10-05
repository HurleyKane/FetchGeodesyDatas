from Fetchlib.FetchFrame import FetchFrame
import os
url = "https://tgm.earth.sinica.edu.tw"


#%%  登录
# frame2 = FetchFrame(home_url=url, download_dir="./")
# frame2.join_username_password(judge_string="陈明锴",)
# frame2.save_cookies("中央研究院.pk1")
# # frame.driver.close() # 关闭浏览器  quit()则结束驱动

#%%  加载cookies
frame2 = FetchFrame(home_url=url, download_dir=os.path.abspath("./"))
frame2.driver.get(url)
frame2.load_cookies("中央研究院.pk1")
frame2.driver.refresh()
frame2.status_join("陈明锴")


#%% 爬取表格数据
# data = frame2.fetch_table("map", table_name="station-table", table_header="thead")
# data.to_csv("station_table.txt")

#%% 下载数据
frame2.download_data(target_name="/Tseries/GS15", link_name="download Time Series")