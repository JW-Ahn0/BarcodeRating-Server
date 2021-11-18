import mysql.connector
import myapp.product
import myapp.bookCrawling
from django.http import JsonResponse


def search_db(request, bar):
    try:

        mysql_con = None
        mysql_con = mysql.connector.connect(host='localhost', port='3306', database='final', user='root',
                                            password='1234')
        mysql_cursor = mysql_con.cursor(dictionary=True)

        sql = "SELECT * FROM final WHERE barcode = %s;"

        var = (str(bar),)
        mysql_cursor.execute(sql, var)
        mysql_list = mysql_cursor.fetchall()
        mysql_cursor = mysql_con.cursor(dictionary=True)

        # 내 db에 없을때
        if mysql_list == []:

            #책이냐
            if str(bar)[0:3] == "978" or str(bar)[0:3] == "979" :
                js = myapp.bookCrawling.bookCrawling(str(bar))
                return JsonResponse(js, safe=False, json_dumps_params={'ensure_ascii': False})
            #아니냐
            else :
                f_d = []
                js = myapp.product.pro_start(str(bar))

                if js == "no":
                    d = [{
                        "type": 'barcode wrong or not in k-net',
                        "img_Url": "",
                        "List": [
                            {
                                "link": "",
                                "name": "",
                                "review": "",
                                "score": ""
                            },
                        ],
                        "title": "",
                        "total_score": "",
                        "total_review": ""
                    }]
                    return JsonResponse(d, safe=False, json_dumps_params={'ensure_ascii': False})
                f_d.append(js)

                mysql_con = None
                mysql_con = mysql.connector.connect(host='localhost', port='3306', database='final', user='root',
                                                    password='1234')
                mysql_cursor = mysql_con.cursor(dictionary=True)

                sql = "SELECT * FROM final WHERE barcode = %s;"
                mysql_cursor.execute(sql, (str(bar),))
                mysql_list = mysql_cursor.fetchall()[0]
                mysql_cursor = mysql_con.cursor(dictionary=True)

                what = mysql_list['what']

                sql = "SELECT * FROM pro_final WHERE what = %s;"
                mysql_cursor.execute(sql, (what,))
                mysql_list = mysql_cursor.fetchall()

                for now_list in mysql_list:
                    if (now_list['barcode'] == str(bar)):
                        continue
                    else:

                        img_url = now_list['url']
                        real_name = now_list['real_name']
                        total_score = now_list['total_score']
                        total_review = now_list['total_review']

                        naver_link = now_list['naver_url']
                        naver_review = now_list['naver_review']
                        naver_score = now_list['naver_total']

                        auction_link = now_list['auction_url']
                        auction_review = now_list['auction_review']
                        auction_score = now_list['auction_total']

                        gmarket_link = now_list['gmarket_url']
                        gmarket_review = now_list['gmarket_review']
                        gmarket_score = now_list['gmarket_total']

                        coupang_link = now_list['coupang_url']
                        coupang_review = now_list['coupang_review']
                        coupang_score = now_list['coupang_total']

                        d = {
                            "type": 'product',
                            "img_Url": img_url,
                            "List": [
                                {
                                    "link": naver_link,
                                    "name": "naver",
                                    "review": naver_review,
                                    "score": naver_score
                                },
                                {
                                    "link": gmarket_link,
                                    "name": "gmarket",
                                    "review": gmarket_review,
                                    "score": gmarket_score
                                },
                                {
                                    "link": auction_link,
                                    "name": "auction",
                                    "review": auction_review,
                                    "score": auction_score
                                },
                                {
                                    "link": coupang_link,
                                    "name": "coupang",
                                    "review": coupang_review,
                                    "score": coupang_score
                                },

                            ],
                            "title": real_name,
                            "total_score": total_score,
                            "total_review": total_review
                        }
                        f_d.append(d)
                return JsonResponse(f_d, safe=False, json_dumps_params={'ensure_ascii': False})





            return js;
        #내 db에 있으면
        else :
            what = mysql_list[0]['what']

            if(what == 'book') :

                sql = "SELECT * FROM book_final WHERE barcode = %s;"
                mysql_cursor.execute(sql, (str(bar),))
                mysql_list = mysql_cursor.fetchall()[0]

                image = mysql_list['url']
                title = mysql_list['name']
                total_score = mysql_list['total_score']
                total_review = mysql_list['total_review']

                kb_url = mysql_list['kb_url']
                kb_star_num = mysql_list['kb_review']
                kb_star = mysql_list['kb_total']

                yes_url = mysql_list['yes_url']
                yes_star_num = mysql_list['yes_review']
                yes_star = mysql_list['yes_total']

                d = [{
                    "type": 'book',
                    "img_Url": image,
                    "List": [
                        {
                            "link": kb_url,
                            "name": "kyobo",
                            "review": kb_star_num,
                            "score": kb_star
                        },
                        {
                            "link": yes_url,
                            "name": "yes24",
                            "review": yes_star_num,
                            "score": yes_star
                        },
                    ],
                    "title": title,
                    "total_score": total_score,
                    "total_review": total_review
                }]
                mysql_con.close()

                return JsonResponse(d, safe=False, json_dumps_params={'ensure_ascii': False})


            else :
                sql = "SELECT * FROM pro_final WHERE barcode = %s;"
                mysql_cursor.execute(sql, (str(bar), ))
                mysql_list = mysql_cursor.fetchall()[0]
                mysql_cursor = mysql_con.cursor(dictionary=True)

                img_url = mysql_list['url']
                real_name = mysql_list['real_name']
                total_score = mysql_list['total_score']
                total_review = mysql_list['total_review']
                what = mysql_list['what']

                naver_link = mysql_list['naver_url']
                naver_review = mysql_list['naver_review']
                naver_score = mysql_list['naver_total']

                auction_link = mysql_list['auction_url']
                auction_review = mysql_list['auction_review']
                auction_score = mysql_list['auction_total']

                gmarket_link = mysql_list['gmarket_url']
                gmarket_review = mysql_list['gmarket_review']
                gmarket_score = mysql_list['gmarket_total']

                coupang_link = mysql_list['coupang_url']
                coupang_review = mysql_list['coupang_review']
                coupang_score = mysql_list['coupang_total']

                f_d = []
                d = {
                    "type": 'product',
                    "img_Url": img_url,
                    "List": [
                        {
                            "link": naver_link,
                            "name": "naver",
                            "review": naver_review,
                            "score": naver_score
                        },
                        {
                            "link": gmarket_link,
                            "name": "gmarket",
                            "review": gmarket_review,
                            "score": gmarket_score
                        },
                        {
                            "link": auction_link,
                            "name": "auction",
                            "review": auction_review,
                            "score": auction_score
                        },
                        {
                            "link": coupang_link,
                            "name": "coupang",
                            "review": coupang_review,
                            "score": coupang_score
                        },

                    ],
                    "title": real_name,
                    "total_score": total_score,
                    "total_review": total_review
                }
                f_d.append(d)

                sql = "SELECT * FROM pro_final WHERE what = %s;"
                mysql_cursor.execute(sql, (what,))
                mysql_list = mysql_cursor.fetchall()

                for now_list in mysql_list:
                    if(now_list['barcode'] == str(bar)):
                        continue
                    else :

                        img_url = now_list['url']
                        real_name = now_list['real_name']
                        total_score = now_list['total_score']
                        total_review = now_list['total_review']

                        naver_link = now_list['naver_url']
                        naver_review = now_list['naver_review']
                        naver_score = now_list['naver_total']

                        auction_link = now_list['auction_url']
                        auction_review = now_list['auction_review']
                        auction_score = now_list['auction_total']

                        gmarket_link = now_list['gmarket_url']
                        gmarket_review = now_list['gmarket_review']
                        gmarket_score = now_list['gmarket_total']

                        coupang_link = now_list['coupang_url']
                        coupang_review = now_list['coupang_review']
                        coupang_score = now_list['coupang_total']

                        d = {
                            "type": 'product',
                            "img_Url": img_url,
                            "List": [
                                {
                                    "link": naver_link,
                                    "name": "naver",
                                    "review": naver_review,
                                    "score": naver_score
                                },
                                {
                                    "link": gmarket_link,
                                    "name": "gmarket",
                                    "review": gmarket_review,
                                    "score": gmarket_score
                                },
                                {
                                    "link": auction_link,
                                    "name": "auction",
                                    "review": auction_review,
                                    "score": auction_score
                                },
                                {
                                    "link": coupang_link,
                                    "name": "coupang",
                                    "review": coupang_review,
                                    "score": coupang_score
                                },

                            ],
                            "title": real_name,
                            "total_score": total_score,
                            "total_review": total_review
                        }
                        f_d.append(d)



                mysql_con.close()

                return JsonResponse(f_d, safe=False, json_dumps_params={'ensure_ascii': False})


    finally:
        if mysql_con is not None:
            mysql_con.close()