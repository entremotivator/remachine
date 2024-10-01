import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Title of the Streamlit application
st.title("Enhanced Real Estate Financial Calculator")

# Sidebar for user inputs
st.sidebar.header("User Inputs")
cost_price = st.sidebar.number_input("Enter Cost Price ($):", value=230157.34, format="%.2f")
price_range_low = st.sidebar.number_input("Enter Price Range Low ($):", value=195738.24, format="%.2f")
price_range_high = st.sidebar.number_input("Enter Price Range High ($):", value=264576.44, format="%.2f")
interest_rate = st.sidebar.number_input("Enter Interest Rate (%):", value=4.0, format="%.1f") / 100
loan_duration = st.sidebar.number_input("Enter Loan Duration (years):", value=30, format="%d")
property_tax_rate = st.sidebar.number_input("Enter Property Tax Rate (%):", value=1.0, format="%.1f") / 100
insurance_rate = st.sidebar.number_input("Enter Homeowners Insurance Rate (%):", value=0.5, format="%.1f") / 100
monthly_expenses = st.sidebar.number_input("Enter Monthly Expenses ($):", value=2000, format="%.2f")
appreciation_rate = st.sidebar.number_input("Enter Annual Appreciation Rate (%):", value=3.0, format="%.1f") / 100

# Calculations
# 1. Down Payment Calculation (20% of COST_PRICE)
down_payment = cost_price * 0.20

# 2. Loan Amount After Down Payment
loan_amount = cost_price - down_payment

# 3. Monthly Payment Calculation
n = loan_duration * 12  # Total number of payments
r = interest_rate / 12  # Monthly interest rate
monthly_payment = loan_amount * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

# 4. Monthly Property Tax Calculation
annual_property_tax = cost_price * property_tax_rate
monthly_property_tax = annual_property_tax / 12

# 5. Monthly Insurance Payment Calculation
annual_insurance = cost_price * insurance_rate
monthly_insurance = annual_insurance / 12

# 6. Total Monthly Payment Including Taxes and Insurance
total_monthly_payment = monthly_payment + monthly_property_tax + monthly_insurance

# 7. Total Amount Paid Over the Loan Duration
total_payments = total_monthly_payment * 12 * loan_duration

# 8. Total Interest Paid Over the Loan Duration
total_interest = total_payments - loan_amount

# 9. Average Price Calculation
average_price = (price_range_low + price_range_high) / 2

# 10. Percentage Difference from LOW to HIGH
percentage_difference = ((price_range_high - price_range_low) / price_range_low) * 100

# 11. ROI if sold at HIGH price (10% increase)
selling_price = cost_price * 1.10  # Selling price at 10% higher
roi = ((selling_price - cost_price) / cost_price) * 100

# 12. Break-even Point Calculation
break_even_months = cost_price / monthly_expenses
break_even_years = break_even_months / 12

# 13. Future Value of Investment After 5 Years
future_value = cost_price * (1 + appreciation_rate) ** 5

# Detailed year-by-year payment breakdown
years = np.arange(1, loan_duration + 1)
remaining_balance = loan_amount
interest_paid = []
principal_paid = []
balance_history = []

for year in years:
    interest_for_year = 0
    principal_for_year = 0
    for month in range(12):
        interest_for_year += remaining_balance * r
        principal_payment = total_monthly_payment - (remaining_balance * r)
        principal_for_year += principal_payment
        remaining_balance -= principal_payment
    interest_paid.append(interest_for_year)
    principal_paid.append(principal_for_year)
    balance_history.append(remaining_balance)

# Create DataFrame for payment breakdown
payment_df = pd.DataFrame({
    'Year': years,
    'Interest Paid': interest_paid,
    'Principal Paid': principal_paid,
    'Remaining Balance': balance_history
})

