import uuid
import os
import sys
from Agent1.graph import app


def run_inventory_bot():

    print("================================================")
    print("   🚀 Enterprise Inventory Chatbot (SQL)")
    print("================================================")
    print("Ask about assets, quarterly bills, or say Hello!")
    print("Type 'exit' to quit.\n")

    # Check database
    if not os.path.exists("inventory_chatbot.db"):
        print("Error: Database 'inventory_chatbot.db' not found.")
        print("Please run 'python setup_db.py' first.")
        sys.exit(1)

    # LangGraph memory config
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    while True:

        try:

            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break

            # Initial State
            initial_state = {
                "question": user_input,
                "messages": []
            }

            # Run graph
            final_state = app.invoke(initial_state, config=config)

            # Print final response
            if final_state.get("messages"):
                last_msg = final_state["messages"][-1]
                print(f"\nBot: {last_msg.content}")

            # Show correction attempts
            revs = final_state.get("revision_count", 0)

            if revs > 0:
                print(f"(Self-corrected {revs} time(s))")

            print("-" * 30)

        except KeyboardInterrupt:
            print("\nExiting...")
            break

        except Exception as e:
            print(f"\n[System Error]: {e}")


if __name__ == "__main__":
    run_inventory_bot()