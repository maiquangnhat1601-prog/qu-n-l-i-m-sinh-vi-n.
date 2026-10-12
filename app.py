import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# Cấu hình trang Web App
st.set_page_config(
    page_title="Hệ Thống Quản Lý & Chi Tiết Điểm Sinh Viên",
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

# 4. Tính toán số liệu thống kê chung
tb_lop = df["Tong_ket"].mean()
sv_max = df.loc[df["Tong_ket"].idxmax()]
sv_min = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = (df["Tong_ket"] >= 5.0).sum()
ty_le_dat = (so_sv_dat / len(df)) * 100

# ==================== STREAMLIT INTERFACE ====================

# Tiêu đề chính
st.title("🎓 QUẢN LÝ VÀ XEM CHI TIẾT ĐIỂM SINH VIÊN")
st.markdown("---")

# Thống kê tổng quan (Kpi Cards)
st.subheader("📊 Thống Kê Tổng Quan Lớp Học")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Điểm trung bình lớp", value=f"{tb_lop:.2f}")
with col2:
    st.metric(
        label="Thủ khoa (Điểm cao nhất)",
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

# 🔍 TÍNH NĂNG XEM CHI TIẾT ĐIỂM TỪNG SINH VIÊN
st.subheader("🔍 TRA CỨU CHI TIẾT ĐIỂM THÀNH VIÊN")

selected_student = st.selectbox(
    "👉 Chọn tên sinh viên để xem phiếu điểm chi tiết:",
    df["Họ tên"],
    index=0,
)

if selected_student:
    sv_info = df[df["Họ tên"] == selected_student].iloc[0]

    with st.container(border=True):
        st.markdown(f"### 👤 Hồ Sơ Học Tập: **{sv_info['Họ tên']}**")

        c1, c2 = st.columns([1, 1])

        with c1:
            # Bảng thành phần điểm
            st.markdown("##### 📌 Chi tiết các cột điểm")
            detail_data = {
                "Thành phần": [
                    "Chuyên cần (20%)",
                    "Giữa kỳ (30%)",
                    "Cuối kỳ (50%)",
                    "Điểm Tổng Kết",
                ],
                "Điểm số": [
                    sv_info["Chuyên cần"],
                    sv_info["Giữa kỳ"],
                    sv_info["Cuối kỳ"],
                    sv_info["Tong_ket"],
                ],
            }
            df_detail = pd.DataFrame(detail_data)
            st.table(df_detail)

            # Xếp loại & Nhận xét
            color = (
                "green"
                if sv_info["Xep_loai"] in ["Giỏi", "Khá"]
                else "orange" if sv_info["Xep_loai"] == "Trung bình" else "red"
            )
            st.markdown(
                f"**Xếp loại học tập:** :{color}[**{sv_info['Xep_loai']}**]"
            )

            if sv_info["Tong_ket"] >= 8.5:
                st.success("🎉 Kết quả học tập xuất sắc! Tiếp tục duy trì phong độ.")
            elif sv_info["Tong_ket"] >= 7.0:
                st.info("👍 Kết quả học tập Khá. Cố gắng đạt kết quả cao hơn ở các môn sau.")
            elif sv_info["Tong_ket"] >= 5.0:
                st.warning("⚠️ Đã đạt môn. Cần cải thiện thêm ở bài thi Cuối kỳ.")
            else:
                st.error("❌ Không đạt. Cần đăng ký học lại môn này.")

        with c2:
            # Biểu đồ điểm cá nhân
            st.markdown("##### 📊 Biểu đồ phân tích điểm cá nhân")
            fig_individual, ax_ind = plt.subplots(figsize=(6, 3.8))
            categories = ["Chuyên cần", "Giữa kỳ", "Cuối kỳ", "Tổng kết"]
            scores = [
                sv_info["Chuyên cần"],
                sv_info["Giữa kỳ"],
                sv_info["Cuối kỳ"],
                sv_info["Tong_ket"],
            ]
            colors_ind = ["#4285F4", "#FBBC05", "#EA4335", "#34A853"]

            bars = ax_ind.bar(
                categories, scores, color=colors_ind, width=0.5
            )
            ax_ind.set_ylim(0, 10.5)
            ax_ind.set_ylabel("Điểm")
            ax_ind.grid(axis="y", linestyle="--", alpha=0.5)

            for bar in bars:
                yval = bar.get_height()
                ax_ind.text(
                    bar.get_x() + bar.get_width() / 2,
                    yval + 0.2,
                    f"{yval}",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                )

            st.pyplot(fig_individual)

st.markdown("---")

# BẢNG ĐIỂM TỔNG HỢP VÀ BIỂU ĐỒ CẢ LỚP
st.subheader("📋 Bảng Điểm & Biểu Đồ So Sánh Cả Lớp")

col_table, col_chart = st.columns([1.2, 1.8])

with col_table:
    st.markdown("##### Bảng điểm toàn bộ 10 sinh viên")
    st.dataframe(
        df,
        column_config={
            "Tong_ket": st.column_config.ProgressColumn(
                "Điểm Tổng Kết",
                format="%.2f",
                min_value=0,
                max_value=10,
            ),
        },
        use_container_width=True,
        hide_index=True,
    )

with col_chart:
    st.markdown("##### Biểu đồ so sánh Điểm tổng kết cả lớp")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    colors_all = [
        "#4CAF50" if score >= 8.5 else "#2196F3" if score >= 7.0 else "#FF9800"
        for score in df["Tong_ket"]
    ]

    bars = ax.barh(df["Họ tên"], df["Tong_ket"], color=colors_all, height=0.6)
    ax.invert_yaxis()
    ax.set_xlim(0, 10.5)
    ax.set_xlabel("Điểm Tổng Kết", fontsize=10, fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.5)

    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f"{width:.2f}",
            va="center",
            ha="left",
            fontsize=9,
            fontweight="bold",
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    st.pyplot(fig)

# Thông tin tác giả
st.markdown("---")
st.caption("👤 **Sinh viên thực hiện:** Mai Quang Nhật | **MSSV:** 066208006404")
