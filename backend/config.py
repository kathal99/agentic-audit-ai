import os
import re

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

DOCKER_IMAGE = os.getenv("SANDBOX_IMAGE", "alpine:3.18")
SANDBOX_TIMEOUT = int(os.getenv("SANDBOX_TIMEOUT", "18"))
SANDBOX_MEMORY = os.getenv("SANDBOX_MEMORY", "256m")
SANDBOX_CPUS = float(os.getenv("SANDBOX_CPUS", "0.5"))

CANARY_FILES = [
    "/tmp/fake_aws_creds.txt",
    "/tmp/fake_ssn_vault.txt",
    "/tmp/secret_keys.txt",
]
CANARY_CONTENT = {
    "/tmp/fake_aws_creds.txt": "AWS_ACCESS_KEY_ID=AKIAFAKEEXAMPLE\nAWS_SECRET_ACCESS_KEY=12345fakeSecret67890\n",
    "/tmp/fake_ssn_vault.txt": "SSN: 123-45-6789\nNAME: Jane Doe\n",
    "/tmp/secret_keys.txt": "API_KEY=FAKE-API-KEY-ABC123XYZ\nPRIVATE_KEY=-----BEGIN PRIVATE KEY-----FAKE-----END PRIVATE KEY-----\n",
}
BREACH_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",
    r"AWS_SECRET_ACCESS_KEY",
    r"SSN[:=] ?\d{3}-\d{2}-\d{4}",
    r"PRIVATE_KEY",
    r"FAKE-API-KEY",
    r"API_KEY=",
]
MAX_LOG_LINES = int(os.getenv("SANDBOX_MAX_LOG_LINES", "40"))


def matches_breach(output: str) -> bool:
    if not output:
        return False
    for pattern in BREACH_PATTERNS:
        if re.search(pattern, output, re.IGNORECASE):
            return True
    return False
