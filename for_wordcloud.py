import pandas as pd
from konlpy.tag import Komoran
from wordcloud import WordCloud
from collections import Counter

file_path = "./data_from_s3/20231006.csv"
data = pd.read_csv(file_path)

komoran = Komoran()

# "name" 컬럼에서 명사 추출
noun_list = []
for text in data['name']:
    nouns = komoran.nouns(text)
    noun_list.extend(nouns)

# 가장 많이 나온 명사부터 40개 저장
counts = Counter(noun_list)
tags = counts.most_common(40)

# WordCloud 생성
wc = WordCloud(font_path="[YOUR_FONT_PATH]", background_color="white", max_font_size=60)
cloud = wc.generate_from_frequencies(dict(tags))

# WordCloud를 파일로 저장
cloud.to_file('test.jpg')

