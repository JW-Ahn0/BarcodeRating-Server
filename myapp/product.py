import requests as rq
from bs4 import BeautifulSoup as bf
from django.http import JsonResponse
import urllib.request
import mysql.connector
import re

def pro_start(barcode) :
    re = search_ko(barcode)
    if re == "no" :
        d = {
            "type": 'not in k-net',
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
        }
        return JsonResponse(d, safe=False, json_dumps_params={'ensure_ascii': False})
    js = product(re)
    return js


def search_name(real_name) :

    mysql_con = None
    mysql_con = mysql.connector.connect(host='localhost', port='3306', database='category', user='root', password='1234')
    mysql_cursor = mysql_con.cursor(dictionary=True)

    sql_food = "SELECT * FROM food_name WHERE name = %s"
    sql_life = "SELECT * FROM life_name WHERE name = %s"

    name_list = real_name.split(' ')

    final_what = ''
    final_id = ''
    final_name = ''

    full_name = [""] * 635
    for name_list2 in name_list :
        name_list3 = name_list2.split('_')
        for name in name_list3 :
            mysql_cursor.execute(sql_food, (name, ))
            mysql_list = mysql_cursor.fetchall()
            mysql_cursor = mysql_con.cursor(dictionary=True)

            if mysql_list == [] :
                continue
            else :
                for now_name in mysql_list:
                    now_id = now_name['food_3st_id']
                    full_name[now_id] = full_name[now_id] + now_name['name'] + ' '



    for i in range(1, 634) :
        if len(full_name[i]) > len(final_name) :
            final_name = full_name[i]
            final_id = i
            final_what = 'food'



    full_name = [""] * 1105
    for name_list2 in name_list:
        name_list3 = name_list2.split('_')
        for name in name_list3:
            mysql_cursor.execute(sql_life, (name, ))
            mysql_list = mysql_cursor.fetchall()
            mysql_cursor = mysql_con.cursor(dictionary=True)

            if mysql_list == []:
                continue
            else:

                for now_name in mysql_list:
                    now_id = now_name['life_3st_id']
                    full_name[now_id] = full_name[now_id] + now_name['name'] + ' '



    for i in range(1, 1103):
        if len(full_name[i]) > len(final_name):
            final_name = full_name[i]
            final_id = i
            final_what = 'life'

    if final_what == 'food' :
        sql = "SELECT * FROM food_3st WHERE id = %s"
        mysql_cursor.execute(sql, (final_id, ))
        mysql_list = mysql_cursor.fetchall()[0]

        what = mysql_list['name']
    else :
        sql = "SELECT * FROM life_3st WHERE id = %s"
        mysql_cursor.execute(sql, (final_id,))
        mysql_list = mysql_cursor.fetchall()[0]

        what = mysql_list['name']

    mysql_con.close()
    return final_name, what




def search_ko(barcode) :

    mysql_con = None
    mysql_con = mysql.connector.connect(host='localhost', port='3306', database='final', user='root', password='1234')
    mysql_cursor = mysql_con.cursor(dictionary=True)

    sql = "SELECT * FROM final WHERE barcode = %s"
    mysql_cursor.execute(sql, (barcode, ))
    mysql_list = mysql_cursor.fetchall()
    mysql_cursor = mysql_con.cursor(dictionary=True)
    if mysql_list == [] :
        bar_webpage = urllib.request.urlopen('http://www.koreannet.or.kr/home/hpisSrchGtin.gs1?gtin=' + str(barcode))
        bar_soup = bf(bar_webpage, 'html.parser')


        title = bar_soup.find('div', "productTit")

        if title is None:
            return "no"

        stitle = str(title.get_text()).split(' ', 2)[2].split('\n')[0].split('\r')[0]
        img_url = str(bar_soup.find('div', "imgArea")).split('src="')[1].split('"')[0]

        name, what = search_name(stitle)

        sql = "INSERT IGNORE INTO final (real_name, name , barcode , img_url, what) VALUES (%s ,%s, %s, %s, %s)"
        var = (stitle, name , str(barcode), img_url, what)
        mysql_cursor.execute(sql, var)
        mysql_con.commit()
        mysql_con.close()
    else :
        name = mysql_list[0]['name']
    return name



def search_naver(name,  sortflag):
    naver_shopping = "https://search.shopping.naver.com/search/all?query="
    naver_shopping += name
    sort = "&sort=review&timestamp=&viewType=list"
    if sortflag == 1:
        naver_shopping += sort
    req = rq.get(naver_shopping)
    raw = req.text
    html = bf(raw, 'html.parser')
    count = 0
    score = 0.0
    review = 0
    totalscore=0.0
    totalreview=0
    productlist = html.find_all('div', class_='basicList_info_area__17Xyo')
    for item in productlist:
        if item.find('span', class_='basicList_graph__ZV6s9') is not None:  # 항목에 별점이 존재하는 경우
            score = float(item.find('span', class_='basicList_graph__ZV6s9').text[3:])
            review = int(item.find('a', class_='basicList_etc__2uAYO').find('em',class_='basicList_num__1yXM9').text.replace(",", ""))
            totalreview+=review
            totalscore += (score * review)
        else:
            count += 1
    if count == productlist.__len__() and sortflag != 1:  # 별점이 존재하는 항목이 1개도없는 경우 리뷰많은 순으로 다시 검색해서 리턴
        return search_naver(name, 1)
    if sortflag ==1 and count == productlist.__len__():
        print("검색결과가 존재하지않습니다.")
        return naver_shopping, totalscore, totalreview
    if(totalreview != 0):
        totalscore /=totalreview
    totalscore = round(totalscore,2)
    # 네이버 쇼핑링크, 별점, 리뷰 수 리턴
    return naver_shopping, totalscore, totalreview
