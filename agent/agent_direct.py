"""Strands agent that calls Lambda directly via boto3 — interactive REPL."""
import json
import os
import sys
import boto3
from strands import Agent, tool
from strands.models import BedrockModel

REGION = os.environ.get("AWS_REGION", "us-west-2")
LAMBDA_NAME = os.environ.get("LAMBDA_NAME", "LogisticsQueryOffers")
MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "us.anthropic.claude-sonnet-4-6")

lambda_client = boto3.client("lambda", region_name=REGION)


@tool
def find_logistics_offers(origin: str = None, destination: str = None, max_rate: float = None) -> str:
    """
    Find available shipping/logistics offers between cities.

    Args:
        origin: The origin city (e.g., 'Mombasa', 'Nairobi'). Optional.
        destination: The destination city (e.g., 'Kigali', 'Kampala'). Optional.
        max_rate: Maximum acceptable rate in USD. Optional.

    Returns:
        JSON string listing matching offers with shipper, rate, and transit days.
    """
    payload = {}
    if origin: payload["origin"] = origin
    if destination: payload["destination"] = destination
    if max_rate: payload["max_rate"] = max_rate

    response = lambda_client.invoke(
        FunctionName=LAMBDA_NAME,
        Payload=json.dumps(payload),
    )
    result = json.loads(response["Payload"].read())
    return result.get("body", "{}")


def banner():
    print("=" * 64)
    print("  Logistics Agent — Interactive Mode")
    print(f"  Model:  {MODEL_ID}")
    print(f"  Region: {REGION}")
    print(f"  Lambda: {LAMBDA_NAME}")
    print("=" * 64)
    print("Ask anything about shipping routes, rates, or carriers.")
    print("Commands:  /help   /clear   /history   /exit  (or Ctrl+D)")
    print("Examples:")
    print("  - Are there any routes from Mombasa?")
    print("  - What about Mombasa to Kigali under $2300?")
    print("  - Cheapest route to Kampala?")
    print("-" * 64)


def main():
    model = BedrockModel(model_id=MODEL_ID, region_name=REGION)
    agent = Agent(
        model=model,
        tools=[find_logistics_offers],
        system_prompt=(
            "You are a logistics assistant for carriers. "
            "Use find_logistics_offers for any question about routes, rates, or shippers. "
            "Present results clearly with origin, destination, shipper, rate, and transit days. "
            "If a user gives partial info (only origin, only destination, etc.), still try the lookup "
            "and let them refine. Be concise and friendly."
        ),
    )

    banner()
    turn = 0
    while True:
        try:
            user_input = input("\n› ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye 👋")
            break

        if not user_input:
            continue

        # Slash commands
        if user_input.startswith("/"):
            cmd = user_input.lower()
            if cmd in ("/exit", "/quit", "/q"):
                print("Bye 👋")
                break
            if cmd in ("/help", "/h", "/?"):
                print("Commands:")
                print("  /help     show this help")
                print("  /clear    reset the conversation (forget context)")
                print("  /history  show how many turns so far")
                print("  /exit     leave (or Ctrl+D)")
                continue
            if cmd == "/clear":
                agent = Agent(
                    model=model,
                    tools=[find_logistics_offers],
                    system_prompt=agent.system_prompt,
                )
                turn = 0
                print("✓ Conversation cleared.")
                continue
            if cmd == "/history":
                print(f"Turns so far: {turn}")
                continue
            print(f"Unknown command: {user_input}  (try /help)")
            continue

        turn += 1
        try:
            agent(user_input)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("   (Conversation continues — try again or /clear)")


if __name__ == "__main__":
    main()
