"""Telegram Bot API notification delivery."""

from curl_cffi import requests

from .ntfy import fmt_price


def notify(cfg, item):
    """Send one listing to the configured Telegram chat(s).

    telegram_chat_id kan vara ett enda id eller flera kommaseparerade
    id:n om du vill att notiserna ska gå till fler personer samtidigt.
    """

    location = " ".join(
        x
        for x in [
            item["town"],
            f"({item['city']})" if item["city"] else "",
        ]
        if x
    )
    text = "\n".join(
        x
        for x in [
            item["subject"],
            f"{fmt_price(item['price'])} €",
            location,
            item["url"],
        ]
        if x
    )
    endpoint = f"https://api.telegram.org/bot{cfg['telegram_bot_token']}/sendMessage"
    chat_ids = [c.strip() for c in str(cfg["telegram_chat_id"]).split(",") if c.strip()]
    for chat_id in chat_ids:
        response = requests.post(
            endpoint,
            json={"chat_id": chat_id, "text": text},
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        if not payload.get("ok"):
            raise RuntimeError("Telegram rejected the notification request")
