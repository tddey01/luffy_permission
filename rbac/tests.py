from django.test import TestCase

# Create your tests here.
from selenium import webdriver
import time
import pymysql


# 获取页面产品的超链接
def get_data(nfex_url):
    page_href = []
    driver = webdriver.Chrome()
    driver.implicitly_wait(20)
    driver.get(nfex_url)
    # 获取新窗口的平台产品信息，只需要项目名称信息
    new_window = driver.find_element_by_xpath("//*[@id='content']")
    new_window_content = new_window.text  # 只获取标签对应的内容
    page_content = new_window_content.split('\n')  # 根据空格来分割数据并放入page_text列表中
    project_name = page_content[0]
    # 创建以项目名称命名的txt文件，把项目介绍存储到txt格式的文件里
    filename = project_name + '.txt'
    # 获取新窗口的项目介绍
    driver.find_element_by_link_text("项目介绍").send_keys('\n')
    # 点击“项目介绍按钮的时候，需要加等待时间，要不然就会报错Message: element not interactable
    time.sleep(3)
    # 获取项目介绍的内容
    new_window_introduction = driver.find_element_by_xpath('//*[@id="introduction"]')
    new_introduction = new_window_introduction.text  # 只获取标签对应的内容
    # page_introduction = new_introduction.split('\n')  # 根据空格来分割数据并放入page_text列表中
    # page_text.append(page_introduction)  # 把页数添加到列表中
    print('get_data的new_introduction的：%s' % new_introduction)
    cur_dir = r'C:\\Users\\user.DESKTOP-LMSSL63\\PycharmProjects\\untitled1\\nfex\\'
    # 创建文件到指定路径下,保存项目介绍的信息
    file_path = cur_dir + filename
    f = open(file_path, 'w')
    f.write(new_introduction)
    f.write('\n')
    # 获取新窗口的投标记录
    driver.find_element_by_link_text("投标记录").send_keys('\n')
    time.sleep(3)
    # 点击尾页，获取投标记录的最大页数
    driver.find_element_by_link_text("尾页").send_keys('\n')
    time.sleep(3)
    # 获取投标记录里面的翻页的页数
    page_num = driver.find_element_by_xpath('//*[@id="investRecord"]/div[2]/ul')
    page_num_text = page_num.text              # 只获取标签对应的内容
    page_num_list = page_num_text.split('\n')  # 根据空格来分割数据并放入page_text列表中
    page_num_max = int(page_num_list[-3])
    print('get_page_href的page_num_max：%s' % page_num_max)
    while 1 <= page_num_max:
        try:
            invest_record = driver.find_element_by_xpath('//*[@id="investRecordTable"]')
            new_invest_record = invest_record.text  # 只获取标签对应的内容
            page_invest_record = new_invest_record.split('\n')  # 根据空格来分割数据并放入page_text列表中
            deal_data(page_invest_record, project_name, page_href)
            # print('get_data的page_investRecord的：%s' % page_invest_record)
            # 因为页面表格的翻页是通过“<a href="javascript:void(0);">下一页</a>”js形式加载，所以使用这种翻页操作
            driver.find_element_by_link_text("上一页").send_keys('\n')
            time.sleep(3)
        except Exception as e:
            print('get_data的e：%s' % e)
            pass
        page_num_max = page_num_max - 1
    driver.quit()
    print('get_page_href的page_href：%s' % page_href)
    conn_database(page_href)
    return page_href


def deal_data(page_invest_record, project_name, page_href):
    invest_record_data = []
    for i in range(len(page_invest_record)):
        invest_record_data1 = []
        if i > 0:
            invest_record_data.append(project_name)
            invest_record_data = page_invest_record[i].split(' ')
            if len(invest_record_data) == 5:
                line_num = invest_record_data[0]  # 页面上的行号
                investors = invest_record_data[1]  # 页面上的投资人
                invest_amount = invest_record_data[2]  # 页面上的投资金额
                invest_time = invest_record_data[3] + ' ' + invest_record_data[4]  # 页面上的投资时间
                invest_record_data1.append(project_name)
                invest_record_data1.append(line_num)
                invest_record_data1.append(investors)
                invest_record_data1.append(invest_amount)
                invest_record_data1.append(invest_time)
                print('get_data的invest_record_data1的：%s' % invest_record_data1)
                page_href.append(invest_record_data1)  #
            else:
                pass
        else:
            pass
    #print('deal_data的page_href：%s' % page_href)
    return page_href


#把需要的数据插入到数据库
def conn_database(insert_list):
    print('开始插入：%s' % insert_list)
    sql_insert = 'insert into investRecord(project_name, line_num, investors, invest_amount, invest_time) ' \
                 'values(%s, %s, %s, %s, %s)'
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='jacklee_123', db='pachong_schema')
        cursor = conn.cursor()
        count_row = cursor.executemany(sql_insert, insert_list)
        conn.commit()
        cursor.close()
        conn.close()
        print(count_row)
    except Exception as e:
        print('conn_database的e：%s' % e)
        pass
    return count_row


#读取项目的详细信息超链接
def get_domains():
    domain_list = []
    try:
        file_object = open('nfex.txt', 'r')
        for line in file_object:
            line = line.strip('\n')
            domain_list.append(line)
    finally:
        file_object.close()
    print('get_domains的domain_list：%s' % domain_list)
    return domain_list

if __name__ == '__main__':
    #https://www.nfex.com/front/invest/invest?bidId=2
    #https://www.nfex.com/front/invest/invest?bidId=5071
    nfex_urls = get_domains()
    print('get_domains的nfex_urls：%s' % nfex_urls)
    print('get_domains的nfex_urls：%s' % len(nfex_urls))
    for i in range(len(nfex_urls)):
        get_data(nfex_urls[i])
