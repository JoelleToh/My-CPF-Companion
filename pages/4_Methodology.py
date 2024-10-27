import streamlit as st
from graphviz import Digraph

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

# Function to create flowchart (My CPF Policy Assistant)
def create_flowchart_1():
    dot = Digraph()
    dot.node('A', 'Start', shape='ellipse')
    dot.node('B', 'User Enters Query', shape='box')
    dot.node('C', 'LLM Decides if Query is Related to CPF Policy', shape='diamond')
    dot.edges(['AB', 'BC'])
    
    # Decision making step 1
    dot.node('D', "Reply: 'I'm unable to assist as the enquiry is not related to CPF policy.'", shape='box')
    dot.node('E', 'End', shape='ellipse')
    dot.edge('C', 'D', label='No')
    dot.edges(['DE'])
    
    dot.node('F', 'Retrieve Relevant Docs using RAG', shape='box')
    dot.node('G', 'Generate Response using LLM', shape='box')
    dot.node('H', 'Display Response', shape='box')
    dot.edges(['FG', 'GH'])
    dot.edge('C', 'F', label='Yes')
    
    # Decision making step 2
    dot.node('I', 'Any further user input?', shape='diamond')
    dot.edge('H', 'I')
    dot.node('J', 'LLM Decides if Query is Related to CPF Policy', shape='diamond')
    dot.node('P', "Reply: 'I'm unable to assist as the enquiry is not related to CPF policy.'", shape='box')
    dot.node('Q', 'End', shape='ellipse')
    dot.edge('P', 'Q', label='No')
    dot.edges(['JP'])

    ## Decision making step 3
    dot.node('K', 'Retrieve Relevant Docs using RAG', shape='box')
    dot.node('L', 'Combine Conversation History with Retrieved Info', shape='box')
    dot.node('M', 'Generate Response using LLM', shape='box')
    dot.node('N', 'Display Response', shape='box')
    dot.node('O', 'End', shape='ellipse')
    dot.edge('I', 'J', label='Yes')
    dot.edge('J', 'K')
    dot.edge('K', 'L')
    dot.edge('L', 'M')
    dot.edge('M', 'N')
    dot.edge('N', 'I')
    dot.edge('I', 'O', label='No')
    
    return dot

# Function to create flowchart (My CPF Policy Assistant)
def create_flowchart_2():
    dot = Digraph()
    dot.node('A', 'Start', shape='ellipse')
    dot.node('B', 'User Enters inputs', shape='box')
    dot.node('C', "Bot perfrom calculation", shape='box')
    dot.node('D', 'Display Response', shape='box')
    dot.node('E', 'End', shape='ellipse')
    dot.edges(['AB', 'BC', 'CD', 'DE' ])
    
    return dot



# Title
st.markdown('<div class="about-us-title">Methodologys</div>', unsafe_allow_html=True)
st.write("""
### Explanation of Data Flows and Implementation Details
- **Data Sources**: Data comes from CPF website and user inputs.
- **Data Processing**: Data is processed and transformed within the app.
- **User Interaction**: Users interact with the app through various inputs.
- **Output Generation**: The app generates outputs based on user interactions and data processing.
""")
# Flowchart Section
st.markdown('<div class="custom-header">Flowchart: My CPF Policy Assistant</div>', unsafe_allow_html=True)
st.graphviz_chart(create_flowchart_1())

st.markdown('<div class="custom-header">Flowchart: CPF Retirement Planning Simulator</div>', unsafe_allow_html=True)
st.graphviz_chart(create_flowchart_2())