from selenium import webdriver
from selenium.webdriver import ActionChains

# 获得各个列表的url，其中url大部分可以直接使用，url1需要再处理
webdrive = webdriver.Chrome()
webdrive.get('https://www.jd.com')
lists = webdrive.find_elements_by_xpath('//ul[@class="JS_navCtn cate_menu"]/li')
actions = ActionChains(webdrive)
list =[]
list1 =[]
for i in lists:
    actions.move_to_element(i).perform()
    webdrive.implicitly_wait(1)
    all_list = webdrive.find_elements_by_xpath('//a[@class="cate_detail_con_lk"]')
    for i in all_list:
        print(i.get_attribute("text"))
        url = i.get_attribute("href")

        if "channel" not in url:
            list.append(url)
            # with open('url.txt','a+') as f:
            #     f.writelines(i)
        else:
            list1.append(url)
            # with open('url1.txt',"a+") as f:
            #     f.writelines(i)
        print(url)
    break
with open("url.txt","w") as f:
    for j in list:
        f.write(j+'\n')
with open("url1.txt","w") as f:
    for j in list1:
        f.write(j+'\n')
