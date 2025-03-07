import streamlit as st

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
    layout="wide"
)

st.write(" # Welcome to the ECPTA App! 👋")

st.sidebar.success("Select a page above.")

st.write("---")

st.subheader("💻 Databases and Repositories ")
st.write("To access Databases and Repositories, navigate using the sidebar on the left or click the links below.")

toc = {
    "Meetings Summary Repository": "A common repository consolidating all meeting summaries with counterparty details.",
    "Turnarounds Database": "Quick access to the Refineries Turnarounds Database."
}

for page, description in toc.items():
    st.markdown(f"- **{page}**")
    st.write(description)

st.subheader("📊 PBI Dashboards")
dashboards = {
    "China Import Quotas": "https://app.powerbi.com/groups/me/reports/23f1a450-6e36-4852-bdc1-007ce1ee5289/9832c9e64ef03074b9f2?experience=power-bi",
    "China Analysis": "https://app.powerbi.com/groups/c1094db0-3d43-4a63-b304-e94a99943ade/reports/887722ee-b3f3-4550-8498-0adb065b3d9a?experience=power-bi",
    "India Analysis": "https://app.powerbi.com/groups/c1094db0-3d43-4a63-b304-e94a99943ade/reports/5bcc71e0-b21c-41d1-b093-367b9cd7439e?experience=power-bi",
    "Global Refinery Database": "Publishing"
}

for name, link in dashboards.items():
    st.markdown(f"- [**{name}**]({link})")

st.write("---")
st.write("For assistance or feedback, contact [delphine.loke@ecopetrol.asia]")