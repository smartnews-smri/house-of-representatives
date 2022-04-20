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


def get_static_file(file):
  open_file = open(DIR_DATA + file + '.json', 'r')
  json_data = json.load(open_file)
  #print(json_data)

  # Reverse id and value
  result = {}
  for key in json_data:
    value = json_data[key]
    result[value] = key
  
  return result


def get_latest_kaiji():
  files = glob.glob(DIR_DATA_KAIJI + "*")
  latest = 142

  for ffile in files:
    prefix = DIR_DATA_KAIJI + "kaiji"
    suffix = ".csv"

    if prefix in ffile and suffix in ffile:
      ffile = ffile.replace(prefix, "")
      ffile = ffile.replace(suffix, "")
      kaiji = int(ffile) 

      if latest < kaiji:
        latest = kaiji

  next = latest + 1
  r = requests.get(get_kaiji_url(str(next)))

  if r.status_code != 200:
    next = ""

  return {
      "latest": str(latest),
      "next": str(next)
    }



#-------------------------------------------------------------
# Versatile functions
#-------------------------------------------------------------

# Get Kaiji URL
def get_kaiji_url(kaiji):
  return "https://www.shugiin.go.jp/internet/itdb_gian.nsf/html/gian/kaiji" + kaiji + ".htm"


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


# Create folder if NOT exists
def create_folder(url):
  exists = os.path.exists(url)
  if exists == False:
    os.mkdir(url)


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

