import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Quản Lý Điểm Sinh Viên",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 1. Dữ liệu sinh viên
data = {
    "Họ tên": [
        "An",
        "Bình",
        "Chi",
        "Dũng",
        "Hà",
        "Lan",
        "Minh",
        "Nam",
        "Phúc",
        "Trang",
    ],
    "Chuyên cần": [9.0, 8.5, 7.0, 9.5, 6.0, 8.0, 9.0, 7.5, 8.0, 9.5],
    "Giữa kỳ": [8.0, 8.0, 6.5, 9.0, 5.5, 7.0, 8.5, 6.0, 7.5, 9.0],
    "Cuối kỳ": [8.5, 8.5, 6.0, 9.0, 6.0, 5.0, 8.5, 7.0, 7.5, 9.5],
}

df = pd.DataFrame(data)

# 2. Tính điểm tổng kết (20% Chuyên cần + 30% Giữa kỳ + 50% Cuối kỳ)
df["Tong_ket"] = (
    0.2 * df["Chuyên cần"] + 0.3 * df["Giữa kỳ"] + 0.5 * df["Cuối kỳ"]
).round(2)


# 3. Xếp loại sinh viên
def xep_loai(score):
    if score >= 8.5:
        return "Giỏi"
    elif score >= 7.0:
        return "Khá"
    elif score >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"


df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# 4. Tính toán số liệu thống kê
tb_lop = df["Tong_ket"].mean()
sv_max = df.loc[df["Tong_ket"].idxmax()]
sv_min = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = (df["Tong_ket"] >= 5.0).sum()
ty_le_dat = (so_sv_dat / len(df)) * 100

# ==================== STREAMLIT INTERFACE ====================

# Tiêu đề chính
st.title("🎓 HỆ THỐNG QUẢN LÝ ĐIỂM SINH VIÊN")
st.markdown("---")

# Thống kê tổng quan (Kpi Cards)
st.subheader("📊 Thống Kê Tổng Quan")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Điểm trung bình lớp", value=f"{tb_lop:.2f}")
with col2:
    st.metric(
        label="Điểm cao nhất",
        value=f"{sv_max['Tong_ket']}",
        delta=sv_max["Họ tên"],
    )
with col3:
    st.metric(
        label="Điểm thấp nhất",
        value=f"{sv_min['Tong_ket']}",
        delta=sv_min["Họ tên"],
        delta_color="inverse",
    )
with col4:
    st.metric(
        label="Tỷ lệ đạt (≥ 5.0)",
        value=f"{so_sv_dat}/{len(df)}",
        delta=f"{ty_le_dat:.0f}%",
    )

st.markdown("---")

# Bảng điểm & Tra cứu
col_left, col_right = st.columns([1.8, 1.2])

with col_left:
    st.subheader("📋 Bảng Điểm Chi Tiết")
    # Hiển thị dataframe có style thanh điểm (Progress bar)
    st.dataframe(
        df,
        column_config={
            "Tong_ket": st.column_config.ProgressColumn(
                "Điểm Tổng Kết",
                help="Điểm tổng kết theo hệ số 20-30-50",
                format="%.2f",
                min_value=0,
                max_value=10,
            ),
        },
        use_container_width=True,
        hide_index=True,
    )

with col_right:
    st.subheader("🔍 Tra Cứu Sinh Viên")
    selected_student = st.selectbox(
        "Chọn sinh viên để xem chi tiết:", df["Họ tên"]
    )

    if selected_student:
        sv_info = df[df["Họ tên"] == selected_student].iloc[0]

        # Card thông tin chi tiết
        with st.container(border=True):
            st.markdown(f"### 👤 {sv_info['Họ tên']}")
            c1, c2 = st.columns(2)
            c1.write(f"• **Chuyên cần:** {sv_info['Chuyên cần']}")
            c1.write(f"• **Giữa kỳ:** {sv_info['Giữa kỳ']}")
            c2.write(f"• **Cuối kỳ:** {sv_info['Cuối kỳ']}")
            c2.write(f"• **Tổng kết:** `{sv_info['Tong_ket']}`")

            # Hiển thị badge xếp loại
            color = (
                "green"
                if sv_info["Xep_loai"] in ["Giỏi", "Khá"]
                else "orange" if sv_info["Xep_loai"] == "Trung bình" else "red"
            )
            st.markdown(f"**Xếp loại:** :{color}[**{sv_info['Xep_loai']}**]")

st.markdown("---")

# Biểu đồ trực quan hóa
st.subheader("📈 Biểu Đồ Điểm Tổng Kết")

fig, ax = plt.subplots(figsize=(10, 4.5))
colors = [
    "#4CAF50" if score >= 8.5 else "#2196F3" if score >= 7.0 else "#FF9800"
    for score in df["Tong_ket"]
]

bars = ax.barh(df["Họ tên"], df["Tong_ket"], color=colors, height=0.6)
ax.invert_yaxis()  # Thứ tự từ trên xuống
ax.set_xlim(0, 10.5)
ax.set_xlabel("Điểm Tổng Kết", fontsize=11, fontweight="bold")
ax.grid(axis="x", linestyle="--", alpha=0.5)

# Thêm nhãn điểm vào từng cột
for bar in bars:
    width = bar.get_width()
    ax.text(
        width + 0.1,
        bar.get_y() + bar.get_height() / 2,
        f"{width:.2f}",
        va="center",
        ha="left",
        fontsize=10,
        fontweight="bold",
    )

# Tùy chỉnh viền biểu đồ
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

st.pyplot(fig)

# Thông tin người thực hiện
st.markdown("---")
st.caption("👤 **Sinh viên thực hiện:** Mai Quang Nhật | **MSSV:** 066208006404")
