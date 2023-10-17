from wordcloud import WordCloud
from collections import Counter
import pandas as pd
from konlpy.tag import Komoran

# 데이터 불러오기
file_path = "./data_from_s3/20231006.csv"

data = pd.read_csv(file_path)

# 형태소 분석기(Komoran) 초기화
komoran = Komoran()

# "name" 컬럼에서 명사 추출
noun_list = []
for text in data['name']:
    nouns = komoran.nouns(text)
    noun_list.extend(nouns)

# 가장 많이 나온 명사부터 40개 저장
counts = Counter(noun_list)

# 특정 단어를 제외할 목록 작성
exclude_words = ["청정", "비비고", "기획", "오리온", "동원", "양반", "백설", "원", "롯데", "서울", "입", "바", "반", "풀무원", "오뚜기",
                 "농심", "해찬들", "종가", "멀티", "맛", "죽", "번들", "짜", "소", "식자", "풀", "국산", "식", "더", "한", "미", "집",
                 "해", "오", "드", "샘", "해태", "순창", "용기", "대림", "옛날", "표", "컵"]


# exclude_words 목록에 있는 단어를 제외
for word in exclude_words:
    if word in counts:
        del counts[word]

# 가장 많이 나온 명사 중에서 100개 선택
tags = counts.most_common(100)

# macOS 기본 폰트 설정 (Apple SD Gothic Neo)
font_path = "/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc"

# WordCloud 생성
wc = WordCloud(font_path=font_path, background_color="white", max_font_size=60)
cloud = wc.generate_from_frequencies(dict(tags))

# WordCloud를 파일로 저장
cloud.to_file('test.jpg')