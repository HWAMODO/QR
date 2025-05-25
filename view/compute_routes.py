# compute_routes.py
import pandas as pd
from itertools import permutations
from geopy.distance import geodesic

# 입력 및 출력 경로 정의
input_path = r"C:/Users/USER/Desktop/국민대과제/data/조별_순찰지_자동생성.csv"
output_path = r"C:/Users/USER/Desktop/국민대과제/data/최적순찰경로.csv"

# 데이터 불러오기
df = pd.read_csv(input_path)
df = df[df['순번'] != 99]  # 복귀용 더미 제거

# 결과 저장용 리스트
final = []

# 거리 계산 함수
def calc_distance(p1, p2):
    return geodesic(p1, p2).meters

# 조별로 최적 경로 계산
for group, sub in df.groupby('조'):
    sub = sub.sort_values('순번')
    start = sub[sub['순번'] == 0].iloc[0]  # 출발지
    places = sub[sub['순번'] > 0]  # 방문 순찰지들

    coords = places[['위도', '경도']].values
    best_order = []
    min_total = float('inf')

    for perm in permutations(range(len(coords))):
        total = 0
        current = (start['위도'], start['경도'])

        for i in perm:
            next_p = (coords[i][0], coords[i][1])
            total += calc_distance(current, next_p)
            current = next_p

        total += calc_distance(current, (start['위도'], start['경도']))  # 복귀

        if total < min_total:
            min_total = total
            best_order = perm

    ordered = places.iloc[list(best_order)].copy()
    ordered.insert(0, '순서', range(1, len(ordered) + 1))
    start_row = pd.DataFrame([[0, *start.values]], columns=['순서'] + list(start.index))
    end_row = pd.DataFrame([[len(ordered)+1, *start.values]], columns=['순서'] + list(start.index))

    final.append(pd.concat([start_row, ordered, end_row]))

# 최종 결과 저장
final_df = pd.concat(final)
final_df = final_df.sort_values(['조', '순서'])
final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"✅ 최적 순찰 경로 저장 완료 → {output_path}")
