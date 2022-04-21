# coding: utf-8

from bs4 import BeautifulSoup
import requests
import csv
import time
import datetime
import json
import glob
import os



#-------------------------------------------------------------
# Get constants
#-------------------------------------------------------------

def get_content_folder():
  dir_data = "./data/"
  return dir_data


def get_latest_kaiji():
  r = requests.get(get_kaiji_url(""))
  html = BeautifulSoup(r.text, "html.parser")
  title = html.find("title").text  # ex. "第208回国会　議案の一覧"

  title = title.replace("第", "")
  title = title.replace("回国会　議案の一覧", "")

  return title



#-------------------------------------------------------------
# Versatile functions
#-------------------------------------------------------------

# Get Kaiji URL
def get_kaiji_url(kaiji):
  prefix = "https://www.shugiin.go.jp/internet/itdb_gian.nsf/html/gian/"
  if kaiji == "":
    return prefix + "menu.htm"
  else:
    return prefix + "kaiji" + kaiji + ".htm"



# Get CSV file content as array
# Return False if the file does NOT exist
def get_csv(url):
  try:
    with open(url) as csvfile:
      read = csv.reader(csvfile, delimiter = ',')
      rows = list(read)
      return rows
  except FileNotFoundError:
    return False


# Save CSV or JSON file
def save_file(url, values):
  ext = url.split(".")[-1]

  if ext == "csv":
    with open(url, 'w', newline = '') as f:
      writer = csv.writer(f)
      writer.writerows(values)

  if ext == "json":
    with open(url, 'w') as f:
      json.dump(values, f, ensure_ascii = False)


#-------------------------------------------------------------
# Update data
#-------------------------------------------------------------

def parse_kaiji(kaiji):

  def parse_kaiji_main(kaiji):

    def get_td_value(tds, i, ttype):
      ret = ""

      if (len(tds) >= i + 1):
        if (ttype == "text"):
          ret = tds[i].text
        if (ttype == "href"):
          if (tds[i].find("a") != None):
            ret = tds[i].find("a")["href"]
            ret = ret.replace("./", "https://www.shugiin.go.jp/internet/itdb_gian.nsf/html/gian/")

      # Clean if the value consists of only spaces
      substitutions = ["　　", "　"]
      for sub in substitutions:
        if ret == sub:
          ret = ""
      
      return ret


    result = [[
      "掲載回次",
      "キャプション",
      "種類",
      "提出回次",
      "番号",
      "議案件名",
      "審議状況",
      "経過情報",
      "経過情報URL",
      "本文情報",
      "本文情報URL",
      "議案種類",
      "議案提出回次",
      "議案番号",
      "議案件名",
      "議案提出者",
      "衆議院予備審査議案受理年月日",
      "衆議院予備付託年月日／衆議院予備付託委員会",
      "衆議院議案受理年月日",
      "衆議院付託年月日／衆議院付託委員会",
      "衆議院審査終了年月日／衆議院審査結果",
      "衆議院審議終了年月日／衆議院審議結果",
      "衆議院審議時会派態度",
      "衆議院審議時賛成会派",
      "衆議院審議時反対会派",
      "参議院予備審査議案受理年月日",
      "参議院予備付託年月日／参議院予備付託委員会",
      "参議院議案受理年月日",
      "参議院付託年月日／参議院付託委員会",
      "参議院審査終了年月日／参議院審査結果",
      "参議院審議終了年月日／参議院審議結果",
      "公布年月日／法律番号"
    ]]

    r = requests.get(get_kaiji_url(kaiji))
    html = BeautifulSoup(r.text, "html.parser")
    tables = html.find_all('table')

    for table in tables:
      trs = table.find_all('tr')
      caption = table.find("caption").text

      for tr in trs:
        tds = tr.find_all('td')

        if len(tds) >= 1:
          row = [""] * 32

          row[0] = kaiji
          row[1] = caption
          row[2] = ""
          row[3] = get_td_value(tds, 0, "text")
          row[4] = get_td_value(tds, 1, "text")
          row[5] = get_td_value(tds, 2, "text")
          row[6] = get_td_value(tds, 3, "text")
          row[7] = get_td_value(tds, 4, "text")
          row[8] = get_td_value(tds, 4, "href")
          row[9] = get_td_value(tds, 5, "text")
          row[10] = get_td_value(tds, 5, "href")

          if caption == "予算の一覧":
            row[9] = ""
            row[10] = ""

          if caption == "承諾の一覧":
            row[4] = ""
            row[5] = get_td_value(tds, 1, "text")
            row[6] = get_td_value(tds, 2, "text")
            row[7] = get_td_value(tds, 3, "text")
            row[8] = get_td_value(tds, 3, "href")
            row[9] = ""
            row[10] = ""

          if caption == "決算その他":
            row[2] = get_td_value(tds, 0, "text")
            row[3] = get_td_value(tds, 1, "text")
            row[4] = ""
            row[5] = get_td_value(tds, 2, "text")
            row[6] = get_td_value(tds, 3, "text")
            row[7] = get_td_value(tds, 4, "text")
            row[8] = get_td_value(tds, 4, "href")
            row[9] = ""
            row[10] = ""

          result.append(row)

    return result


  def parse_keika_all(kaiji, result):

    def parse_keika(row):
      time.sleep(1)
      url = row[8]
      r = requests.get(url)
      html = BeautifulSoup(r.text, "html.parser")

      tds = html.find_all("td")
      komokus = []
      naiyos = []

      for td in tds:
        if (td["headers"][0] == "KOMOKU"):
          komokus.append(td.text)

        if (td["headers"][0] == "NAIYO"):
          naiyos.append(td.text)

      for i, komoku in enumerate(komokus):
        naiyo = naiyos[i]
        naiyo = naiyo.replace("\r", "");
        naiyo = naiyo.replace("\n", "");

        header_index = result[0].index(komoku)
        row[header_index] = naiyo

    for row in result:
      if (row[8][0:8] == "https://"):
        parse_keika(row)

    return result

  result = parse_kaiji_main(kaiji)
  result = parse_keika_all(kaiji, result)

  # Get existing kaiji CSV
  gian_all_raw = get_csv(DIR_DATA + "gian_all.csv")

  # Delete existing kaiji row
  gian_all = []
  for kaiji_row in gian_all_raw:
    if kaiji_row[0] != kaiji:
      gian_all.append(kaiji_row)

  # Get index of kaiji
  index = len(gian_all)
  for i, kaiji_row in enumerate(gian_all):
    if i == 0:
      continue
    if int(kaiji_row[0]) > int(kaiji):
      index = i
      break

  # Insert into gian_all
  for row in result[1:]:
    gian_all.insert(index, row)
    index += 1

  save_file(DIR_DATA + "gian_all.csv", gian_all)
  save_file(DIR_DATA + "gian_all.json", gian_all)



def update_time():
  dt_now = datetime.datetime.now()
  dt_str = dt_now.strftime('%Y-%m-%d %H:%M:%S')

  latest = {
      'file_update': dt_str
  }

  save_file(DIR_DATA + "updatetime.json", latest)



#-------------------------------------------------------------
# Main
#-------------------------------------------------------------

DIR_DATA = get_content_folder()

parse_kaiji(get_latest_kaiji())
update_time()
