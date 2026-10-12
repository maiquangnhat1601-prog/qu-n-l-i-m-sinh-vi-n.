import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# 1. Yêu cầu 1: Tạo DataFrame chứa thông tin 10 sinh viên
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

# 2. Yêu cầu 2: Tính điểm tổng kết = 20% Chuyên cần + 30% Giữa kỳ + 50% Cuối kỳ
df["Tong_ket"] = (
    0.2 * df["Chuyên cần"] + 0.3 * df["Giữa kỳ"] + 0.5 * df["Cuối kỳ"]
).round(2)


# 3. Yêu cầu 3: Xếp loại sinh viên
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

# 4. Yêu cầu 4: Thống kê
tb_lop = df["Tong_ket"].mean()
sv_max = df.loc[df["Tong_ket"].idxmax()]
sv_min = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = (df["Tong_ket"] >= 5.0).sum()

# ==================== STREAMLIT WEB APP ====================

# Hiển thị tiêu đề
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# Hiển thị bảng điểm
st.subheader("Bảng điểm sinh viên")
st.dataframe(df)

# Hiển thị thông tin thống kê
st.subheader("Thống kê")
st.write(f"- Điểm trung bình của lớp: **{tb_lop:.2f}**")
st.write(
    f"- Sinh viên có điểm tổng kết cao nhất: **{sv_max['Họ tên']}** ({sv_max['Tong_ket']} điểm)"
)
st.write(
    f"- Sinh viên có điểm tổng kết thấp nhất: **{sv_min['Họ tên']}** ({sv_min['Tong_ket']} điểm)"
)
st.write(f"- Số sinh viên đạt (điểm tổng kết ≥ 5.0): **{so_sv_dat}**")

# Selectbox chọn sinh viên
st.subheader("Tra cứu thông tin sinh viên")
selected_student = st.selectbox("Chọn sinh viên:", df["Họ tên"])

if selected_student:
    sv_info = df[df["Họ tên"] == selected_student].iloc[0]
    st.write(f"- **Chuyên cần:** {sv_info['Chuyên cần']}")
    st.write(f"- **Giữa kỳ:** {sv_info['Giữa kỳ']}")
    st.write(f"- **Cuối kỳ:** {sv_info['Cuối kỳ']}")
    st.write(f"- **Điểm tổng kết:** {sv_info['Tong_ket']}")
    st.write(f"- **Xếp loại:** {sv_info['Xep_loai']}")

# 5. Yêu cầu 5: Trực quan hóa (Biểu đồ cột ngang)
st.subheader("Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(8, 5))
y_pos = np.arange(len(df["Họ tên"]))

ax.barh(y_pos, df["Tong_ket"], align="center", color="#4C8BF5")
ax.set_yticks(y_pos)
ax.set_yticklabels(df["Họ tên"])
ax.invert_yaxis()  # Đảo ngược thứ tự để danh sách hiển thị từ trên xuống
ax.set_xlabel("Điểm tổng kết")
ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.set_xlim(0, 10)

st.pyplot(fig)

# Thông tin tác giả ở cuối trang (chữ nhỏ)
st.markdown("---")
st.caption("Họ và tên: Mai Quang Nhật | MSSV: 066208006404")
