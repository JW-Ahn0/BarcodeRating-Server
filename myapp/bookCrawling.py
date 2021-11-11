
from bs4 import BeautifulSoup
from django.http import JsonResponse
import urllib.request
#-*-coding:utf-8 -*-


def bookCrawling(request, url):
    #url = 9791162540640

    #검색후 상세페이지
    kb_webpage = urllib.request.urlopen('https://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&barcode='+str(url))
    yes_webpage = urllib.request.urlopen('http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=ALL&qdomain=%C0%FC%C3%BC&Wcode=001_005&query='+str(url))

    kb_soup = BeautifulSoup(kb_webpage, 'html.parser')
    yes_soup = BeautifulSoup(yes_webpage, 'html.parser')

    #교보에서 제목뽑기
    titlesoup = kb_soup.find('h1', "title")
    title = titlesoup.find('strong')

    #교보에서 img뽑기
    imagesoup = kb_soup.find('div', "box_detail_cover")
    image = imagesoup.find('img')
    imurl = str(image).split('src="')
    finalimage = imurl[1].split('"')

    #교보별점
    kb_star = (float)(kb_soup.find('div', "popup_load").find('em').get_text())

    #교보리뷰수
    kb_star_num = (int)(str(kb_soup.find('div',"popup_load").get_text()).split('(리뷰 ')[1].split('개')[0])

    #yes24별점
    yes_star = (float)(yes_soup.find('div', "info_row info_rating").find('em', "yes_b").get_text())
    #yes24리뷰수
    yes_star_num = (int)(yes_soup.find('div', "info_row info_rating").find('em', "txC_blue").get_text())

    #기본 json
    data = {}
    data['book'] = []
    data['book'].append({
        "title": title.get_text(),
        "img_url": finalimage[0],
        "total" : str((kb_star_num*kb_star + yes_star_num*yes_star) / (kb_star_num+yes_star_num)),
        "kb" : [str(kb_star), str(kb_star_num)],
        "yes": [str(yes_star), str(yes_star_num)]
    })
    return JsonResponse(data)