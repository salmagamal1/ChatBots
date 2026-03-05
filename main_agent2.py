import asyncio
from Agent2.graph import KnowledgeGraphAgent
from logger_config import setup_logger

# --- System Safeguards ---
MAX_MESSAGES = 10
MAX_CHARS = 200

logger = setup_logger()

async def main():
    logger.info("System starting Knowledge Graph AI Agent")

    print("==================================================")
    print("  Knowledge Graph AI Agent ")
    print("==================================================")
    print(f"System: Chat limit is {MAX_MESSAGES} messages. Max {MAX_CHARS} chars per message.")
    print("System: Type 'exit' or 'quit' to shut down.\n")

    # agent = KnowledgeGraphAgent()
    agent = KnowledgeGraphAgent(timeout=120.0)
    message_count = 0

    while message_count < MAX_MESSAGES:

        user_input = input("You: ").strip()

        if user_input.lower() in ['exit', 'quit']:
            logger.info("User terminated session manually")
            print("System: Shutting down gracefully. Goodbye!")
            break

        if not user_input:
            continue

        if len(user_input) > MAX_CHARS:
            logger.warning(f"User input exceeded limit: {len(user_input)} chars")
            print(f"System Error: Message is {len(user_input)} characters. Please keep it under {MAX_CHARS}.")
            continue

        logger.info(f"User Input Received: {user_input}")

        print("Agent is thinking...")

        try:
            final_response = await agent.run(user_input=user_input)

            logger.info(f"Agent Response: {final_response}")
            print(f"\nAgent: {final_response}\n")

        except Exception as e:
            logger.error("Execution error occurred", exc_info=True)
            print(f"\nSystem Error during execution: {e}\n")

        message_count += 1

    if message_count >= MAX_MESSAGES:
        logger.info("Maximum session limit reached")
        print("\nSystem: Maximum conversation limit reached. Goodbye!")

if __name__ == "__main__":
    asyncio.run(main())


