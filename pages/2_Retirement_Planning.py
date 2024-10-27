import streamlit as st
import numpy as np
from datetime import datetime


# Title
st.markdown("<h1 style='color:darkblue;'>📆 CPF Retirement Planning Simulator</h1>", unsafe_allow_html=True)

# Introduction
st.write("""
Welcome to the CPF Retirement Planning Simulator. This tool helps you to project your CPF withdrawal at 55 and CPF amount when you retire (according to the information you provide below) so that you can make informed decisions to plan for retirement.
""")

# User Inputs
# Create a table for OA, SA, and MA inputs
st.markdown("<h3 style='color:#114264;'>Current CPF Balances</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    oa_bal = st.number_input("Ordinary Account (OA)", min_value=0, value=100000, step=1000, help="Enter your current OA balance.")
with col2:
    sa_bal = st.number_input("Special Account (SA)", min_value=0, value=100000, step=1000, help="Enter your current SA balance.")
with col3:
    ma_bal = st.number_input("MediSave Account (MA)", min_value=0, value=100000, step=1000, help="Enter your current MA balance.")

# Income information
st.markdown("<h3 style='color:#114264;'>Income Information</h3>", unsafe_allow_html=True)
salary = st.number_input("Monthly Salary (SGD)", min_value=750, value=3000, step=1, help="Enter your monthly salary.")
st.write("Note: Applicable for income greater than $750.")
salary_inc = st.number_input("Annual Salary Increment (%)", min_value=0.0, value=2.0, step=0.1, help="Enter your expected annual salary increment percentage.")
bonus = st.number_input("Bonus (SGD)", min_value=0, value=9000, step=100, help="Enter your annual bonus.")

# Expected Annual Interest Rates
st.markdown("<h3 style='color:#114264;'>Expected Annual Interest Rates</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    oa_rate = st.number_input("OA Interest Rate (%)", min_value=0.0, value=2.5, step=0.1, help="Enter the expected annual interest rate for OA.")
with col2:
    sa_ma_rate = st.number_input("SA/MA Interest Rate (%)", min_value=0.0, value=4.0, step=0.1, help="Enter the expected annual interest rate for SA and MA.")
inflation = st.number_input("Expected Annual Inflation Rate (%)", min_value=0.0, value=2.0, step=0.1, help="Enter the expected annual inflation rate.")
st.write("Note: Singapore's average core inflation rate over the past 20 years has been below 2%.")

# Retirement Plan
st.markdown("<h3 style='color:#114264;'>Retirement Plan</h3>", unsafe_allow_html=True)
ret_age = st.number_input("Planned Retirement Age", min_value=55, help="Enter your planned retirement age.")
monthly_income = st.number_input("Desired Monthly Income in Retirement (SGD)", min_value=0, value=3000, step=100, help="Enter your desired monthly income in retirement.")
curr_age = st.number_input("Current Age", min_value=18, max_value=65, value=35, step=1, help="Enter your current age.")

# Ensure retirement age is greater than current age
if ret_age <= curr_age:
    st.error("Retirement age must be greater than current age.")
    st.stop()

# Data for BRS projections
years = np.array([2024, 2025, 2026, 2027])
brs = np.array([102900, 106500, 110200, 114100])
# Calculate the gradient (annual increase)
brs_gradient = np.gradient(brs, years)[0]
current_year = datetime.now().year
# Projected BRS and FRS for the year the user turns 55
start_year = current_year
start_brs = 102900
target_year = current_year + (55 - curr_age)

def project_retirement_sums(start_year, start_brs, brs_gradient, target_year):
    return start_brs + brs_gradient * (target_year - start_year)

projected_brs = project_retirement_sums(start_year, start_brs, brs_gradient, target_year)
projected_frs = 2 * projected_brs

def calculate_cpf_contributions_over_years(salary, bonus, curr_age, retirement_age, oa_rate, sa_ma_rate, oa_bal, sa_bal, ma_bal):
    salary_ceiling = 6800  # Monthly salary ceiling
    total_oa_contrib = oa_bal
    total_sa_contrib = sa_bal
    total_ma_contrib = ma_bal
    ra = 0  # Initialize Retirement Account
    for age in range(curr_age, retirement_age + 1):
        eff_salary = min(salary, salary_ceiling)
        if age <= 54:
            if age <= 35:
                contrib_rate = 0.37
                sa_ratio, ma_ratio = 0.1621, 0.2162
            elif 35 < age <= 45:
                contrib_rate = 0.37
                sa_ratio, ma_ratio = 0.1891, 0.2432
            elif 45 < age <= 50:
                contrib_rate = 0.37
                sa_ratio, ma_ratio = 0.2162, 0.2702
            elif 50 < age <= 54:
                contrib_rate = 0.37
                sa_ratio, ma_ratio = 0.3108, 0.2837
        else:
            if age == 55:
                contrib_rate = 0.37
                sa_ratio, ma_ratio = 0.3108, 0.2837
                # Transfer SA to RA
                total_oa_sa = total_oa_contrib + total_sa_contrib
                if total_oa_sa >= projected_frs:
                    ra += projected_frs
                    remaining_sa = total_sa_contrib - projected_frs
                    total_oa_contrib += remaining_sa
                else:
                    ra += total_oa_sa - 5000
                    total_oa_contrib = 5000
                total_sa_contrib = 0
            elif 55 < age <= 60:
                contrib_rate = 0.31
                ma_ratio = 0.3387
            elif 60 < age <= 65:
                contrib_rate = 0.22
                ma_ratio = 0.4772
            elif 65 < age <= 70:
                contrib_rate = 0.165
                ma_ratio = 0.6363
            else:  # age > 70
                contrib_rate = 0.125
                ma_ratio = 0.84

        total_cpf = (eff_salary * 12 * contrib_rate) + (bonus * contrib_rate)
        if age <= 54:
            sa_contrib = total_cpf * sa_ratio
            ma_contrib = total_cpf * ma_ratio
            oa_contrib = total_cpf - (sa_contrib + ma_contrib)
            total_sa_contrib += sa_contrib
        else:
            ma_contrib = total_cpf * ma_ratio
            oa_contrib = total_cpf - ma_contrib
        total_oa_contrib += oa_contrib
        total_ma_contrib += ma_contrib
        # Apply interest rates to the base sum plus new contributions
        total_oa_contrib *= (1 + oa_rate*0.01/12)
        total_sa_contrib *= (1 + sa_ma_rate*0.01/12)
        total_ma_contrib *= (1 + sa_ma_rate*0.01/12)
        ra *= (1 + sa_ma_rate*0.01/12)  # Apply interest to RA
    return {
        "Total OA Contribution": total_oa_contrib,
        "Total SA Contribution": total_sa_contrib,
        "Total MA Contribution": total_ma_contrib,
        "Retirement Account": ra}

def calculate_retirement_duration(ra_balance, oa_balance, monthly_income, inflation, sa_ma_rate):
    total_balance = ra_balance + oa_balance
    months = 0
    while total_balance > 0:
        # Adjust monthly income for inflation
        adjusted_income = monthly_income * ((1 + inflation*0.01) ** (months / 12))
        # Deduct the adjusted monthly income from the total balance
        total_balance -= adjusted_income 
        # Apply interest to the remaining balance
        total_balance *= (1 + sa_ma_rate*0.01 / 12)
        months += 1
    return months


# Calculate CPF contributions on retirement
cpf_contributions = calculate_cpf_contributions_over_years(salary, bonus, curr_age, ret_age, oa_rate, sa_ma_rate, oa_bal, sa_bal, ma_bal)

# Calculate CPF contributions @ 55 years old 
cpf_contributions_55 = calculate_cpf_contributions_over_years(salary, bonus, curr_age, 55, oa_rate, sa_ma_rate, oa_bal, sa_bal, ma_bal)
# Add existing balances to the calculated contributions
total_oa = cpf_contributions['Total OA Contribution']
total_sa = cpf_contributions['Total SA Contribution']
total_ma = cpf_contributions['Total MA Contribution']
ra = cpf_contributions['Retirement Account']
# Calculate how long the RA + OA can last
months = calculate_retirement_duration(ra, total_oa, monthly_income, inflation, sa_ma_rate)
years = months // 12
remaining_months = months % 12

st.write()
st.write()
# Display the results
st.markdown("<h2 style='color:#007B75; margin-top: 30px;'>Projected Retirement Sums at Age 55</h2>", unsafe_allow_html=True)

st.write(f"""
- **Projected Basic Retirement Sum (BRS):** ${projected_brs:.2f}
- **Projected Full Retirement Sum (FRS):** ${projected_frs:.2f}
""")

st.table({
    "Account": ["Ordinary Account (OA)", "MediSave Account (MA)", "Retirement Account (RA)"],
    "Amount (SGD)": [
        f"${cpf_contributions_55['Total OA Contribution']:.2f}",
        f"${cpf_contributions_55['Total MA Contribution']:.2f}",
        f"${cpf_contributions_55['Retirement Account']:.2f}"
    ]
})
st.write("note: The RA calculated will be slightly higher than the FRS due to interest accumulation.")
st.write()
st.markdown("<h2 style='color:#007B75; margin-top: 30px;'>Projected CPF amount during retirement</h2>", unsafe_allow_html=True)
st.table({
    "Account": ["Ordinary Account (OA)", "MediSave Account (MA)", "Retirement Account (RA)"],
    "Amount (SGD)": [
        f"${total_oa:.2f}",
        f"${total_ma:.2f}",
        f"${ra:.2f}"
    ]
})
st.write(f"Your RA and OA can last for {years} years and {remaining_months} months.")
st.write("note: The projection is based on no withdrawals before retirement.")
# Additional Information
st.markdown("""
<span style="color:darkred">
This simulation provides an estimate based on the inputs provided. Actual results may vary based on changes in CPF policies, interest rates, and inflation rates. It is not meant to replace any professional financial advice or personalized retirement planning.
</span>
""", unsafe_allow_html=True)