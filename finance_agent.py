"""
Personal Finance Agent - Multi-Agent System
Capstone Project for Agents Intensive Course

This agent demonstrates:
1. Multi-agent architecture (3 sequential agents)
2. Custom tools (ExpenseParser, CategoryClassifier)
3. Session & state management
4. Observability (comprehensive logging)
5. Context engineering (cumulative analysis)
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


# ==================== COURSE CONCEPT 1: CUSTOM TOOLS ====================

class ExpenseParserTool:
    """
    Custom Tool: Parses natural language expense input
    Extracts: amount, currency, description
    """
    
    def __init__(self):
        self.name = "expense_parser"
        self.description = "Parses natural language expense input and extracts structured data"
    
    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parse expense from natural language
        Examples:
        - "Spent ₹500 on groceries"
        - "$45 for lunch at restaurant"
        - "Auto rickshaw ₹80"
        """
        # Extract amount with currency
        rupee_match = re.search(r'₹\s*(\d+(?:\.\d{2})?)', text)
        dollar_match = re.search(r'\$\s*(\d+(?:\.\d{2})?)', text)
        
        amount = 0
        currency = '₹'  # Default to Rupees
        
        if rupee_match:
            amount = float(rupee_match.group(1))
            currency = '₹'
        elif dollar_match:
            amount = float(dollar_match.group(1))
            currency = '$'
        else:
            # Try to find any number
            number_match = re.search(r'(\d+(?:\.\d{2})?)', text)
            if number_match:
                amount = float(number_match.group(1))
        
        return {
            'amount': amount,
            'currency': currency,
            'description': text,
            'raw_input': text,
            'parsed_at': datetime.now().isoformat()
        }


class CategoryClassifierTool:
    """
    Custom Tool: Classifies expenses into categories
    Uses keyword matching with predefined patterns
    """
    
    def __init__(self):
        self.name = "category_classifier"
        self.description = "Classifies expenses into categories based on keywords"
        
        # Category keywords database
        self.categories = {
            'food': ['grocery', 'groceries', 'restaurant', 'cafe', 'coffee', 
                    'lunch', 'dinner', 'breakfast', 'food', 'meal', 'eating',
                    'dmart', 'reliance', 'bigbasket', 'swiggy', 'zomato',
                    'biryani', 'chai', 'tea', 'snack'],
            'transportation': ['uber', 'lyft', 'gas', 'fuel', 'parking', 'taxi',
                             'metro', 'bus', 'train', 'travel', 'trip', 'flight',
                             'car', 'vehicle', 'commute', 'auto', 'rickshaw',
                             'ola', 'rapido', 'petrol', 'diesel'],
            'entertainment': ['movie', 'cinema', 'netflix', 'spotify', 'game',
                            'concert', 'theater', 'fun', 'entertainment',
                            'hotstar', 'prime', 'pvr', 'inox', 'gaming'],
            'utilities': ['electric', 'electricity', 'water', 'internet', 'phone',
                         'mobile', 'bill', 'utility', 'broadband', 'wifi',
                         'jio', 'airtel', 'vi', 'bsnl', 'gas', 'lpg'],
            'shopping': ['amazon', 'mall', 'store', 'shop', 'clothing', 'clothes',
                        'purchase', 'bought', 'flipkart', 'myntra', 'ajio', 'meesho',
                        'shopping', 'shirt', 'shoes'],
            'healthcare': ['doctor', 'pharmacy', 'medicine', 'hospital', 'clinic',
                          'medical', 'health', 'apollo', 'fortis', 'prescription'],
            'other': []
        }
    
    def classify(self, description: str) -> str:
        """
        Classify expense based on keywords in description
        Returns category name
        """
        description_lower = description.lower()
        
        for category, keywords in self.categories.items():
            if any(keyword in description_lower for keyword in keywords):
                return category
        
        return 'other'


# ==================== COURSE CONCEPT 2: STATE MANAGEMENT ====================

@dataclass
class Expense:
    """Data model for an expense"""
    id: str
    amount: float
    currency: str
    description: str
    category: str
    timestamp: str
    raw_input: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


