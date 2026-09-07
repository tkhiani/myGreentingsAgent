import logging
from datetime import datetime

from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
def get_greeting() -> str:
    """Get an appropriate greeting based on the current time of day.

    Returns:
        A greeting string: 'Good Morning', 'Good Afternoon', 'Good Evening', or 'Good Night'.
    """
    try:
        hour = datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Good Morning"
        elif 12 <= hour < 18:
            greeting = "Good Afternoon"
        elif 18 <= hour < 21:
            greeting = "Good Evening"
        else:
            greeting = "Good Night"
        logger.info("get_greeting: hour=%d, greeting=%s", hour, greeting)
        return greeting
    except Exception as exc:
        logger.error("get_greeting failed: %s", exc)
        return "Hello"
