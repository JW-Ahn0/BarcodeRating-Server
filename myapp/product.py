# -*- coding: utf-8 -*-
import requests as rq
from django.http import JsonResponse
from bs4 import BeautifulSoup as bf

#dd

def return_name(barcode):
    koreanet = "http://www.koreannet.or.kr/home/hpisSrchGtin.gs1?gtin=" #코리안넷 주소
    koreanet += str(barcode)
    req = rq.get(koreanet) #http로 html 가져옴
    raw = req.text
    html = bf(raw, 'html.parser')  # string을 html 양식으로 parsing
    try:
        info_name = html.select('div.productTit')
        info_image = html.select('div.imgArea')  # &amp; 걸러주는 작업해야됨 이미지쪽임1
    except Exception as e:
        print(e)
        return "코리안넷에 등록된 상품이 아닙니다.","null"
    info_str = ""
    for x in info_name:
        info_str += str(x)

    info_img =""
    for x in info_image[0].select('img')[0]['src']:
        info_img += str(x)

    info_str = info_str[50:-13] # 이름만 가져오기 위해. 16번째 문자부터 끝까지 가져옴.
    return info_str,info_img

def search_naver(name, sortFlag):

    if name =="코리안넷에 등록된 상품이 아닙니다.":
        return "코리안넷에 등록된 상품이 아닙니다."
    print("입력된값:"+name)
    naver_shopping = "https://search.shopping.naver.com/search/all?query="
    naver_shopping +=name
    sort = "&sort=review&timestamp=&viewType=list"
    
    if sortFlag ==1:
        naver_shopping += sort
    req = rq.get(naver_shopping)
    raw = req.text
    html = bf(raw, 'html.parser')
    count = 0
    score = 0.0
    review = 0
    try:
        List = html.find_all('div',class_ ='basicList_info_area__17Xyo')
        for item in List:
            if item.find('span',class_ = 'basicList_graph__ZV6s9') is not None:
                score = float(item.find('span',class_ = 'basicList_graph__ZV6s9').text[3:])
                print(score)
                review = int(item.find('a',class_='basicList_etc__2uAYO').find('em', class_='basicList_num__1yXM9').text.replace(",",""))
                print(review)
            else:
                count += 1
    except Exception as e:
        print(e)
        return naver_shopping,score,review


    if count ==List.__len__() and sortFlag != 1:
        return search_naver(name,1)

    return naver_shopping,score,review

def hello_world():
		d = { "title" : "입력된값:홈스타 강력세정 욕실용 900ml",
					"img_Url" : "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fbhl9kC%2FbtqC3NJwQ04%2F0kyUm1mZ75YcqksFTwTaOK%2Fimg.png",
						"total" : "177.777777",
							"mall_List" : [
							{"name" : "naver",
							"score" : 4.8,
							"review" : "1,887",
							"link" : "https://search.shopping.naver.com/search/all?query=%ED%99%88%EC%8A%A4%ED%83%80%20%EA%B0%95%EB%A0%A5%EC%84%B8%EC%A0%95%20%EC%9A%95%EC%8B%A4%EC%9A%A9%20900ml&frm=NVSHATC&prevQuery=%ED%99%88%EC%8A%A4%ED%83%80%20%EA%B0%95%EB%A0%A5%EC%84%B8%EC%A0%95%20%EC%9A%95%EC%8B%A4%EC%9A%A9%20900ml&sort=review&timestamp=&viewType=list" } ],
		}
		return JsonResponse(d)

def product(requests, Barcode):
    if Barcode is not None:
          title, imgUrl = return_name(str(Barcode))
          link , score , review = search_naver(title, 0)
          total = review * score
          d = {
                  "img_Url":imgUrl,
                  "mall_List" : [
                  {
                      "link":link,
                      "name":"naver",
                      "review":review,
                      "score":score
                  }
                  ],
                  "title":title,
                  "total":total
          }
          return JsonResponse(d, safe=False, json_dumps_params={'ensure_ascii': False})
    else :
          return "항목이 존재하지 않습니다."