def update_data(kaiji):

  def get_gian_type(caption, ttype):
    value = ""

    #print(caption, ttype, GIAN_TYPE)

    if (ttype != ""):
      value = ttype
    else:
      value = caption.replace("の一覧", "")

    if value == "":
      ret = ""
    else:
      ret = GIAN_TYPE[value]
    return ret


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


      r = requests.get(get_kaiji_url(kaiji))
      html = BeautifulSoup(r.text, "html.parser")

      # print(soup)

      tables = html.find_all('table')
      result = [[
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

      for table in tables:
        trs = table.find_all('tr')
        caption = table.find("caption").text

        #print("---table---")
        #print("caption: " + caption.text)

        for tr in trs:
          tds = tr.find_all('td')
          #print("---tr---")
          #ats = []

          if len(tds) >= 1:
            #print(tds)
            #print(ats)

            row = [""] * 31

            row[0] = caption
            row[1] = ""
            row[2] = get_td_value(tds, 0, "text")
            row[3] = get_td_value(tds, 1, "text")
            row[4] = get_td_value(tds, 2, "text")
            row[5] = get_td_value(tds, 3, "text")
            row[6] = get_td_value(tds, 4, "text")
            row[7] = get_td_value(tds, 4, "href")
            row[8] = get_td_value(tds, 5, "text")
            row[9] = get_td_value(tds, 5, "href")

            if caption == "予算の一覧":
              row[8] = ""
              row[9] = ""

            if caption == "承諾の一覧":
              row[3] = ""
              row[4] = get_td_value(tds, 1, "text")
              row[5] = get_td_value(tds, 2, "text")
              row[6] = get_td_value(tds, 3, "text")
              row[7] = get_td_value(tds, 3, "href")
              row[8] = ""
              row[9] = ""

            if caption == "決算その他":
              row[1] = get_td_value(tds, 0, "text")
              row[2] = get_td_value(tds, 1, "text")
              row[3] = ""
              row[4] = get_td_value(tds, 2, "text")
              row[5] = get_td_value(tds, 3, "text")
              row[6] = get_td_value(tds, 4, "text")
              row[7] = get_td_value(tds, 4, "href")
              row[8] = ""
              row[9] = ""

            #print(row)

            result.append(row)

      return result

    def parse_keika_all(kaiji, result):

      def parse_keika(row):
        #print("start parse_keika(" + row[7] + ")")
        time.sleep(1)
        url = row[7]
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
        if (row[7][0:8] == "https://"):
          parse_keika(row)

      return result

    result = parse_kaiji_main(kaiji)
    result = parse_keika_all(kaiji, result)
    
    save_file(DIR_DATA_KAIJI + "kaiji" + kaiji + ".csv", result)


  def update_gian_list(kaiji):

    def get_gian_status(value):
      if value == "":
        ret = ""
      else:
        ret = GIAN_STATUS[value]

      return ret


    def get_gian_file_header():
      return [[
        "審議回次",
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


    # Convert kaiji row into individual gian row
    def get_gian_file_row(krow):

      row = [
        kaiji,
        krow[0],
        krow[1],
        krow[2],
        krow[3],
        krow[4],
        krow[5],
        krow[6],
        krow[7],
        krow[8],
        krow[9],
        krow[10],
        krow[11],
        krow[12],
        krow[13],
        krow[14],
        krow[15],
        krow[16],
        krow[17],
        krow[18],
        krow[19],
        krow[20],
        krow[21],
        krow[22],
        krow[23],
        krow[24],
        krow[25],
        krow[26],
        krow[27],
        krow[28],
        krow[29],
        krow[30]
      ]

      return row


    rows_kaiji = get_csv(DIR_DATA_KAIJI + "kaiji" + kaiji + ".csv")
    rows_gian_list = get_csv(DIR_DATA + "gian_list.csv")

    for krow in rows_kaiji[1:]:

      target_index = -1

      for i, grow in enumerate(rows_gian_list):
        if i == 0:
          continue
        if get_gian_type(krow[0], krow[1]) == grow[0] and krow[2] == grow[1] and krow[3] == grow[2] and krow[4] == grow[3]:
          target_index = i

      # New row to add/update for gian_list
      gian_list_row = [
        get_gian_type(krow[0], krow[1]),
        krow[2],
        krow[3],
        krow[4],
        kaiji,
        get_gian_status(krow[5])
      ]

      # New row to add/update for individual gian
      gian_file_row = get_gian_file_row(krow)

      # When the Gian already exists in gian_list
      if target_index >= 0:
        rows_gian_list[target_index] = gian_list_row
        file_index = "g" + str(target_index).zfill(5) # ex. "g00001"

      # When the Gian does NOT exist in gian_list
      else:
        rows_gian_list.append(gian_list_row)
        file_index = "g" + str(len(rows_gian_list) - 1).zfill(5) # ex. "g00001"

      # Create DIR_DATA_GIAN + kaijiXXX folder if NOT exists
      dir_data_gian_kaiji = DIR_DATA_GIAN + "kaiji" + krow[2] + "/"
      create_folder(dir_data_gian_kaiji)

      # Update individual gian file
      rows_gian_file = get_csv(dir_data_gian_kaiji + file_index + ".csv")

      if rows_gian_file == False:
        rows_gian_file = get_gian_file_header()
      else:
        for j, frow in enumerate(rows_gian_file):
          if j == 0:
            continue
          if kaiji == frow[0] and krow[0] == frow[1] and krow[1] == frow[2] and krow[2] == frow[3] and krow[3] == frow[4] and krow[4] == frow[5]:
            rows_gian_file.pop(j)

      # Save individual gian file
      rows_gian_file.append(gian_file_row)
      save_file(dir_data_gian_kaiji + file_index + ".csv", rows_gian_file)
      save_file(dir_data_gian_kaiji + file_index + ".json", rows_gian_file)

    # Save gian list file
    save_file(DIR_DATA + "gian_list.csv", rows_gian_list)
    save_file(DIR_DATA + "gian_list.json", rows_gian_list)


  print("update_data(" + kaiji + ")")
  parse_kaiji(kaiji)
  update_gian_list(kaiji)


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
DIR_DATA_KAIJI = DIR_DATA + "kaiji/"
DIR_DATA_GIAN = DIR_DATA + "gian/"
GIAN_TYPE = get_static_file("gian_type")
GIAN_STATUS = get_static_file("gian_status")
LATEST = get_latest_kaiji()

#update_data(LATEST["latest"])

#if (LATEST["next"] != ""):
  #update_data(LATEST["next"])

update_time()


for i in range(142,209):
  update_data(str(i))
