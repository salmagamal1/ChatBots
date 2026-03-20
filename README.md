# Enterprise Dual-Agent Chatbot System

An intelligent, multi-agent conversational system designed to interact with enterprise data. This project features two specialized AI agents: a LangGraph-powered SQL chatbot for precise inventory management, and a LlamaIndex-powered Knowledge Graph agent for complex, unstructured data queries using Neo4j.

## 🚀 Key Features

* **Agent 1: SQL Inventory Bot (LangGraph)**
    * Translates natural language into accurate SQL queries.
    * Directly interfaces with a localized SQLite database (`inventory_chatbot.db`) to manage enterprise assets, purchase orders, locations, and billing.
    * Features self-correction and revision logic to ensure query accuracy before returning results to the user.
* **Agent 2: Knowledge Graph Agent (LlamaIndex)**
    * Processes complex user intent (mapping to general, inquire, edit, or delete actions).
    * Generates and executes Cypher queries against a Neo4j graph database.
    * Synthesizes raw graph data into natural, contextual, human-readable responses.
* **Secure & Scalable**
    * Environment variables managed safely via `.dotenv`.
    * Optimized dependency management for clean deployments.
    * Centralized logging system (`logs/agent.log`) for monitoring workflow execution.

## 🛠️ Technology Stack

* **Core Logic:** Python 3, LangGraph, LlamaIndex
* **Databases:** SQLite (Structured Inventory), Neo4j (Knowledge Graph)
* **LLM Integration:** Langchain (Groq)

## ⚙️ Local Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.org/salmagamal1/ChatBots.git](https://github.org/salmagamal1/ChatBots.git)
   cd ChatBots
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your API keys and database credentials. *(Note: This file is ignored by git for security).*
   ```env
   GROQ_API_KEY=your_groq_key
   NEO4J_URI=your_neo4j_uri
   NEO4J_USERNAME=your_username
   NEO4J_PASSWORD=your_password
   ```

5. **Initialize the SQLite Database:**
   ```bash
   python setup_db.py
   ```

## 🎮 Running the Agents

**To launch the Inventory SQL Chatbot:**
```bash
python main_agent1.py
```
*Example query: "What is the status of purchase order PO-5001?"*

**To launch the Knowledge Graph Agent:**
```bash
python main_agent2.py
```
*Example query: "Show me the relationship dependencies for our current projects."*

## 🗄️ Project Structure

* `/Agent1`: Contains LangGraph state, nodes, and prompt logic for the SQL inventory bot.
* `/Agent2`: Contains LlamaIndex workflow, Cypher generation, and response synthesis logic.
* `setup_db.py`: Schema creation and data seeding for the local SQLite database.
* `logger_config.py`: Centralized logging configuration for system monitoring.
* `LangIndex & neo4j.txt`: Architecture outline for the intent-driven Knowledge Graph workflow.

