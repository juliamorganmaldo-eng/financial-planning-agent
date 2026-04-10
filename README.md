# 💼 AI Personal Financial Planning Agent

An AI-powered financial planning agent built with Python, Streamlit, and the Anthropic Claude API. Simulates a wealth advisor's client discovery process — users input their financial profile and receive a personalized investment plan with portfolio allocation and actionable recommendations.

## Features
- Collects client age, income, savings, goals, and risk tolerance
- Uses Claude AI as the "CFP brain" to generate personalized financial plans
- Outputs structured plan with risk assessment, goal timelines, and priority actions
- Visualizes portfolio allocation as an interactive Plotly pie chart

## Tech Stack
- Python
- Streamlit
- Anthropic Claude API
- Plotly
- python-dotenv

## How to Run Locally

1. Clone the repo:
   git clone https://github.com/juliamorganmaldo-eng/financial-planning-agent.git

2. Create a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies:
   pip install anthropic streamlit plotly python-dotenv fpdf2

4. Add your API key — create a .env file:
   ANTHROPIC_API_KEY=your_key_here

5. Run the app:
   streamlit run app.py

## Disclaimer
This tool is for educational purposes only and does not constitute financial advice.