class SessionState:
    """
    Session & State Management
    Tracks all expenses and provides cumulative analysis
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.expenses: List[Expense] = []
        self.created_at = datetime.now().isoformat()
    
    def add_expense(self, expense: Expense):
        """Add expense to session state"""
        self.expenses.append(expense)
    
    def get_total(self) -> float:
        """Get total spending"""
        return sum(e.amount for e in self.expenses)
    
    def get_category_totals(self) -> Dict[str, float]:
        """Get spending by category"""
        totals = {}
        for expense in self.expenses:
            category = expense.category
            totals[category] = totals.get(category, 0) + expense.amount
        return totals
    
    def get_expense_count(self) -> int:
        """Get number of expenses"""
        return len(self.expenses)
    
    def to_dict(self) -> Dict:
        """Serialize state"""
        return {
            'session_id': self.session_id,
            'created_at': self.created_at,
            'expense_count': self.get_expense_count(),
            'total_spending': self.get_total(),
            'expenses': [e.to_dict() for e in self.expenses]
        }


# ==================== COURSE CONCEPT 3: OBSERVABILITY ====================

class AgentLogger:
    """
    Observability: Comprehensive logging system
    Tracks agent execution, decisions, and results
    """
    
    def __init__(self):
        self.logs: List[Dict] = []
    
    def log(self, agent_name: str, event_type: str, message: str, data: Optional[Dict] = None):
        """Log an event"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'agent': agent_name,
            'event_type': event_type,
            'message': message,
            'data': data or {}
        }
        self.logs.append(log_entry)
        
        # Print to console for visibility
        emoji = self._get_emoji(event_type)
        print(f"{emoji} [{agent_name}] {message}")
        if data:
            print(f"   Data: {json.dumps(data, indent=2)}")
    
    def _get_emoji(self, event_type: str) -> str:
        """Get emoji for event type"""
        emojis = {
            'start': '🚀',
            'processing': '⚙️',
            'success': '✅',
            'error': '❌',
            'info': 'ℹ️',
            'warning': '⚠️'
        }
        return emojis.get(event_type, '📝')
    
    def get_logs(self) -> List[Dict]:
        """Get all logs"""
        return self.logs


# ==================== COURSE CONCEPT 4: MULTI-AGENT SYSTEM ====================

class Agent:
    """Base Agent class"""
    
    def __init__(self, name: str, logger: AgentLogger):
        self.name = name
        self.logger = logger
    
    def execute(self, input_data: Any) -> Any:
        """Execute agent logic - to be overridden"""
        raise NotImplementedError


class InputParserAgent(Agent):
    """
    Agent 1: Parses natural language input into structured data
    Uses: ExpenseParserTool
    """
    
    def __init__(self, logger: AgentLogger):
        super().__init__("InputParserAgent", logger)
        self.tool = ExpenseParserTool()
    
    def execute(self, raw_input: str) -> Dict[str, Any]:
        """Parse expense from natural language"""
        self.logger.log(self.name, 'start', f'Parsing input: {raw_input}')
        
        try:
            parsed_data = self.tool.parse(raw_input)
            self.logger.log(self.name, 'success', 'Successfully parsed expense', parsed_data)
            return parsed_data
        except Exception as e:
            self.logger.log(self.name, 'error', f'Failed to parse: {str(e)}')
            raise


class CategoryClassifierAgent(Agent):
    """
    Agent 2: Classifies expenses into categories
    Uses: CategoryClassifierTool
    """
    
    def __init__(self, logger: AgentLogger):
        super().__init__("CategoryClassifierAgent", logger)
        self.tool = CategoryClassifierTool()
    
    def execute(self, parsed_expense: Dict[str, Any]) -> Dict[str, Any]:
        """Classify expense category"""
        description = parsed_expense['description']
        self.logger.log(self.name, 'start', f'Classifying: {description}')
        
        try:
            category = self.tool.classify(description)
            parsed_expense['category'] = category
            self.logger.log(self.name, 'success', f'Classified as: {category}', 
                          {'category': category})
            return parsed_expense
        except Exception as e:
            self.logger.log(self.name, 'error', f'Classification failed: {str(e)}')
            raise


