import os
from datetime import date

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

DATA_FILE = "green_campus_data.csv"

COLUMNS = [
    "Date", "User", "Role", "Class/Department",
    "Energy (kWh)", "Water (L)", "Total Waste (kg)",
    "Recycled Waste (kg)", "Green Waste (kg)",
    "Trees Planted", "Plants/Saplings",
    "Rainwater Harvested (L)", "Solar Energy (kWh)"
]

st.set_page_config(
    page_title="School Green Campus Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* ============================================================
   FINAL GREEN VISIBILITY VERSION
   COLOUR CHANGES ONLY.
   No layout, navigation, data, calculations or functionality
   have been changed.
   ============================================================ */

/* ---------- COMPLETE MAIN APP BACKGROUND ---------- */
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #2e8b57 !important;
}

[data-testid="stAppViewContainer"] {
    background-image: none !important;
}

/* Keep Streamlit header transparent */
[data-testid="stHeader"] {
    background: transparent !important;
}

/* ============================================================
   MAIN HEADINGS
   WHITE = maximum contrast against green
   ============================================================ */
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4,
[data-testid="stMain"] h5,
[data-testid="stMain"] h6,
[data-testid="stMain"] h1 *,
[data-testid="stMain"] h2 *,
[data-testid="stMain"] h3 *,
[data-testid="stMain"] h4 *,
[data-testid="stMain"] h5 *,
[data-testid="stMain"] h6 * {
    color: #ffffff !important;
    -webkit-text-fill-color: #000000 !important;
    text-shadow: none !important;
}

/* Main title */
.main-title,
.main-title * {
    color: #000000 !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Subheadings / descriptions */
.subtitle,
.subtitle * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #e7f6c5 !important;
}

/* ============================================================
   NORMAL TEXT ON GREEN BACKGROUND
   WHITE — replaces the old green text
   ============================================================ */
