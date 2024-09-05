# 아카라이브 도박 예측기
### 아카라이브 도박을 더 스마트하게

## 1. 소개
이 레포지토리는 아카라이브 도박 예측기 코드를 공유하고, 최적화를 통해 더욱 효율적인 예측 방법을 모색하기 위해 만들어졌습니다. 다양한 도박 예측 시나리오에서 활용할 수 있는 기본 코드와 사용 방법을 제공합니다.

## 2. 주요 기능
- **온도계**와 **나무게임**의 당첨 결과 데이터를 바탕으로 예측을 수행합니다.
- 간단한 설정을 통해 두 가지 게임에 대해 정확한 예측을 시도할 수 있습니다.

## 3. 서버 셋업
필요 패키지 설치:

```
pip install scikit-learn selenium numpy datetime
```

### 온도계 게임 실행:
```
cd thermo
python index.py
```

### 나무게임 실행:
```
cd tree
python index.py
```

> **Note:** Chrome 버전에 맞는 [ChromeDriver](https://sites.google.com/chromium.org/driver/)를 설치해야 합니다.

## 4. 라이선스
이 프로젝트는 [MIT 라이선스](./LICENSE)를 따릅니다.
