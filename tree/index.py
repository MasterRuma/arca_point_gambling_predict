from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import codecs
import csv
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.exceptions import DataConversionWarning
import warnings

database = {
        "part" : "",
        "slot" : "",
        "range" : "",
        "OOE" : "",
        "LOR" : "",
        "part1" : 0,
        "part2" : 0,
        "part3" : 0,
        "part4" : 0,
        "part5" : 0,
        "part6" : 0,
        "FL" : 0,
        "FR" : 0,
        "RO" : 0,
        "RE" : 0,
        "SL" : 0,
        "SR" : 0
    }

percent = {
    "part1" : 0,
    "part2" : 0,
    "part3" : 0,
    "part4" : 0,
    "part5" : 0,
    "part6" : 0,
    "FL" : 0,
    "FR" : 0,
    "RO" : 0,
    "RE" : 0,
    "SL" : 0,
    "SR" : 0
    }

s = Service("./chromedriver")

opts = Options()

opts.add_argument("--headless")

driver = webdriver.Chrome(service=s, options=opts)

driver.get("https://arca.live/b/namugame")

def divide(data):
    round = data.split(" 결과 : ")[0]
    number = data.split(" 결과 : ")[1].split("(")[0]
    army = data.split(",")[0].split("(")[1]
    OOE = data.split(",")[1]
    direction = data.split(",")[2].split(")")[0]

    result = round + "," + number + "," + army + "," + OOE + "," + direction

    with open('dataset.csv', "a", newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow([result])

    process(10)

def process(number):
    forward_get_number = []
    forward_get_direction = []

    with open("dataset.csv", "r", encoding ="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = []
        for row in reader:
            rows.append(row[0])
        rows = rows[-number:] # 이거 추가함

    # 여러 줄의 값 가져오기
    for value in rows:
        temp = value.split(",")[1].split("번 슬롯")[0]
        temp = int(temp)
        forward_get_number.append(temp)

    for value in rows:
        temp = value.split(",")[4]
        if temp == "좌":
            forward_get_direction.append(1)
        elif temp == "우":
            forward_get_direction.append(2)

    print(forward_get_number)
    print(forward_get_direction)

    try:
        n = predict_number(forward_get_number, number)
        d = predict_direction(forward_get_direction, number)

        if d == 1:
            d = "좌"
        elif d == 2:
            d = "우"
        
        with open('final.txt', "w", newline='', encoding='utf-8-sig') as f:
            f.write(f'{n} | {d}')
    except:
        pass

def predict_number(forward_get_number, number):

    # 데이터 준비
    X = np.array(forward_get_number).astype(int)

    # 데이터 분할
    X_train, X_test, y_train, y_test = train_test_split(X[:-1].reshape(-1, 1), X[1:].reshape(-1, 1), test_size=0.2, random_state=42)

    # 모델 학습
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DataConversionWarning)
        model = RandomForestRegressor()
        model.fit(X_train, y_train.ravel())

    # 다음 숫자 예측
    predicted_value = model.predict([[int(forward_get_number[-1])]])[0]
    next_number = min(6, max(1, round(predicted_value)))
    #print(int(next_number))

    # 예측 결과 확인
    try:
        int(next_number)
    except ValueError:
        print("다시 해보기")

    return next_number

def predict_direction(forward_get_direction, number):
    # 데이터 준비
    X = np.array(forward_get_direction).astype(int)

    # 데이터 분할
    X_train, X_test, y_train, y_test = train_test_split(X[:-1].reshape(-1, 1), X[1:].reshape(-1, 1), test_size=0.2, random_state=42)

    # 모델 학습
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DataConversionWarning)
        model = RandomForestRegressor()
        model.fit(X_train, y_train.ravel())

    # 다음 숫자 예측
    predicted_value = model.predict([[int(forward_get_direction[-1])]])[0]
    next_number = min(2, max(1, round(predicted_value)))
    #print(int(next_number))

    with open('final_direction' + str(number) + '.csv', "a", newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow([next_number])

    # 예측 결과 확인
    try:
        int(next_number)
    except ValueError:
        print("다시 해보기")

    return next_number
    
previus = ""

count = 0

while True:
    
    data = driver.find_element(By.XPATH, '//*[@id="result-message"]').get_attribute("innerHTML")

    if data != previus and data != "arca.live":
        divide(data)
        if count == 1000:
            driver.get("https://arca.live/b/namugame")
            count = 0
        else:
            count += 1

        with open("recent.txt", "w", encoding="utf-8-sig") as f:
            f.write(data)

        previus = data
    else:
        pass
    
    time.sleep(1)