def search_coupang(name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    count = 0
    score = 0.0
    review = 0
    totalscore=0.0
    totalreview=0

    coupang_shopping = "https://www.coupang.com/np/search?component=&q="
    coupang_shopping += name
    req = rq.get(coupang_shopping,headers=headers)
    raw = req.text
    html = bf(raw, 'html.parser')

    productlist = html.find_all('li', class_='search-product')
    for item in productlist:
        if item.find('div', class_='rating-star') is not None:  # 항목에 별점이 존재하는 경우
            score = float(item.find('em', class_='rating').text[:])
            review = int( str(item.find('span', class_='rating-total-count').text[1:-1]).replace(',',"") )
            totalreview += review
            totalscore += (score * review)
        else :
            count += 1
    if count == productlist.__len__():
        print("검색결과가 존재하지않습니다.")
        return coupang_shopping, totalscore, totalreview
    if(totalreview != 0):
        totalscore /=totalreview
    totalscore = round(totalscore,2)
    # 쿠팡 쇼핑링크, 별점, 리뷰 수 리턴
    return coupang_shopping, totalscore, totalreview
def search_auction(name):
    count = 0
    score = 0.0
    review = 0
    totalscore=0.0
    totalreview=0

    auction_shopping = "https://browse.auction.co.kr/search?keyword="
    auction_shopping += name
    auction_shopping += "&s=13" #리뷰많은순으로 추가
    req = rq.get(auction_shopping)
    raw = req.text
    html = bf(raw, 'html.parser')
    productlist = html.find_all('div', class_='component component--item_card type--general')

    for item in productlist:
        if item.find('li', class_='item awards') is not None:  # 항목에 별점이 존재하는 경우
            score = float(item.find('li', class_='item awards').text[5:-2])
            review = int( str(item.find('span', class_='text--reviewcnt').text[3:]).replace(',',"") )
            totalreview += review
            totalscore += (score * review)
        else :
            count += 1
    if count == productlist.__len__():
        print("검색결과가 존재하지않습니다.")
        return auction_shopping, totalscore, totalreview

    if(totalreview != 0):
        totalscore /=totalreview
    totalscore = round(totalscore,2)
    # 옥션 쇼핑링크, 별점, 리뷰 수 리턴
    return auction_shopping, totalscore, totalreview
def search_gmarket(name):
    count = 0
    score = 0.0
    review = 0
    totalscore=0.0
    totalreview=0

    gmarket_shopping = "https://browse.gmarket.co.kr/search?keyword="
    gmarket_shopping += name
    gmarket_shopping += "&s=13" #리뷰많은순으로 추가
    req = rq.get(gmarket_shopping)
    raw = req.text
    html = bf(raw, 'html.parser')

    productlist = html.find_all('div', class_='box__component box__component-itemcard box__component-itemcard--general')
    for item in productlist:
        if item.find('span', class_='image__awards-points') is not None:  # 항목에 별점이 존재하는 경우
            if item.find('li', class_='list-item list-item__feedback-count') is not None and item.find('span', class_='image__awards-points') is not None:
                review = int ( str(item.find('li', class_='list-item list-item__feedback-count').find('span',class_='text').text[1:-1]).replace(',',"") )
                score = float(re.sub(r'[^0-9]','',item.find('span', class_='image__awards-points').text[:])  )/20
                totalscore += (score * review)
                totalreview += review
        else:
            count += 1
    if count == productlist.__len__():
        print("검색결과가 존재하지않습니다.")
        return gmarket_shopping, totalscore, totalreview

    if (totalreview != 0):
        totalscore /= totalreview
    totalscore = round(totalscore, 2)
    # 지마켓 쇼핑링크, 별점, 리뷰 수 리턴
    return gmarket_shopping, totalscore, totalreview


def product(name):

    title = str(name)

    total_review = 0
    total_score = 0.0
    naver_link, naver_score, naver_review = search_naver(title, 0)
    gmarket_link, gmarket_score,gmarket_review = search_gmarket(title)
    auction_link, auction_score, auction_review = search_auction(title)
    coupang_link, coupang_score, coupang_review = search_coupang(title)

    total_review = naver_review +  gmarket_review+  auction_review+ coupang_review
    if total_review!=0:
        total_score = round(((naver_score * naver_review + gmarket_score * gmarket_review + auction_score * auction_review + coupang_score * coupang_review) / total_review),2)

    mysql_conr = None
    mysql_con = mysql.connector.connect(host='localhost', port='3306', database='final', user='root', password='1234')
    mysql_cursor = mysql_con.cursor(dictionary=True)

    sql_bar = "SELECT * FROM final WHERE name = %s"
    mysql_cursor.execute(sql_bar, (name, ))
    mysql_bar = mysql_cursor.fetchall()[0]
    mysql_cursor = mysql_con.cursor(dictionary=True)

    real_name = mysql_bar['real_name']
    barcode = mysql_bar['barcode']
    img_url = mysql_bar['img_url']
    what = mysql_bar['what']


    sql = "INSERT IGNORE INTO pro_final (total_score, total_review, real_name, name , barcode , url, what , naver_url, naver_total, naver_review, coupang_url, coupang_total, coupang_review, auction_url, auction_total, auction_review, gmarket_url, gmarket_total, gmarket_review) VALUES (%s ,%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    var = (total_score, total_review,real_name, name, barcode, img_url, what, naver_link, naver_score,naver_review,coupang_link,coupang_score,coupang_review,auction_link,auction_score,auction_review,gmarket_link,gmarket_score,gmarket_review)
    mysql_cursor.execute(sql, var)
    mysql_con.commit()

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
        "total_review" : total_review
    }

    return JsonResponse(d, safe=False, json_dumps_params={'ensure_ascii': False})

