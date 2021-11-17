import mysql.connector
import urllib.request
from bs4 import BeautifulSoup
import time

def start(request):
    mysql_ssg_search()

def mysql_cate_1st():
    try:
        mysql_con = None
        mysql_con = mysql.connector.connect(host='localhost', port='3306', database='category', user='root',
                                            password='1234')
        mysql_cursor = mysql_con.cursor(dictionary=True)

        ssg = urllib.request.urlopen("http://emart.ssg.com/")
        ssg_soup = BeautifulSoup(ssg, 'html.parser')

        # ssg가 3초 이내면 막아버림
        time.sleep(3)

        # 전체 list
        list = ssg_soup.find_all('ul', "em_lnb_lst")

        # foodlist
        food_list = list[0]

        # lifelist
        life_list = list[1]

        # foodlist db에 추가
        first_class_list = food_list.find_all('li', attrs={'class', 'emlnb_top_mn'})
        sql = "INSERT INTO food_1st (name, category) VALUES ( %s,%s );"
        for now in first_class_list:
            food = now.find('a')
            foodname = food.get_text()
            foodcate = str(food).split("javascript:Category.goCategory('")[1].split("'")[0]

            val = (foodname, foodcate)
            mysql_cursor.execute(sql, val)

        mysql_con.commit()

        # lifelist db에 추가
        first_class_list = life_list.find_all('li', attrs={'class', 'emlnb_top_mn'})
        sql = "INSERT INTO life_1st (name, category) VALUES ( %s,%s );"
        for now in first_class_list:
            life = now.find('a')
            lifename = life.get_text()
            lifecate = str(life).split("javascript:Category.goCategory('")[1].split("'")[0]

            val = (lifename, lifecate)
            mysql_cursor.execute(sql, val)

        mysql_con.commit()

    finally:
        if mysql_con is not None:
            mysql_con.close()


def mysql_cate_2st():
    try:
        mysql_con = None
        mysql_con = mysql.connector.connect(host='localhost', port='3306', database='category', user='root', password='1234')
        mysql_cursor = mysql_con.cursor(prepared=True)

        # food_1st에서 긁어오기
        sql = "SELECT * FROM food_1st"
        mysql_cursor.execute(sql)

        mysql_food_1st = mysql_cursor.fetchall()
        mysql_cursor = mysql_con.cursor(prepared=True)

        id = 0
        name = 1
        category = 2

        # food_1st category 로 food_2st긁어오기
        for now_category in mysql_food_1st:
            food_id = now_category[id]
            food_category = now_category[category]



            ssg = urllib.request.urlopen("http://emart.ssg.com/category/main.ssg?dispCtgId=" + str(food_category))
            ssg_soup = BeautifulSoup(ssg, 'html.parser')

            # ssg가 3초 이내면 막아버림
            time.sleep(3)

            food_2st_title_list = ssg_soup.find_all('ul', 'cmflt_ctlist_high cmfltExpClist notranslate')

            # 숨어있는 title도 있어서 여러개를 긁어야함
            for now_food_2st_title_list in food_2st_title_list:

                food_2st_list = now_food_2st_title_list.find_all('li')

                # 내용물 긁기 및 db에 저장
                for now_food in food_2st_list:
                    food_2st_name = now_food.get_text()
                    food_2st_category = str(now_food).split('data-ilparam-value="')[1].split('"')[0]
                    sql = "INSERT INTO food_2st (name , category, parent_id ) VALUES ( %s , %s, %s )"
                    val = (food_2st_name, food_2st_category, food_id)
                    mysql_cursor.execute(sql, val)

                mysql_con.commit()



        mysql_cursor = mysql_con.cursor(prepared=True)

        # life_1st에서 긁어오기
        sql = "SELECT * FROM life_1st"
        mysql_cursor.execute(sql)

        mysql_life_1st = mysql_cursor.fetchall()
        mysql_cursor = mysql_con.cursor(prepared=True)

        id = 0
        name = 1
        category = 2

        # life_1st category 로 life_2st긁어오기
        for now_category in mysql_life_1st:
            life_id = now_category[id]
            life_category = now_category[category]



            ssg = urllib.request.urlopen("http://emart.ssg.com/category/main.ssg?dispCtgId=" + str(life_category))
            ssg_soup = BeautifulSoup(ssg, 'html.parser')

            # ssg가 2초 이내면 막아버림
            time.sleep(3)


            life_2st_title_list = ssg_soup.find_all('ul', 'cmflt_ctlist_high cmfltExpClist notranslate')

            # 숨어있는 title도 있어서 여러개를 긁어야함
            for now_life_2st_title_list in life_2st_title_list:

                life_2st_list = now_life_2st_title_list.find_all('li')

                # 내용물 긁기 및 db에 저장
                for now_life in life_2st_list:
                    life_2st_name = now_life.get_text()
                    life_2st_category = str(now_life).split('data-ilparam-value="')[1].split('"')[0]
                    sql = "INSERT INTO life_2st (name , category, parent_id ) VALUES ( %s , %s, %s )"
                    val = (life_2st_name, life_2st_category, life_id)
                    mysql_cursor.execute(sql, val)

                mysql_con.commit()

    finally:
        if mysql_con is not None:
            mysql_con.close()


