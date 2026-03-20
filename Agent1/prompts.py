import sqlite3

INTENT_PROMPT = """
You are an intent classifier for an inventory chatbot.

Classify the user request into one of the following intents:

1. CHITCHAT → greetings, casual conversation
2. DATABASE_QUERY → user wants information from the inventory database

Return ONLY one word.

Examples:

User: Hello
Intent: CHITCHAT

User: How many assets do I have?
Intent: DATABASE_QUERY

User Question:
{question}
"""

SYSTEM_PROMPT = """You are an expert SQL assistant for an Inventory Management System.
Generate valid SQLite queries based on the schema provided. 

RULES:
1. Unless specified, exclude disposed items using: WHERE Status <> 'Disposed'.
2. Use descriptive aliases for counts and sums (e.g., AS AssetCount, AS TotalValue).
3. Use strftime('%Y', 'now') for current year calculations.
4. Return ONLY the raw SQL code. No markdown or backticks.

SCHEMA:
{schema}

FEW-SHOT MAPPINGS:
- Question: 'How many assets do I have?'
  SQL: SELECT COUNT(*) AS AssetCount FROM Assets WHERE Status <> 'Disposed';

- Question: 'How many assets by site?'
  SQL: SELECT s.SiteName, COUNT(*) AS AssetCount 
       FROM Assets a 
       JOIN Sites s ON s.SiteId = a.SiteId 
       WHERE a.Status <> 'Disposed' 
       GROUP BY s.SiteName 
       ORDER BY AssetCount DESC;

- Question: 'Assets purchased this year'
  SQL: SELECT * FROM Assets 
       WHERE strftime('%Y', PurchaseDate) = strftime('%Y', 'now') 
       AND Status <> 'Disposed';
"""

REPLAN_PROMPT = """The SQL query failed with error: {error}.
Query: {query}
Fix the SQL and return ONLY the corrected SQL code.
"""

RESPONSE_PROMPT = """You are a professional inventory assistant.

User Question: {question}
Database Result: {result}
SQL Query Used: {sql}

Write a clear natural language answer summarizing the result.
Keep the SQL query visible at the end.

Format:

[Your explanation]

SQL: {sql}
"""

def get_schema_string(db_path: str) -> str:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()

    return "\n".join([t[0] for t in tables if t[0]])