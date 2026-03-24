import streamlit as st
import anthropic
import plotly.graph_objects as go
import os
import re

api_key = os.environ.get('ANTHROPIC_API_KEY')

st.set_page_config(page_title='AI Financial Planning Agent', page_icon='💼', layout='wide')
st.title('💼 Personal Financial Planning Agent')
st.markdown('Enter your financial profile below to receive a personalized plan.')
st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader('Your Profile')
    age = st.number_input('Your Age', min_value=18, max_value=80, value=28)
    annual_income = st.number_input('Annual Income ($)', min_value=0, value=75000, step=5000)
    monthly_expenses = st.number_input('Monthly Expenses ($)', min_value=0, value=3500, step=100)
    current_savings = st.number_input('Current Savings ($)', min_value=0, value=15000, step=1000)
    existing_investments = st.number_input('Existing Investments ($)', min_value=0, value=5000, step=1000)
with col2:
    st.subheader('Goals & Risk')
    risk_tolerance = st.select_slider('Risk Tolerance', options=['Very Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very Aggressive'], value='Moderate')
    time_horizon = st.slider('Investment Time Horizon (years)', 1, 40, 20)
    primary_goal = st.selectbox('Primary Financial Goal', ['Retirement', 'Buy a Home', 'Build Emergency Fund', 'Pay Off Debt', 'Save for Education', 'Grow Wealth'])
    secondary_goal = st.selectbox('Secondary Goal (optional)', ['None', 'Retirement', 'Buy a Home', 'Build Emergency Fund', 'Pay Off Debt', 'Save for Education', 'Grow Wealth'])
    debt_amount = st.number_input('Total Debt ($)', min_value=0, value=0, step=1000)

st.divider()
generate_btn = st.button('Generate My Financial Plan', type='primary', use_container_width=True)

def generate_financial_plan(client_data):
    client = anthropic.Anthropic(api_key=api_key)
    system_prompt = '''You are a Certified Financial Planner (CFP) with 15 years of experience in wealth management.
Always structure your response in exactly these sections:
1. FINANCIAL HEALTH SUMMARY (2-3 sentences)
2. RISK PROFILE ASSESSMENT (explain their risk profile and why it fits)
3. RECOMMENDED PORTFOLIO ALLOCATION (give exact percentages for: US Stocks, International Stocks, Bonds, Real Estate/REITs, Cash)
4. TOP 3 PRIORITY ACTIONS (numbered, specific, actionable steps)
5. GOAL TIMELINE (for each goal mentioned, estimate a realistic timeline)
6. IMPORTANT DISCLOSURES (one paragraph of standard CFP disclosures)
Be specific with numbers. Speak in plain English. Be encouraging but realistic.'''
    user_message = f'''Please create a financial plan for this client:
Age: {client_data['age']}
Annual Income: ${client_data['income']:,}
Monthly Expenses: ${client_data['expenses']:,}
Current Savings: ${client_data['savings']:,}
Existing Investments: ${client_data['investments']:,}
Total Debt: ${client_data['debt']:,}
Risk Tolerance: {client_data['risk']}
Time Horizon: {client_data['horizon']} years
Primary Goal: {client_data['primary_goal']}
Secondary Goal: {client_data['secondary_goal']}
Monthly savings capacity: ${client_data['income']//12 - client_data['expenses']:,}'''
    message = client.messages.create(model='claude-sonnet-4-20250514', max_tokens=1500, messages=[{'role': 'user', 'content': user_message}], system=system_prompt)
    return message.content[0].text

def extract_allocation(plan_text):
    defaults = {'US Stocks': 40, 'International Stocks': 20, 'Bonds': 25, 'Real Estate/REITs': 10, 'Cash': 5}
    allocations = {}
    for label in defaults:
        match = re.search(rf'{re.escape(label)}[:\s]+(\d+)%', plan_text, re.IGNORECASE)
        allocations[label] = int(match.group(1)) if match else defaults[label]
    return allocations

def create_portfolio_chart(allocations):
    colors = ['#1E3A5F', '#2E86AB', '#2A9D8F', '#E9C46A', '#F4A261']
    fig = go.Figure(data=[go.Pie(labels=list(allocations.keys()), values=list(allocations.values()), marker=dict(colors=colors, line=dict(color='white', width=2)), textinfo='label+percent', hole=0.35)])
    fig.update_layout(title='Recommended Portfolio Allocation', showlegend=True, height=400)
    return fig

if generate_btn:
    if not api_key:
        st.error('API key not found! Run: export ANTHROPIC_API_KEY=your_key_here in terminal, then restart the app.')
    else:
        client_data = {'age': age, 'income': annual_income, 'expenses': monthly_expenses, 'savings': current_savings, 'investments': existing_investments, 'debt': debt_amount, 'risk': risk_tolerance, 'horizon': time_horizon, 'primary_goal': primary_goal, 'secondary_goal': secondary_goal}
        with st.spinner('Generating your personalized financial plan...'):
            plan = generate_financial_plan(client_data)
        st.success('Your financial plan is ready!')
        chart_col, plan_col = st.columns([1, 1])
        with chart_col:
            allocations = extract_allocation(plan)
            fig = create_portfolio_chart(allocations)
            st.plotly_chart(fig, use_container_width=True)
        with plan_col:
            st.subheader('Your Personalized Financial Plan')
            st.markdown(plan)

st.divider()
st.caption('Disclaimer: This tool is for educational purposes only and does not constitute financial advice. Please consult a licensed financial advisor.')
