import asyncio
import sys
from Agent2.graph import KnowledgeGraphAgent
from logger_config import setup_logger

# --- Windows Async Safeguard ---
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# --- System Safeguards ---
MAX_MESSAGES = 100
MAX_CHARS = 1200

logger = setup_logger()

async def main():
    logger.info("System starting Knowledge Graph AI Agent")

    print("==================================================")
    print("  Knowledge Graph AI Agent ")
    print("==================================================")
    print(f"System: Chat limit is {MAX_MESSAGES} messages. Max {MAX_CHARS} chars per message.")
    print("System: Type 'exit' or 'quit' to shut down.\n")

    # Initialize the LlamaIndex Workflow
    agent = KnowledgeGraphAgent(timeout=120.0)
    message_count = 0
    
    # Initialize the memory list to maintain conversation history
    chat_history = []

    while message_count < MAX_MESSAGES:

        user_input = input("You: ").strip()

        # Exit conditions
        if user_input.lower() in ['exit', 'quit']:
            logger.info("User terminated session manually")
            print("System: Shutting down gracefully. Goodbye!")
            break

        # Empty input check
        if not user_input:
            continue

        # Character limit safeguard
        if len(user_input) > MAX_CHARS:
            logger.warning(f"User input exceeded limit: {len(user_input)} chars")
            print(f"System Error: Message is {len(user_input)} characters. Please keep it under {MAX_CHARS}.")
            continue

        logger.info(f"User Input Received: {user_input}")
        print("Agent is thinking...")

        try:
            # Run the workflow, passing both the input and the chat history
            final_response = await agent.run(user_input=user_input, chat_history=chat_history)

            logger.info(f"Agent Response: {final_response}")
            print(f"\nAgent: {final_response}\n")
            
            # Append the current interaction to the history for the next loop
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": str(final_response)})

        except Exception as e:
            logger.error("Execution error occurred", exc_info=True)
            print(f"\nSystem Error during execution: {e}\n")

        message_count += 1

    if message_count >= MAX_MESSAGES:
        logger.info("Maximum session limit reached")
        print("\nSystem: Maximum conversation limit reached. Goodbye!")

if __name__ == "__main__":
    asyncio.run(main())