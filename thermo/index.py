import datetime
import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import codecs
import re

# 첫 실행시 생성
if os.path.isfile("./dataset.csv"):
    os.remove("./dataset.csv")

with codecs.open("./dataset.csv", "w", "utf-8-sig") as f:
    writer = csv.writer(f)


s = Service("./chromedriver")
opts = Options()
opts.add_argument("--headless")

driver = webdriver.Chrome(service=s, options=opts)

# 반복
driver.get("https://arca.live/b/thermometer")

previus = ''

def slice(data):

    # 값 자르기
    thermo_round = data.split(": ")[0]
    temp = data.split(": ")[1].split("°C")[0]
    temp_re = 100 - int(temp)

    print(thermo_round)
    print(temp)   
    print(temp_re) 

    result = thermo_round + "," + temp + "," + str(temp_re)

    with open('dataset.csv', "a", newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow([result])

    process(50)


# 1분마다 반복하기
def process(number):
    forward_get = []

    with open("dataset.csv", "r", encoding ="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = []
        for row in reader:
            rows.append(row[0])
        rows = rows[-number:] # 이거 추가함

    # 여러 줄의 값 가져오기
    for value in rows:
        temp = value.split(",")[1]
        forward_get.append(temp)

    print(forward_get)

    try:
        predict(forward_get, number) 
    except:
        pass

def predict(forward_get, number):
    # 머신러닝 모델 학습
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    import numpy as np
    from sklearn.exceptions import DataConversionWarning
    import warnings

    # 데이터 준비
    X = np.array(forward_get).astype(int)

    # 데이터 분할
    X_train, X_test, y_train, y_test = train_test_split(X[:-1].reshape(-1, 1), X[1:].reshape(-1, 1), test_size=0.2, random_state=42)

    # 모델 학습
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DataConversionWarning)
        model = RandomForestRegressor()
        model.fit(X_train, y_train.ravel())

    # 다음 숫자 예측
    next_number = min(100, max(0, round(model.predict([[int(forward_get[-1])]])[0])))
    #print(int(next_number))

    with open('final.txt', "w", newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow([next_number])

    # 예측 결과 확인
    try:
        int(next_number)
    except ValueError:
        print("다시 해보기")

count = 0

while True:
    value_elements = driver.find_elements(by=By.XPATH, value="/html/body/div[2]/div[3]/article/div[1]/div[1]/div/div/div[2]/div[2]/div[2]/div")
    detect_time = driver.find_elements(by=By.XPATH, value="/html/body/div[2]/div[3]/article/div[1]/div[1]/div/div/div[2]/div[1]")

    value = value_elements[0].text.split('\n')[0]

    detect_time = detect_time[0]

    if previus != value:
        slice(value)
        previus = value
        if count == 1000:
            driver.get("https://arca.live/b/thermometer")
            count = 0
        else:
            count += 1
    else:
        pass
    time.sleep(1)
