Personal Finance Agent 💰

Track: Concierge Agents
Author: Vaishnavi Sambhaji Patil
Course: Agents Intensive - 5-Day AI Agents Course with Google

🎯 Problem Statement

Managing personal finances is challenging for most individuals. People struggle to:

Track daily expenses consistently

Understand their spending patterns

Identify areas where they're overspending

Get actionable recommendations to improve their budget

Manual tracking is time-consuming and error-prone, leading to poor financial decisions and budget overruns.

💡 Solution

The Personal Finance Agent is a multi-agent AI system that automates expense tracking, analysis, and provides personalized budget recommendations. It uses natural language processing to understand expenses described in everyday language and provides instant insights.

Why Agents?

Sequential Processing: Each agent specializes in one task (parse → classify → analyze)

Stateful Operations: Maintains expense history across interactions

Context Awareness: Understands spending patterns over time

Autonomous Decision Making: Automatically categorizes and analyzes without manual intervention

🏗️ Architecture

This system implements a Sequential Multi-Agent Architecture with a FastAPI interface:

          ┌─────────────────────────┐
          │       User Input        │
          │  (Web Frontend / API)  │
          └───────────┬────────────┘
                      │
                      ▼
          ┌─────────────────────────┐
          │       FastAPI API       │
          │  • POST /process_expense│
          └───────────┬────────────┘
                      │
                      ▼
          ┌─────────────────────────┐
          │  Input Parser Agent     │
          │  • Parse text           │
          │  • Extract amount       │
          │  • Extract description  │
          └───────────┬────────────┘
                      │
                      ▼
          ┌─────────────────────────┐
          │ Category Classifier     │
          │ • Classify category     │
          │ • Food / Transport /    │
          │   Entertainment etc.    │
          └───────────┬────────────┘
                      │
                      ▼
          ┌─────────────────────────┐
          │ Budget Analyzer Agent   │
          │ • Aggregate expenses    │
          │ • Calculate totals      │
          │ • Generate insights     │
          └───────────┬────────────┘
                      │
                      ▼
              ┌──────────────┐
              │   Results    │
              │  / Insights  │
              └──────────────┘
                      ▲
                      │
          ┌─────────────────────────┐
          │     Session State       │
          │ • Store all expenses    │
          │ • Track totals          │
          │ • Shared across agents  │
          └─────────────────────────┘

Components

1. InputParserAgent

Parses natural language expense descriptions

Extracts amount, currency, and description

2. CategoryClassifierAgent

Classifies expenses into categories: Food, Transport, Entertainment, Utilities, Shopping, Healthcare, Other

3. BudgetAnalyzerAgent

Aggregates expenses

Calculates totals and category breakdowns

Generates context-aware insights

4. SessionState

Stores all expenses during runtime

Maintains totals and category-level analytics

5. FastAPI API

/process_expense endpoint to send expense text

Returns structured result and summary

🛠️ Features Demonstrated

Multi-Agent System: Sequential agents with specialized roles

Custom Tools: ExpenseParserTool & CategoryClassifierTool

Sessions & State Management: SessionState stores all expenses

Observability: Logging and insights at each agent step

Context Engineering: Cumulative understanding for better recommendations

🚀 Setup & Installation
Prerequisites

Python 3.8 or higher

pip package manager

Installation
# Clone the repository
git clone https://github.com/Vaishnavi212121/personal-finance-agent.git
cd personal-finance-agent

# Install dependencies
pip install -r requirements.txt
pip install fastapi uvicorn

# Run the API
uvicorn server:app --reload --port 8000

📖 Usage
Python API Example
import requests

expense_text = "Spent ₹500 on groceries"
response = requests.post(
    "http://127.0.0.1:8000/process_expense",
    json={"text": expense_text}
)
print(response.json())

Frontend Integration

Open demo.html in a browser

Enter your monthly budget

Add expense using natural language, e.g. "₹350 for lunch at Swiggy"

The frontend calls FastAPI backend and updates:

Expense list

Category totals

Budget progress bar

📊 Sample Output
Input: Spent ₹500 on groceries at DMart
✓ Classified as: Food - ₹500.00

Input: Auto rickshaw ride ₹80
✓ Classified as: Transportation - ₹80.00

Total Expenses Tracked: 2
Total Spending: ₹580.00

Category Breakdown:
  • Food: ₹500.00 (86.2%)
  • Transportation: ₹80.00 (13.8%)

💡 Recommendation:
⚠️ Your Food spending is 86% of total expenses. Consider reducing by 10-15% to balance your budget.

📁 Project Structure
personal-finance-agent/
├── finance_agent.py          # Multi-agent system
├── server.py                 # FastAPI backend
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── demo.html                 # Frontend demo
├── demo.gif                  # Optional animation
└── docs/
    ├── architecture.png      # Architecture diagram
    └── screenshots/          # UI screenshots

🎯 Value Proposition

Time Savings: Eliminates manual expense categorization

Instant Insights: Real-time analysis

Actionable Advice: Personalized recommendations

Easy to Use: Natural language input

Privacy-First: Runs locally, no data sent externally

🔮 Future Enhancements

Integrate LLM (Gemini) for smarter categorization

Connect with banking APIs for automatic expense import

Long-term memory for multi-session persistence

Interactive charts for spending trends

Set and track monthly budget goals

🧪 Testing
# Run tests
python -m pytest tests/

# Run with coverage
pytest --cov=finance_agent tests/

🤝 Contributing

Contributions welcome! Submit a Pull Request.

📄 License

MIT License. See LICENSE file.

📧 Contact

GitHub: @Vaishnavi212121

Email: vaishnavipatil9018@gmail.com

LinkedIn: https://www.linkedin.com/in/vaishnavi-patil-312477259/

Built with ❤️ for the Agents Intensive Capstone Project