"""
main.py
--------
WHY THIS FILE EXISTS:
This is the single entry point you (or Docker, or a cron job) run to
start the assistant. It wires the independent pieces together —
Settings, GmailClient, AIProcessor, EmailWorkflow — and runs the polling
loop. Keeping wiring here (not inside the classes themselves) is called
"dependency injection": each class receives what it needs from outside
rather than constructing its own dependencies, which is what makes each
class independently testable.

USAGE:
    python main.py            # runs continuously, polling every N seconds
    python main.py --once     # runs a single pass and exits (good for cron)
"""

import argparse
import sys
import time

from src.ai_processor import AIProcessor
from src.config import load_settings
from src.email_workflow import EmailWorkflow
from src.gmail_client import GmailClient
from src.logger import get_logger


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Email Automation Assistant")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single fetch-analyze-reply pass and exit, instead of looping.",
    )
    args = parser.parse_args()

    try:
        settings = load_settings()
    except EnvironmentError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        sys.exit(1)

    logger = get_logger(__name__, settings.log_level)
    logger.info("Starting AI Email Automation Assistant.")
    logger.info(f"AUTO_SEND_REPLIES={settings.auto_send_replies} | model={settings.openai_model}")

    gmail_client = GmailClient(
        credentials_path=settings.gmail_credentials_path,
        token_path=settings.gmail_token_path,
    )
    ai_processor = AIProcessor(api_key=settings.openai_api_key, model=settings.openai_model)
    workflow = EmailWorkflow(gmail_client, ai_processor, settings)

    if args.once:
        workflow.run_once()
        return

    logger.info(f"Polling every {settings.poll_interval_seconds} seconds. Press Ctrl+C to stop.")
    try:
        while True:
            workflow.run_once()
            time.sleep(settings.poll_interval_seconds)
    except KeyboardInterrupt:
        logger.info("Stopped by user (Ctrl+C). Goodbye.")


if __name__ == "__main__":
    main()
