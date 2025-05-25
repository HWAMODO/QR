# generate_curated_patrol_points.py
import pandas as pd

# 중심 초등학교와 각 조별 순찰지 구성 (순서 명시)
# 좌표는 기존에 제공한 CSV에서 가져올 예정
core_assignments = {
    "서울일원초등학교": ["중동중학교", "밀알학교"],
    "서울양전초등학교": ["개포동근린공원", "개원중학교"],
    "서울개포초등학교": ["개포동근린공원"],
    "서울대진초등학교": ["대진공원", "마루공원"],
    "서울영희초등학교": ["중동고등학교"],
    "서울대청초등학교": ["일원에코파크"],
    "서울대모초등학교": ["서울로봇고등학교"]
}

# 중심 초등학교 좌표 로딩
df_core = pd.read_csv("C:/Users/USER/Desktop/국민대과제/data/초등학교_좌표완성본.csv")
# 사용자 순찰지 좌표 로딩
df_patrol = pd.read_csv("C:/Users/USER/Desktop/국민대과제/data/순찰지_지오코딩.csv")

rows = []

for school, patrols in core_assignments.items():
    # 중심 초등학교 정보
    core_row = df_core[df_core['학교명'] == school].iloc[0]
    rows.append({"조": school, "순번": 0, "장소": school, "위도": core_row['위도'], "경도": core_row['경도']})

    # 지정된 순찰지 추가
    for i, place in enumerate(patrols, start=1):
        patrol_row = df_patrol[df_patrol['장소'] == place].iloc[0]
        rows.append({"조": school, "순번": i, "장소": place, "위도": patrol_row['위도'], "경도": patrol_row['경도']})

    # 복귀 지점 (중심학교 다시 추가)
    rows.append({"조": school, "순번": len(patrols)+1, "장소": school, "위도": core_row['위도'], "경도": core_row['경도']})

# 데이터프레임으로 저장
result_df = pd.DataFrame(rows)
result_df.to_csv("C:/Users/USER/Desktop/국민대과제/data/조별_순찰지_경로지정.csv", index=False, encoding="utf-8-sig")
print("✅ 조별 순찰지 경로지정 CSV 저장 완료: 조별_순찰지_경로지정.csv")

