import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="練習 15｜站點地圖", layout="wide")
st.title("練習 15｜共享單車站點分佈地圖")
st.caption("資料來源：parking_lots.csv（共享單車歷史與型態站點資料）")

# 🔥 步驟 1：請在這裡貼上你剛剛「複製路徑」得到的絕對路徑
# 舉例：df = pd.read_csv(r"C:\Users\User\Desktop\bike\parking_lots.csv.csv")
df = pd.read_csv("./parking_lots.csv")

# 自動清理一下欄位名稱，防止前後有空格隱形字
df.columns = df.columns.str.strip()

df["parking_lot_id"] = df["parking_lot_id"].astype(str)
st.metric("總站點數", f"{len(df):,} 站")

# ── 步驟 2：選擇地圖顏色維度 ─────────────────────────────────
color_by = st.radio(
    "顏色依據",
    ["縣市（parking_lot_city）", "營運/商圈型態（parking_lot_biz_type_desc）"],
    horizontal=True,
)

if "縣市" in color_by:
    color_col = "parking_lot_city"
else:
    color_col = "parking_lot_biz_type_desc"

col1, col2 = st.columns([1, 2])
with col1:
    st.write("### 📋 站點資訊清單 (前 20 筆)")
    st.dataframe(
        df[
            [
                "parking_lot_name",
                "parking_lot_city",
                "parking_lot_area",
                "parking_lot_biz_type_desc",
            ]
        ].head(20),
        use_container_width=True,
    )

with col2:
    st.write("### 🗺️ 散點地圖")
    center_lat = df["parking_lot_latitude"].mean()
    center_lon = df["parking_lot_longitude"].mean()

    # ── 步驟 3：散點地圖 ──────────────────────────────────────
    fig = px.scatter_mapbox(
        df,
        lat="parking_lot_latitude",
        lon="parking_lot_longitude",
        color=color_col,
        size_max=15,
        hover_name="parking_lot_name",
        hover_data={
            "parking_lot_id": True,
            "parking_lot_city": True,
            "parking_lot_area": True,
            "parking_lot_biz_type_desc": True,
            "min_rent_start_date": True,
            "parking_lot_latitude": False,
            "parking_lot_longitude": False,
        },
        mapbox_style="open-street-map",
        zoom=7.5,
        center={"lat": center_lat, "lon": center_lon},
        height=560,
        title="共享單車站點分佈",
    )
    fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
    st.plotly_chart(fig, use_container_width=True)
