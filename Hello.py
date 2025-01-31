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
    "China Import Quotas": "https://app.powerbi.com/groups/me/reports/23f1a450-6e36-4852-bdc1-007ce1ee5289/9832c9e64ef03074b9f2?experience=power-bi"
}

for name, link in dashboards.items():
    st.markdown(f"- [**{name}**]({link})")

st.write("---")
st.write("For assistance or feedback, contact [delphine.loke@ecopetrol.asia]")