# Display results
st.header("Calculation Results")
st.write(f"1. Down Payment: ${down_payment:,.2f}")
st.write(f"2. Loan Amount After Down Payment: ${loan_amount:,.2f}")
st.write(f"3. Monthly Payment: ${monthly_payment:,.2f}")
st.write(f"4. Monthly Property Tax: ${monthly_property_tax:,.2f}")
st.write(f"5. Monthly Insurance Payment: ${monthly_insurance:,.2f}")
st.write(f"6. Total Monthly Payment: ${total_monthly_payment:,.2f}")
st.write(f"7. Total Amount Paid Over Loan Duration: ${total_payments:,.2f}")
st.write(f"8. Total Interest Paid Over Loan Duration: ${total_interest:,.2f}")
st.write(f"9. Average Price: ${average_price:,.2f}")
st.write(f"10. Percentage Difference from Low to High: {percentage_difference:.2f}%")
st.write(f"11. ROI if Sold at High Price (10% Increase): {roi:.2f}%")
st.write(f"12. Break-even Point: {break_even_months:.2f} months ({break_even_years:.2f} years)")
st.write(f"13. Future Value After 5 Years: ${future_value:,.2f}")

# Display payment breakdown
st.subheader("Yearly Payment Breakdown")
st.dataframe(payment_df)

# Downloadable Amortization Schedule
csv = payment_df.to_csv(index=False)
st.download_button(label="Download Amortization Schedule as CSV", data=csv, file_name='amortization_schedule.csv', mime='text/csv')

# Plot the results
fig, ax = plt.subplots(3, 1, figsize=(10, 12))

# Interest and Principal Paid Plot
ax[0].bar(payment_df['Year'], payment_df['Interest Paid'], label='Interest Paid', color='red', alpha=0.6)
ax[0].bar(payment_df['Year'], payment_df['Principal Paid'], label='Principal Paid', color='green', alpha=0.6)
ax[0].set_title('Yearly Interest and Principal Paid')
ax[0].set_xlabel('Year')
ax[0].set_ylabel('Amount ($)')
ax[0].legend()

# Remaining Balance Plot
ax[1].plot(payment_df['Year'], payment_df['Remaining Balance'], label='Remaining Balance', marker='o', color='blue')
ax[1].set_title('Remaining Loan Balance Over Time')
ax[1].set_xlabel('Year')
ax[1].set_ylabel('Remaining Balance ($)')
ax[1].legend()

# Total Payment Breakdown Pie Chart
ax[2].pie([total_interest, total_payments - total_interest], labels=['Total Interest', 'Principal Payments'], autopct='%1.1f%%', startangle=90)
ax[2].axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
ax[2].set_title('Total Payment Breakdown')

plt.tight_layout()
st.pyplot(fig)

# Sensitivity Analysis Section
st.header("Monthly Payment Sensitivity Analysis")
st.subheader("Adjust Interest Rate and Loan Duration")

# Sliders for sensitivity analysis
adjusted_interest_rate = st.slider("Adjust Interest Rate (%):", min_value=1.0, max_value=10.0, value=interest_rate*100, step=0.1)
adjusted_loan_duration = st.slider("Adjust Loan Duration (years):", min_value=5, max_value=30, value=loan_duration)

# Recalculate monthly payment based on adjusted values
adjusted_n = adjusted_loan_duration * 12
adjusted_r = adjusted_interest_rate / 100 / 12
adjusted_monthly_payment = loan_amount * (adjusted_r * (1 + adjusted_r) ** adjusted_n) / ((1 + adjusted_r) ** adjusted_n - 1)
adjusted_total_monthly_payment = adjusted_monthly_payment + monthly_property_tax + monthly_insurance

# Display adjusted results
st.write(f"Adjusted Monthly Payment: ${adjusted_total_monthly_payment:,.2f}")

# Cash Flow Summary
st.header("Cash Flow Summary")
annual_cash_flow = total_monthly_payment * 12 - (monthly_expenses * 12)
st.write(f"Annual Cash Flow: ${annual_cash_flow:,.2f}")
if annual_cash_flow > 0:
    st.write("You have a positive cash flow!")
else:
    st.write("You have a negative cash flow. Consider reviewing your expenses.")

# Future Value Over Time Plot
years_future = np.arange(1, 6)  # Next 5 years
future_values = [cost_price * (1 + appreciation_rate) ** year for year in years_future]

st.subheader("Future Value of Investment Over 5 Years")
plt.figure(figsize=(8, 6))
plt.plot(years_future, future_values, marker='o')
plt.title("Future Value of Investment")
plt.xlabel("Years")
plt.ylabel("Future Value ($)")
plt.xticks(years_future)
plt.grid()
st.pyplot(plt)
