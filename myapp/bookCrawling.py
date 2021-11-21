from bs4 import BeautifulSoup
from django.http import JsonResponse
import urllib.request
import mysql.connector


def bookCrawling(url):

    kb_url = 'https://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&barcode='+str(url)
    yes_url = 'http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=ALL&qdomain=%C0%FC%C3%BC&Wcode=001_005&query='+str(url)
    #검색후 상세페이지
    kb_webpage = urllib.request.urlopen(kb_url)
    yes_webpage = urllib.request.urlopen(yes_url)

    kb_soup = BeautifulSoup(kb_webpage, 'html.parser')
    yes_soup = BeautifulSoup(yes_webpage, 'html.parser')

    #교보에서 제목뽑기
    titlesoup = kb_soup.find('h1', "title")

    if titlesoup is None :
        return "no"
    title = titlesoup.find('strong')

    #교보에서 img뽑기
    imagesoup = kb_soup.find('div', "box_detail_cover")
    image = imagesoup.find('img')
    imurl = str(image).split('src="')
    finalimage = imurl[1].split('"')

    #교보별점
    kb_star = kb_soup.find('div', "popup_load").find('em')
    if kb_star is None:
        kb_star = 0
        kb_star_num = 0
    else :
        kb_star = (float)(kb_star.get_text())
        kb_star_num = (int)(str(kb_soup.find('div', "popup_load").get_text()).split('(리뷰 ')[1].split('개')[0].replace(',', ""))

    #yes24별점
    yes_star = yes_soup.find('div', "info_row info_rating")

    if yes_star is None:
        yes_star = 0
        yes_star_num = 0
    else :
        yes_star = (float)(yes_star.find('em', "yes_b").get_text())
        yes_star_num = (int)(yes_soup.find('div', "info_row info_rating").find('em', "txC_blue").get_text().replace(',',""))

    total_review = kb_star_num+yes_star_num
    if total_review == 0:
        total_score = 0
    else :
        total_score = round((kb_star_num*kb_star + yes_star_num*yes_star) / total_review , 2)

    mysql_conr = None
    mysql_con = mysql.connector.connect(host='localhost', port='3306', database='final', user='root', password='1234')
    mysql_cursor = mysql_con.cursor(dictionary=True)

    title = title.get_text().replace('\n','').replace('\r','').replace('\t','')

    sql = "INSERT IGNORE INTO final (real_name, name, barcode, img_url, what) VALUES (%s,%s,%s,%s,%s)"
    var = (title, title, url, finalimage[0], 'book')
    mysql_cursor.execute(sql, var)

    sql = "INSERT IGNORE INTO book_final (barcode, name, url,total_score, total_review, kb_url, yes_url, kb_total, yes_total, kb_review, yes_review) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    var = (url, title, finalimage[0],total_score,total_review, kb_url, yes_url, kb_star, yes_star, kb_star_num, yes_star_num)
    mysql_cursor.execute(sql, var)

    mysql_con.commit()
    mysql_con.close()

    #기본 json
    d = [{
        "type": 'book',
        "img_Url": finalimage[0],
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

    return d