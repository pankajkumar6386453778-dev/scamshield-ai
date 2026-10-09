import ipaddress
import re
from urllib.parse import urlsplit, unquote

SUSPICIOUS_TOKENS = {
    "verify", "urgent", "login", "signin", "account", "secure",
    "update", "claim", "prize", "wallet", "password", "payment"
}

def analyze_url(raw_url: str) -> dict:
    """Analyze URL structure locally; never requests or opens the URL."""
    raw_url = (raw_url or "").strip()
    if not raw_url:
        return {"error": "Enter a URL first."}

    candidate = raw_url if "://" in raw_url else "https://" + raw_url
    try:
        parsed = urlsplit(candidate)
        host = (parsed.hostname or "").lower().rstrip(".")
        # Accessing .port validates malformed port values.
        port = parsed.port
    except ValueError:
        return {"error": "The URL format or port is invalid."}

    if not host or " " in host:
        return {"error": "Could not identify a valid hostname."}

    indicators = []
    score = 0

    if len(raw_url) > 100:
        indicators.append("The URL is unusually long.")
        score += 1

    try:
        ipaddress.ip_address(host)
        indicators.append("The hostname is an IP address rather than a conventional domain.")
        score += 2
    except ValueError:
        pass

    labels = [part for part in host.split(".") if part]
    if len(labels) >= 5:
        indicators.append("The hostname contains many subdomain labels.")
        score += 1

    decoded = unquote((parsed.path or "") + "?" + (parsed.query or "")).lower()
    found_tokens = sorted(token for token in SUSPICIOUS_TOKENS if re.search(rf"\b{re.escape(token)}\b", decoded))
    if found_tokens:
        indicators.append("Suspicious-looking URL words: " + ", ".join(found_tokens) + ".")
        score += 1

    if parsed.scheme.lower() != "https":
        indicators.append("The URL does not use HTTPS. This alone does not prove it is malicious.")
        score += 1

    if "@" in parsed.netloc:
        indicators.append("The URL authority contains '@', which can be used to confuse readers.")
        score += 2

    if port is not None and port not in (80, 443):
        indicators.append(f"The URL uses a non-standard port ({port}).")
        score += 1

    if re.search(r"%[0-9a-fA-F]{2}", raw_url):
        indicators.append("The URL contains percent-encoded characters.")
        score += 1

    level = "Low"
    if score >= 4:
        level = "High"
    elif score >= 2:
        level = "Medium"

    return {
        "host": host,
        "scheme": parsed.scheme.lower(),
        "port": port,
        "indicators": indicators,
        "heuristic_score": score,
        "risk_level": level,
        "error": None,
    }
