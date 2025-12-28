def create_greeting(name: str) -> str:
    return f"Hello, {name}! Welcome to the world of AI agents !"


def run_agent():
    # Understanding Intent
    user_name = input("What is your name? ")
    # Planning phase
    print("Agent : I should use the create_greeting tool.")
    # Using the tools
    greeting = create_greeting(user_name)
    # Reflect
    if greeting:
        print(f"Agent says: {greeting}")
    else:
        print("Agent: I failed to create a greeting.")

if __name__ == "__main__":
    run_agent()

