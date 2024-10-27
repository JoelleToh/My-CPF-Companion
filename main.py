import streamlit as st       


# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My CPF Companion"
)

# endregion <--------- Streamlit App Configuration --------->

# Title 
st.markdown("<h1 style='color:darkblue;'>Welcome to My CPF Companion</h1>", unsafe_allow_html=True)
st.write("Explore Our Key Features:")

st.text(" ")
st.subheader("📚CPF Policy Explainer")

st.write("""
         Have questions about CPF policies? Our CPF Policy Explainer is here to help!\n
        Simply ask any question about CPF policy in the link below, and our chatbot will assist you.
""")
# link to CPF Policy Explainer chatbot
st.page_link("pages/1_CPF_Policy_Explainer.py", label="CPF PolicyExplainer", icon="👉")

st.text(" ")
st.text(" ")

st.subheader("📆CPF Retirement Planning Simulator")
st.write("""
         Plan your retirement with our Retirement Planning Simulator in the link below.\n
        This tool helps you to project your CPF withdrawal at 55 and CPF amount when you retire\
          (according to the information you provide below)\
          so that you can make informed decisions to plan for retirement.
        
""")
# link to Retirement Planning Simulator
st.page_link("pages/2_Retirement_Planning.py", label="Retirement Planning Simulator", icon="👉")