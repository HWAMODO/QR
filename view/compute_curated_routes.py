# compute_curated_routes.py
import pandas as pd
from itertools import permutations

# 순찰 경로 데이터 로딩
df = pd.read_csv("C:/Users/USER/Desktop/국민대과제/data/조별_순찰지_경로지정.csv")

routes = []

for group in df['조'].unique():
    group_points = df[df['조'] == group].reset_index(drop=True)

    # 출발지와 도착지 고정
    start = group_points.iloc[0]
    end = group_points.iloc[-1]
    mid_points = group_points.iloc[1:-1]  # 중간 순찰지

    best_order = None
    best_dist = float('inf')

    mid_perms = permutations(mid_points.index.tolist())

    for perm in mid_perms:
        ordered = pd.concat([
            pd.DataFrame([start]),
            mid_points.loc[list(perm)],
            pd.DataFrame([end])
        ])

        coords = ordered[['위도', '경도']].values
        total_dist = sum(
            ((coords[i][0] - coords[i+1][0])**2 + (coords[i][1] - coords[i+1][1])**2)**0.5
            for i in range(len(coords)-1)
        )

        if total_dist < best_dist:
            best_dist = total_dist
            best_order = ordered.copy()

    best_order['순번'] = range(len(best_order))
    routes.append(best_order)

pd.concat(routes).to_csv("C:/Users/USER/Desktop/국민대과제/data/최적_조별_순찰경로.csv", index=False, encoding="utf-8-sig")
print("✅ 최적 경로 계산 완료: 최적_조별_순찰경로.csv")