[data-testid="stMain"] .stMarkdown,
[data-testid="stMain"] .stMarkdown p,
[data-testid="stMain"] .stMarkdown li,
[data-testid="stMain"] p,
[data-testid="stMain"] li {
    color: #7C4700 !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* ============================================================
   SCOREBOARD / KPI CARDS
   WHITE CARDS + DARK/GREEN TEXT = CLEAR AND READABLE
   ============================================================ */
.card {
    background: #ffffff !important;
    border: 1px solid #d8eadc !important;
    color: #111111 !important;
}

.card * {
    background-color: transparent !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #111111 !important;
}

/* Card titles */
.card h1,
.card h2,
.card h3,
.card h4,
.card h5,
.card h6,
.card h1 *,
.card h2 *,
.card h3 *,
.card h4 *,
.card h5 *,
.card h6 * {
    color: #08783e !important;
    -webkit-text-fill-color: #08783e !important;
}

/* Card values/details */
.card p,
.card span,
.card label,
.card div {
    color: #7FFF00 !important;
    -webkit-text-fill-color: #111111 !important;
}

/* ============================================================
   STREAMLIT METRIC SCOREBOARDS
   ============================================================ */
[data-testid="stMetric"] {
    background: #F0C807 !important;
    border: 1px solid #d8eadc !important;
    border-radius: 14px !important;
}

[data-testid="stMetric"] * {
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="stMetricValue"] div {
    color: #08783e !important;
    -webkit-text-fill-color: #08783e !important;
    font-weight: 800 !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * {
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
    font-weight: 700 !important;
}

[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] * {
    color: #08783e !important;
    -webkit-text-fill-color: #08783e !important;
}

/* ============================================================
   ENTER DETAILS + TRACKING
   HEADINGS = WHITE
   FORM TEXT = BLACK ON WHITE INPUTS
   ============================================================ */
[data-testid="stForm"] {
    color: #111111 !important;
}

[data-testid="stForm"] label,
[data-testid="stForm"] label *,
[data-testid="stForm"] p {
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
}

/* Inputs */
[data-testid="stMain"] input,
[data-testid="stMain"] textarea {
    background: #00B496 !important;
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
    caret-color: #111111 !important;
}

[data-testid="stMain"] input::placeholder,
[data-testid="stMain"] textarea::placeholder {
    color: #5f6b63 !important;
    -webkit-text-fill-color: #5f6b63 !important;
}

/* Dropdowns */
[data-testid="stMain"] [data-baseweb="select"],
[data-testid="stMain"] [data-baseweb="select"] > div {
    background: #4FB06D !important;
    color: #111111 !important;
}

[data-testid="stMain"] [data-baseweb="select"] *,
[data-testid="stMain"] [role="option"],
[data-testid="stMain"] [role="option"] * {
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
}

[data-testid="stMain"] [role="listbox"] {
    background: #ffffff !important;
}

/* Date input */
[data-testid="stMain"] [data-baseweb="input"],
[data-testid="stMain"] [data-baseweb="input"] input {
    background: #ffffff !important;
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
}

/* ============================================================
   ALERTS
   ============================================================ */
[data-testid="stMain"] [data-testid="stAlert"],
[data-testid="stMain"] [data-testid="stAlert"] * {
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
}

/* ============================================================
   TABLE
   ============================================================ */
[data-testid="stMain"] [data-testid="stDataFrame"] {
    background: #ffffff !important;
}

[data-testid="stMain"] [data-testid="stDataFrame"] * {
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
}

/* ============================================================
   CAPTIONS
   ============================================================ */
[data-testid="stMain"] [data-testid="stCaptionContainer"] *,
[data-testid="stMain"] .stCaption {
    color: #e7f6c5 !important;
    -webkit-text-fill-color: #e7f6c5 !important;
}

/* ============================================================
   BUTTONS
   ============================================================ */
[data-testid="stMain"] button,
[data-testid="stMain"] button * {
    color: #ffffff !important;
    -webkit-text-fill-color: #111111 !important;
}

/* ============================================================
   LINKS
   ============================================================ */
[data-testid="stMain"] a,
[data-testid="stMain"] a * {
    color: #fff4a8 !important;
    -webkit-text-fill-color: #fff4a8 !important;
}

/* ============================================================
   SIDEBAR — PRESERVE ITS EXISTING GREEN/PLANT DESIGN
   ============================================================ */
[data-testid="stSidebar"] {
    /* Existing sidebar remains in place */
}

[data-testid="stSidebar"] * {
    color: #000000 !important;
    -webkit-text-fill-color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)


def create_data_file():
    if not os.path.exists(DATA_FILE):
        sample = pd.DataFrame([
            [str(date.today()), "Demo Student", "Student", "Class 12",
             120, 1500, 40, 25, 10, 3, 8, 500, 35],
            [str(date.today()), "Eco Team", "Student", "Class 11",
             100, 1300, 35, 22, 8, 2, 5, 350, 28],
        ], columns=COLUMNS)
        sample.to_csv(DATA_FILE, index=False)


def load_data():
    create_data_file()
    df = pd.read_csv(DATA_FILE)
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = 0
    return df[COLUMNS]


def save_data(df):
    df.to_csv(DATA_FILE, index=False)


def add_record(values):
    df = load_data()
    new_row = pd.DataFrame([values], columns=COLUMNS)
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)


def recycling_rate(df):
    total = df["Total Waste (kg)"].sum()
    recycled = df["Recycled Waste (kg)"].sum()
    return (recycled / total * 100) if total > 0 else 0


def calculate_points(row):
    return (
        row["Trees Planted"] * 10
        + row["Plants/Saplings"] * 3
        + row["Recycled Waste (kg)"] * 2
        + row["Green Waste (kg)"]
        + row["Rainwater Harvested (L)"] / 100
        + row["Solar Energy (kWh)"] * 0.5
    )


def get_badge(points):
    if points >= 500: return "🏆 Earth Champion"
    if points >= 300: return "🌳 Green Guardian"
    if points >= 150: return "🌿 Eco Warrior"
    if points >= 50: return "♻️ Green Starter"
    return "🌱 Eco Explorer"


def create_leaderboard(df):
    if df.empty:
        return pd.DataFrame(columns=["User", "Points", "Badge"])
    work = df.copy()
    work["Points"] = work.apply(calculate_points, axis=1)
    board = work.groupby("User", as_index=False)["Points"].sum()
    board["Points"] = board["Points"].round(1)
    board["Badge"] = board["Points"].apply(get_badge)
    return board.sort_values("Points", ascending=False).reset_index(drop=True)


def show_header():
    st.markdown(
        '<div class="main-title">🌱 School Green Campus Sustainability Dashboard</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">Track energy, water, waste, recycling, trees and other green-campus activities.</div>',
        unsafe_allow_html=True
    )


def entry_screen():
    st.markdown("## 🌱 Enter Your Green Campus Details")
    st.info("Enter your activity details and click Submit. The dashboard will appear after submission.")

    with st.form("green_entry_form", clear_on_submit=False):
        c1, c2 = st.columns(2)

        with c1:
            name = st.text_input("Name *", placeholder="Enter your name")
            role = st.selectbox("Role", ["Student", "Teacher", "Staff", "Eco Club"])
            class_department = st.text_input(
                "Class / Department", placeholder="Example: Class 12 / Science"
            )
            entry_date = st.date_input("Date", value=date.today())
            energy = st.number_input("Energy Used (kWh)", min_value=0.0, step=1.0)
            water = st.number_input("Water Used (L)", min_value=0.0, step=10.0)

        with c2:
            total_waste = st.number_input("Total Waste (kg)", min_value=0.0, step=1.0)
            recycled_waste = st.number_input("Recycled Waste (kg)", min_value=0.0, step=1.0)
            green_waste = st.number_input("Green Waste (kg)", min_value=0.0, step=1.0)
            trees = st.number_input("Trees Planted", min_value=0, step=1)
            plants = st.number_input("Plants / Saplings", min_value=0, step=1)
            rainwater = st.number_input("Rainwater Harvested (L)", min_value=0.0, step=10.0)
            solar = st.number_input("Solar Energy Generated (kWh)", min_value=0.0, step=1.0)

        submitted = st.form_submit_button("🌿 Submit Details", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Please enter your name.")
            return
        if recycled_waste > total_waste:
            st.error("Recycled waste cannot be greater than total waste.")
            return
        if green_waste > total_waste:
            st.error("Green waste cannot be greater than total waste.")
            return

        add_record([
            str(entry_date), name.strip(), role,
            class_department.strip() or "Not specified",
            energy, water, total_waste, recycled_waste, green_waste,
            trees, plants, rainwater, solar
        ])
        st.session_state.submitted = True
        st.session_state.current_user = name.strip()
        st.success("Details submitted successfully! Opening your dashboard...")
        st.rerun()


def dashboard(df):
    show_header()
    rate = recycling_rate(df)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("⚡ Energy", f"{df['Energy (kWh)'].sum():,.0f} kWh")
    m2.metric("💧 Water", f"{df['Water (L)'].sum():,.0f} L")
    m3.metric("♻️ Recycling", f"{rate:.1f}%")
    m4.metric("🌳 Trees", f"{df['Trees Planted'].sum():,.0f}")

    m5, m6, m7, m8 = st.columns(4)
    m5.metric("🌱 Plants", f"{df['Plants/Saplings'].sum():,.0f}")
    m6.metric("🍃 Green Waste", f"{df['Green Waste (kg)'].sum():,.0f} kg")
    m7.metric("☀️ Solar", f"{df['Solar Energy (kWh)'].sum():,.0f} kWh")
    m8.metric("🌧️ Rainwater", f"{df['Rainwater Harvested (L)'].sum():,.0f} L")

    if rate >= 60:
        st.success("🌟 Great work! The campus has a strong recycling rate.")
    elif rate >= 30:
        st.warning("♻️ Recycling is improving. Try increasing waste segregation.")
    else:
        st.error("🌱 Recycling needs attention. Start with better waste separation.")

    st.markdown("### 📈 Sustainability Trend")
    trend = df.groupby("Date", as_index=False)[
        ["Energy (kWh)", "Water (L)", "Recycled Waste (kg)"]
    ].sum()
    if len(trend) > 1:
        st.line_chart(trend.set_index("Date"), use_container_width=True)
    else:
        st.info("Add more dated entries to see a trend chart.")

    st.markdown("### 📝 Recent Activity")
    st.dataframe(df.tail(10).iloc[::-1], use_container_width=True, hide_index=True)


def tracking(df):
    show_header()
    st.markdown("## 📊 Tracking")

    users = ["All"] + sorted(df["User"].dropna().unique().tolist())
    selected_user = st.selectbox("Filter by User", users)

    departments = ["All"] + sorted(df["Class/Department"].dropna().unique().tolist())
    selected_department = st.selectbox("Filter by Class / Department", departments)

    filtered = df.copy()
    if selected_user != "All":
        filtered = filtered[filtered["User"] == selected_user]
    if selected_department != "All":
        filtered = filtered[filtered["Class/Department"] == selected_department]

    st.dataframe(filtered, use_container_width=True, hide_index=True)

    if not filtered.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### ♻️ Waste vs Recycling")
            waste_chart = filtered[["Date", "Total Waste (kg)", "Recycled Waste (kg)"]].groupby("Date").sum()
            st.bar_chart(waste_chart, use_container_width=True)
        with c2:
            st.markdown("### 🌳 Trees & Plants")
            green_chart = filtered[["Date", "Trees Planted", "Plants/Saplings"]].groupby("Date").sum()
            st.bar_chart(green_chart, use_container_width=True)

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Tracking Data (CSV)", csv,
        "green_campus_tracking.csv", "text/csv"
    )


def green_guardians(df):
    show_header()
    st.markdown("## 🏆 Green Guardians")
    st.write("A leaderboard based on eco-friendly actions submitted by different users.")

    board = create_leaderboard(df)
    if board.empty:
        st.info("No submissions yet.")
        return

    top = board.head(3)
    cols = st.columns(3)
    for i, col in enumerate(cols):
        if i < len(top):
            row = top.iloc[i]
            with col:
                st.markdown(
                    f'<div class="card"><h3>#{i + 1} {row["User"]}</h3>'
                    f'<h2>{row["Points"]:.1f} points</h2><p>{row["Badge"]}</p></div>',
                    unsafe_allow_html=True
                )

    st.markdown("### 📋 Full Leaderboard")
    display_board = board.copy()
    display_board.insert(0, "Rank", range(1, len(display_board) + 1))
    st.dataframe(display_board, use_container_width=True, hide_index=True)

    current_user = st.session_state.get("current_user")
    if current_user:
        me = display_board[display_board["User"] == current_user]
        if not me.empty:
            row = me.iloc[0]
            st.success(f"Your current score: {row['Points']:.1f} points — {row['Badge']}")


def eco_tips():
    show_header()
    st.markdown("## 💡 Eco-Friendly Tips")
    tips = [
        ("⚡ Energy", "Switch off lights, fans and equipment when they are not needed."),
        ("💧 Water", "Report leaking taps and avoid unnecessary water use."),
        ("♻️ Recycling", "Separate paper, plastic, metal and other recyclable materials."),
        ("🍃 Green Waste", "Collect leaves and organic waste separately for composting."),
        ("🌳 Plants", "Plant and care for suitable native trees and plants."),
        ("☀️ Solar", "Use renewable energy wherever practical."),
        ("🌧️ Rainwater", "Collect rainwater for suitable non-drinking uses."),
        ("🚶 Transport", "Walk, cycle or use shared transport for suitable trips."),
        ("🥤 Reusables", "Prefer reusable bottles and containers over disposable ones."),
    ]
    for title, text in tips:
        st.markdown(
            f'<div class="card"><h3>{title}</h3><p>{text}</p></div>',
            unsafe_allow_html=True
        )


def about():
    show_header()
    st.markdown("## ℹ️ About This Project")
    st.write(
        "The School Green Campus Sustainability Dashboard is a Streamlit-based "
        "prototype for recording and visualising sustainability activities in a school."
    )
    st.markdown("### 🎯 Main Objectives")
    st.write(
        "- Track energy and water use\n"
        "- Monitor waste and recycling\n"
        "- Record trees and plants added to campus\n"
        "- Track solar energy and rainwater harvesting\n"
        "- Encourage students through the Green Guardians leaderboard\n"
        "- Provide simple eco-friendly tips"
    )
    st.markdown("### 🛠️ Technology")
    st.write("Python • Streamlit • Pandas • Matplotlib • CSV data storage")
    st.info(
        "This version updates immediately when users submit data. "
        "For a large public deployment or real IoT sensor streaming, "
        "replace CSV storage with a database and connect sensor APIs."
    )


if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

df = load_data()

if not st.session_state.submitted:
    entry_screen()
    st.stop()

show_header()

with st.sidebar:
    st.markdown("## 🌱 Green Campus")
    st.caption(f"Current user: {st.session_state.current_user}")
    page = st.radio(
        "Menu",
        ["Dashboard", "Enter Details", "Tracking", "Green Guardians", "Eco Tips", "About"],
        index=0,
    )
    st.markdown("---")
    if st.button("➕ Enter as Another User", use_container_width=True):
        st.session_state.submitted = False
        st.session_state.current_user = ""
        st.rerun()

if page == "Dashboard":
    dashboard(df)
elif page == "Enter Details":
    entry_screen()
elif page == "Tracking":
    tracking(df)
elif page == "Green Guardians":
    green_guardians(df)
elif page == "Eco Tips":
    eco_tips()
elif page == "About":
    about()