class BudgetAnalyzerAgent(Agent):
    """
    Agent 3: Analyzes spending patterns and provides insights
    Uses: Session state for cumulative analysis
    """
    
    def __init__(self, logger: AgentLogger, session_state: SessionState):
        super().__init__("BudgetAnalyzerAgent", logger)
        self.session_state = session_state
    
    def execute(self, classified_expense: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze expense in context of overall budget"""
        self.logger.log(self.name, 'start', 'Analyzing budget impact')
        
        try:
            # Create expense object
            expense = Expense(
                id=f"exp_{len(self.session_state.expenses) + 1}",
                amount=classified_expense['amount'],
                currency=classified_expense['currency'],
                description=classified_expense['description'],
                category=classified_expense['category'],
                timestamp=classified_expense['parsed_at'],
                raw_input=classified_expense['raw_input']
            )
            
            # Add to session
            self.session_state.add_expense(expense)
            
            # Generate insights
            insights = self._generate_insights()
            
            result = {
                'expense': expense.to_dict(),
                'insights': insights
            }
            
            self.logger.log(self.name, 'success', 'Analysis complete', insights)
            return result
            
        except Exception as e:
            self.logger.log(self.name, 'error', f'Analysis failed: {str(e)}')
            raise
    
    def _generate_insights(self) -> Dict[str, Any]:
        """Generate spending insights"""
        total = self.session_state.get_total()
        category_totals = self.session_state.get_category_totals()
        expense_count = self.session_state.get_expense_count()
        
        # Find highest spending category
        if category_totals:
            top_category = max(category_totals.items(), key=lambda x: x[1])
        else:
            top_category = ('none', 0)
        
        return {
            'total_spending': total,
            'expense_count': expense_count,
            'category_breakdown': category_totals,
            'top_category': {
                'name': top_category[0],
                'amount': top_category[1]
            }
        }


# ==================== COURSE CONCEPT 5: AGENT ORCHESTRATION ====================

class PersonalFinanceAgentSystem:
    """
    Multi-Agent Orchestrator
    Coordinates sequential execution of agents:
    Input Parser → Category Classifier → Budget Analyzer
    """
    
    def __init__(self):
        self.logger = AgentLogger()
        self.session_state = SessionState(session_id=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        # Initialize agents
        self.parser_agent = InputParserAgent(self.logger)
        self.classifier_agent = CategoryClassifierAgent(self.logger)
        self.analyzer_agent = BudgetAnalyzerAgent(self.logger, self.session_state)
    
    def process_expense(self, raw_input: str) -> Dict[str, Any]:
        """
        Process expense through multi-agent pipeline
        Sequential execution with context passing
        """
        print("\n" + "="*60)
        print(f"Processing: {raw_input}")
        print("="*60)
        
        try:
            # Agent 1: Parse input
            parsed_data = self.parser_agent.execute(raw_input)
            
            # Agent 2: Classify category
            classified_data = self.classifier_agent.execute(parsed_data)
            
            # Agent 3: Analyze budget impact
            final_result = self.analyzer_agent.execute(classified_data)
            
            return final_result
            
        except Exception as e:
            self.logger.log("System", 'error', f"Pipeline failed: {str(e)}")
            raise
    
    def get_summary(self) -> Dict[str, Any]:
        """Get overall spending summary"""
        return {
            'session_info': {
                'session_id': self.session_state.session_id,
                'created_at': self.session_state.created_at
            },
            'statistics': {
                'total_expenses': self.session_state.get_expense_count(),
                'total_spending': self.session_state.get_total(),
                'category_breakdown': self.session_state.get_category_totals()
            },
            'all_expenses': [e.to_dict() for e in self.session_state.expenses]
        }


# ==================== DEMO ====================

def run_demo():
    """Run demonstration of the Personal Finance Agent"""
    
    print("\n" + "="*60)
    print("🤖 PERSONAL FINANCE AGENT - Multi-Agent System Demo")
    print("="*60)
    
    # Initialize system
    agent_system = PersonalFinanceAgentSystem()
    
    # Sample expenses
    sample_expenses = [
        "Spent ₹500 on groceries at DMart",
        "Auto rickshaw ride ₹80",
        "Swiggy order ₹350 for dinner",
        "Netflix subscription ₹649",
        "Ola cab to office ₹250",
        "$45 for lunch at restaurant",
        "Flipkart shopping ₹1200 for clothes"
    ]
    
    print("\n📝 Processing sample expenses...\n")
    
    # Process each expense
    for expense_text in sample_expenses:
        result = agent_system.process_expense(expense_text)
        print(f"\n✅ Processed: {expense_text}")
        print(f"   Category: {result['expense']['category']}")
        print(f"   Amount: {result['expense']['currency']}{result['expense']['amount']}")
    
    # Get summary
    print("\n" + "="*60)
    print("📊 SPENDING SUMMARY")
    print("="*60)
    
    summary = agent_system.get_summary()
    stats = summary['statistics']
    
    print(f"\n💰 Total Spending: ₹{stats['total_spending']:.2f}")
    print(f"📝 Total Expenses: {stats['total_expenses']}")
    print(f"\n📊 Category Breakdown:")
    for category, amount in stats['category_breakdown'].items():
        print(f"   {category.capitalize()}: ₹{amount:.2f}")
    
    print("\n" + "="*60)
    print("✅ Demo Complete!")
    print("="*60)

    print("\n")


if __name__ == "__main__":
    run_demo()