def mysql_cate_3st():
    try:
        mysql_con = None
        mysql_con = mysql.connector.connect(host='localhost', port='3306', database='category', user='root',
                                            password='1234')
        mysql_cursor = mysql_con.cursor(prepared=True)
        # food_2st에서 긁어오기
        sql = "SELECT * FROM food_2st"
        mysql_cursor.execute(sql)

        mysql_food_2st = mysql_cursor.fetchall()
        mysql_cursor = mysql_con.cursor(prepared=True)

        id = 0
        name = 1
        category = 2

        # food_2st category 로 food_3st긁어오기
        for now_category in mysql_food_2st:
            food_id = now_category[id]
            food_name = now_category[name]
            food_category = now_category[category]

            ssg = urllib.request.urlopen("http://emart.ssg.com/category/main.ssg?dispCtgId=" + str(food_category))
            ssg_soup = BeautifulSoup(ssg, 'html.parser')

            # ssg가 3초 이내면 막아버림
            time.sleep(3)

            food_3st_title_list = ssg_soup.find_all('ul', 'cmflt_ctlist notranslate')

            # 3단계가 없는 아이들이 있음. 그럴시 2단계 그대로 내려 오도록 조치함.
            if len(food_3st_title_list) == 0:
                sql = "INSERT INTO food_3st (name , category, parent_id ) VALUES ( %s , %s, %s )"
                val = (food_name, food_category, food_id)
                mysql_cursor.execute(sql, val)

            else:
                # 숨어있는 title도 있어서 여러개를 긁어야함
                for now_food_3st_title_list in food_3st_title_list:

                    food_3st_list = now_food_3st_title_list.find_all('li')

                    # 내용물 긁기 및 db에 저장
                    for now_food in food_3st_list:
                        food_3st_name = now_food.get_text('\n', strip=True)
                        food_3st_category = str(now_food).split('data-ilparam-value="')[1].split('"')[0]
                        sql = "INSERT INTO food_3st (name , category, parent_id ) VALUES ( %s , %s, %s )"
                        val = (food_3st_name, food_3st_category, food_id)
                        mysql_cursor.execute(sql, val)

            mysql_con.commit()

        mysql_cursor = mysql_con.cursor(prepared=True)

        # life_2st에서 긁어오기
        sql = "SELECT * FROM life_2st"
        mysql_cursor.execute(sql)

        mysql_life_2st = mysql_cursor.fetchall()
        mysql_cursor = mysql_con.cursor(prepared=True)

        id = 0
        name = 1
        category = 2

        # life_2st category 로 life_3st긁어오기
        for now_category in mysql_life_2st:
            life_id = now_category[id]
            life_name = now_category[name]
            life_category = now_category[category]

            ssg = urllib.request.urlopen("http://emart.ssg.com/category/main.ssg?dispCtgId=" + str(life_category))
            ssg_soup = BeautifulSoup(ssg, 'html.parser')

            # ssg가 3초 이내면 막아버림
            time.sleep(3)

            life_3st_title_list = ssg_soup.find_all('ul', 'cmflt_ctlist notranslate')

            # 3단계가 없는 아이들이 있음. 그럴시 2단계 그대로 내려 오도록 조치함.
            if len(life_3st_title_list) == 0:
                sql = "INSERT INTO life_3st (name , category, parent_id ) VALUES ( %s , %s, %s )"
                val = (life_name, life_category, life_id)
                mysql_cursor.execute(sql, val)

            else:
                # 숨어있는 title도 있어서 여러개를 긁어야함
                for now_life_3st_title_list in life_3st_title_list:

                    life_3st_list = now_life_3st_title_list.find_all('li')

                    # 내용물 긁기 및 db에 저장
                    for now_life in life_3st_list:
                        life_3st_name = now_life.get_text('\n', strip=True)
                        life_3st_category = str(now_life).split('data-ilparam-value="')[1].split('"')[0]
                        sql = "INSERT INTO life_3st (name , category, parent_id ) VALUES ( %s , %s, %s )"
                        val = (life_3st_name, life_3st_category, life_id)
                        mysql_cursor.execute(sql, val)

            mysql_con.commit()



    finally:
        if mysql_con is not None:
            mysql_con.close()

