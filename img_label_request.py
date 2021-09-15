__author__ = 'Qian Yang'
# -*- coding:utf-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup

global fi
global imgi
fi=0
imgi=0
def get_one_page(url):
  response= requests.get(url)
  if response.status_code == 200:
    return response.content.decode("utf8","ignore").encode("utf8","ignore")

def write_label(filename,type,contents):
    fo = open("./label/"+filename+".txt", "a")
    label=""
    if(type==1):
      label="性別："
    if(type==2):
      label="年齢層："
    if(type==3):
      label="種族："
    if(type==4):
      label="属性："
    
    for content in contents:
      fo.write(label+content+"\n")

    fo.close()

#采用BeautifulSoup解析
def bs4_paraser(html):
  all_value = []
  value = {}
  soup = BeautifulSoup(html,'html.parser')
  #print(soup)
  fo = open("test.txt", "w")
  fo.write( str(soup) )
  fo.close()
  all_div_item = soup.find_all('img', attrs={'class': 'card-img-top'})
  print(len(all_div_item))
  
  for img_url in all_div_item:

    img_url=str(img_url)
    pattern_r = re.compile('src="(.+)"/>')
    img_url = 'https://www.vrcw.net/'+ str(re.findall(pattern_r,img_url)[0])
    global imgi
    url = "./img/" + str(imgi) + ".jpg"
    r = requests.get(img_url)
    with open(url, 'wb') as f:#下载图片
        f.write(r.content)
        time.sleep(0.1)#下载间隔时间
        print("下载完%d张了..."%(imgi+1))
        imgi=imgi+1


  all_title_item = soup.find_all('h3', attrs={'class': 'card-title'})
  print(len(all_title_item))
  
  all_card_item = soup.find_all('div', attrs={'class': 'card-text'})
  print(len(all_card_item))
  #print(all_card_item)
  #input()

  
  for card in all_card_item :
    card_str=str(card)
    print(card_str)

    pattern_r = re.compile('性別：(.+)</a>')
    target_string1 = re.findall(pattern_r,card_str)
    #print("???",target_string1)
    #input("#"*50)
    pattern_r = re.compile("年齢層：(.+)</a>")
    target_string2 = re.findall(pattern_r,card_str)
    pattern_r = re.compile("種族：(.+)</a>")
    target_string3 = re.findall(pattern_r,card_str)
    pattern_r = re.compile("属性：(.+)</a>")
    target_string4 = re.findall(pattern_r,card_str)

    #filename=str(all_title_item[i])
    global fi
    filename=str(fi)
    write_label(filename,1,target_string1)
    write_label(filename,2,target_string2)
    write_label(filename,3,target_string3)
    write_label(filename,4,target_string4)
    fi=fi+1
    #input("write content to "+filename)
  #all_div_item = soup.find_all('div', attrs={'class': 'movie-item-info'})
  """for r in all_div_item:
    # 获取电影的名称和url
    title = r.find_all(name="p",attrs={"class":"name"})[0].string
    movie_url = r.find_all('p', attrs={'class': 'name'})[0].a['href']
    value['title'] = title
    value['movie_url'] = movie_url
    all_value.append(value)
    value = {}"""
  return all_value
 
def main():
  url1 = 'https://www.vrcw.net/product/type/avatar?page='
  pagenum=1
  while(pagenum < 72):
    url= url1+ str(pagenum)

    html = get_one_page(url)
    all_value = bs4_paraser(html)
    #print(all_value)
    pagenum = pagenum+1
    
  


if __name__ == '__main__':
  main()
