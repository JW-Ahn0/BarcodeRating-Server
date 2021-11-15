import mysql.connector
import urllib.request
from bs4 import BeautifulSoup


def mysql_scan(request):
    try:
        mysql_con = None
        mysql_con = mysql.connector.connect(host='localhost', port='3306', database='test', user='root',
                                            password='1234')

        mysql_cursor = mysql_con.cursor(dictionary=True)

        num = 1
        ssg = urllib.request.urlopen(
            "http://emart.ssg.com/disp/category.ssg?dispCtgId=6000096324&pageSize=100&page=" + str(num))
        ssg_soup = BeautifulSoup(ssg, 'html.parser')

        sql = "INSERT IGNORE INTO test2_table (name, what) VALUES ( %s,%s );"
        title_all = ssg_soup.find_all('div', "title")
        for now in title_all:
            name = now.find('em', "tx_ko").get_text()
            name_all = name.split(' ')
            for now_name in name_all:
                val = (now_name, "생수")
                mysql_cursor.execute(sql, val)

        mysql_con.commit()
        mysql_cursor.close()


    finally:
        if mysql_con is not None:
            mysql_con.close()

