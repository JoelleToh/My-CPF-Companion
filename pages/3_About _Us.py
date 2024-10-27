import streamlit as st

# Set the page configuration
st.set_page_config(page_title="About Us", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .about-us-title {
        color: darkblue;
        font-size: 2.5em;
        font-weight: bold;
    }
    .custom-header {
        color: #114264;
        font-size: 1.5em;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of the About Us Page
st.markdown('<div class="about-us-title">About Us</div>', unsafe_allow_html=True)

# Project Scope Section
st.markdown('<div class="custom-header">Project Scope</div>', unsafe_allow_html=True)
st.write(
    "This project (My CPF Companion) aims to provide users with accurate and timely information regarding the Central Provident Fund (CPF) in Singapore through the following two bots:"
)

# List of Bots
st.write(
    "1. **My CPF Policy Assistant**: This bot provides users with accurate and timely information regarding CPF through interaction with a friendly virtual assistant."
)

st.write(
    "2. **CPF Retirement Planning Simulator**: This tool helps you to project your CPF withdrawal at 55 and CPF amount when you retire (according to the information you provide below) so that you can make informed decisions to plan for retirement."
)

# Objectives Section
st.markdown('<div class="custom-header">Objectives</div>', unsafe_allow_html=True)
st.markdown(
    """
    - **Provide Accurate Information**: To deliver reliable and up-to-date information about CPF policies based on official sources.
    - **Enhance User Experience**: To create an intuitive interface that allows users to ask questions and receive instant responses related to CPF.
    """
)

# Data Sources Section
st.markdown('<div class="custom-header">Data Sources</div>', unsafe_allow_html=True)
st.write(
    "The CPF Policy Assistant utilizes data from multiple reputable sources, including:"
)
st.markdown(
    """
    - The official Central Provident Fund Board (CPF) website for the latest policy updates and information.
    - News releases and official announcements related to CPF.
    """
)

# Features Section
st.markdown('<div class="custom-header">Features</div>', unsafe_allow_html=True)
st.markdown(
    """
    - **Natural Language Processing**: Leverage advanced AI technology to understand and respond to user queries in natural language.
    - **Retrieval-Augmented Generation (RAG)**: Utilize a robust retrieval mechanism to ensure responses are based on the most relevant and recent information.
    - **Interactive User Interface**: A user-friendly interface that makes it easy for users to ask questions and receive answers.
    """
)

# Optional: Add a footer with additional information
st.write("---")
st.write("© 2024 My CPF Companion. All rights reserved.")
