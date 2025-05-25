import pandas as pd
from geopy.distance import geodesic

# 파일 경로 정의
core_path = r"C:/Users/USER/Desktop/국민대과제/data/초등학교_좌표완성본.csv"
cand_school_path = r"C:/Users/USER/Desktop/국민대과제/data/학교_지오코딩완료.csv"
cand_green_path = r"C:/Users/USER/Desktop/국민대과제/data/녹지대_WGS84.csv"
output_path = r"C:/Users/USER/Desktop/국민대과제/data/조별_순찰지_자동생성.csv"

# 데이터 불러오기
df_core = pd.read_csv(core_path, encoding='cp949')
df_school = pd.read_csv(cand_school_path)
df_green = pd.read_csv(cand_green_path)

# 후보지 통합 (중고등학교 + 녹지대)
df_school = df_school[df_school['학교종류명'].isin(['중학교', '고등학교'])]
df_school = df_school.rename(columns={'학교명': '이름', '학교종류명': '종류'})
df_green['종류'] = '녹지대'
df_green = df_green.rename(columns={'녹지대명': '이름'})

df_candidates = pd.concat([df_school[['이름', '위도', '경도', '종류']], df_green[['이름', '위도', '경도', '종류']]], ignore_index=True)

# NaN 제거 + 숫자형 변환
df_candidates['위도'] = pd.to_numeric(df_candidates['위도'], errors='coerce')
df_candidates['경도'] = pd.to_numeric(df_candidates['경도'], errors='coerce')
df_candidates = df_candidates.dropna(subset=['위도', '경도'])

# 거리 계산 함수
def distance(p1, p2):
    return geodesic(p1, p2).meters

assigned = set()
results = []

total_distance_target = 1000

for _, core in df_core.iterrows():
    school_name = core['학교명']
    school_coord = (core['위도'], core['경도'])

    df_candidates['거리'] = df_candidates.apply(
        lambda x: distance(school_coord, (x['위도'], x['경도'])),
        axis=1
    )

    filtered = df_candidates[
        (df_candidates['거리'] <= 1000) & (~df_candidates['이름'].isin(assigned))
    ]

    best_subset = []
    best_total = 99999

    for size in [4, 3, 2]:
        subset = filtered.nsmallest(size, '거리')
        total = subset['거리'].sum()
        if abs(total - total_distance_target) < abs(best_total - total_distance_target):
            best_subset = subset
            best_total = total

    for i, (_, row) in enumerate(best_subset.iterrows(), 1):
        results.append({
            "조": school_name,
            "순번": i,
            "장소": row['이름'],
            "종류": row['종류'],
            "위도": row['위도'],
            "경도": row['경도'],
            "거리": row['거리']
        })
        assigned.add(row['이름'])

    # 출발/복귀지
    results.append({
        "조": school_name, "순번": 0, "장소": school_name,
        "종류": "초등학교", "위도": school_coord[0], "경도": school_coord[1], "거리": 0
    })
    results.append({
        "조": school_name, "순번": 99, "장소": school_name,
        "종류": "초등학교", "위도": school_coord[0], "경도": school_coord[1], "거리": 0
    })

# 저장
final_df = pd.DataFrame(results).sort_values(['조', '순번'])
final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"✅ 순찰지 자동 생성 완료 → 저장 경로: {output_path}")