def mysql_ssg_search():
    try:
        mysql_con = None
        mysql_con = mysql.connector.connect(host='localhost', port='3306', database='category', user='root',
                                            password='1234')

        mysql_cursor = mysql_con.cursor(prepared=True)

        """
        # food_3st에서 긁어오기
        sql = "SELECT * FROM food_3st"
        mysql_cursor.execute(sql)

        mysql_food_3st = mysql_cursor.fetchall()
        mysql_cursor = mysql_con.cursor(prepared=True)

        id = 0
        category = 2

        # food_3st category 로 page 단어 가져오기
        for now_category in mysql_food_3st:
            food_id = now_category[id]
            food_category = now_category[category]
            if food_id < 364:
                continue


            ssg = urllib.request.urlopen("http://emart.ssg.com/category/main.ssg?dispCtgId=" + str(food_category) + "&pageSize=100" + "&page=" + str(1))
            ssg_soup = BeautifulSoup(ssg, 'html.parser')

            # ssg가 3초 이내면 막아버림
            time.sleep(3)

            # 전체 page 개수
            food_length = ssg_soup.find('div', 'com_paginate notranslate').find('a', 'btn_last on')
            if food_length is None:
                length_final = ssg_soup.find('div', 'com_paginate notranslate')
                length = (int)(str(length_final).count('changePage(')) + 1

            else:
                length = (int)(str(food_length).split('changePage(')[1].split(')')[0])

            set_name_list = set()
            # 각 page 마다 단어 긁어오기
            for page in range(1, length + 1):

                ssg = urllib.request.urlopen("http://emart.ssg.com/category/main.ssg?dispCtgId=" + str(
                    food_category) + "&pageSize=100" + "&page=" + str(page))
                ssg_soup = BeautifulSoup(ssg, 'html.parser')

                # ssg가 3초 이내면 막아버림
                time.sleep(3)

                title_list = ssg_soup.find_all('div', 'cunit_md notranslate')

                for title in title_list:
                    total_name = title.find('em', 'tx_ko').get_text()
                    name_list = total_name.split(' ')

                    trash = ['', 'x', ' ', '!', 'X', '+', '~', '-','/']
                    for name in name_list:
                        if name not in trash:
                            set_name_list.add(name)



            sql = "INSERT INTO food_name (name , food_3st_id ) VALUES ( %s , %s )"
            for name in set_name_list:
                val = (name, food_id)
                mysql_cursor.execute(sql, val)
            mysql_con.commit()
            
        """
        # life_3st에서 긁어오기
        sql = "SELECT * FROM life_3st"
        mysql_cursor.execute(sql)

        mysql_life_3st = mysql_cursor.fetchall()
        mysql_cursor = mysql_con.cursor(prepared=True)

        id = 0
        category = 2

        # life_3st category 로 page 단어 가져오기
        for now_category in mysql_life_3st:

            life_id = now_category[id]
            life_category = now_category[category]

            if ( (life_id > 300) and (life_id < 309 )):
                time.sleep(0.1)
            else :
                if life_id < 402:
                    continue

            ssg = urllib.request.urlopen("http://emart.ssg.com/category/main.ssg?dispCtgId=" + str(life_category) + "&pageSize=100" + "&page=" + str(1))
            ssg_soup = BeautifulSoup(ssg, 'html.parser')

            # ssg가 3초 이내면 막아버림
            time.sleep(3)

            # 전체 page 개수
            life_length = ssg_soup.find('div', 'com_paginate notranslate')
            if life_length is None:
                continue
            life_length = life_length.find('a', 'btn_last on')
            if life_length is None:
                length_final = ssg_soup.find('div', 'com_paginate notranslate')
                length = (int)(str(length_final).count('changePage(')) + 1

            else:
                length = (int)(str(life_length).split('changePage(')[1].split(')')[0])

            set_name_list = set()
            # 각 page 마다 단어 긁어오기
            for page in range(1, length + 1):

                ssg = urllib.request.urlopen("http://emart.ssg.com/category/main.ssg?dispCtgId=" + str(
                    life_category) + "&pageSize=100" + "&page=" + str(page))
                ssg_soup = BeautifulSoup(ssg, 'html.parser')

                # ssg가 3초 이내면 막아버림
                time.sleep(3)

                title_list = ssg_soup.find_all('div', 'cunit_md notranslate')

                for title in title_list:
                    total_name = title.find('em', 'tx_ko').get_text()
                    name_list = total_name.split(' ')

                    trash = ['', 'x', ' ', '!', 'X', '+', '~', '-', '/']
                    for name in name_list:
                        if name not in trash:
                            set_name_list.add(name)


            sql = "INSERT INTO life_name (name , life_3st_id ) VALUES ( %s , %s )"
            for name in set_name_list:
                val = (name, life_id)
                mysql_cursor.execute(sql, val)
            mysql_con.commit()


    finally:
        if mysql_con is not None:
            mysql_con.close()