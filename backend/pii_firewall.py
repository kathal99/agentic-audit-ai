import re
import math

class PIIFirewall:
    """Deep-packet inspection for PII, secrets, and high-entropy exfiltration."""

    def __init__(self):
        self.patterns = {
            "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
            "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
            "API_KEY": r"(?i)(api[_-]?key|secret|token|bearer|private[_-]?key)\s*[:=]\s*['\"]?([A-Za-z0-9_-]{16,})",
            "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "IPV4": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
            "AWS_KEY": r"(?i)AKIA[0-9A-Z]{16}",
        }

    def inspect(self, payload: str) -> dict:
        violations = []
        for rule_name, pattern in self.patterns.items():
            if re.search(pattern, payload):
                violations.append(rule_name)

        entropy_score = self.compute_shannon_entropy(payload)
        is_suspicious_entropy = entropy_score > 4.6 and len(payload) > 24
        return {
            "has_leak": len(violations) > 0 or is_suspicious_entropy,
            "violations": violations,
            "entropy_score": entropy_score,
            "sanitized_payload": self.sanitize(payload),
        }

    def sanitize(self, payload: str) -> str:
        clean = payload
        for rule_name, pattern in self.patterns.items():
            clean = re.sub(pattern, f"[REDACTED_{rule_name}]", clean)
        return clean

    @staticmethod
    def compute_shannon_entropy(data: str) -> float:
        if not data:
            return 0.0
        entropy = 0.0
        for x in set(data):
            p_x = float(data.count(x)) / len(data)
            entropy -= p_x * math.log(p_x, 2)
        return round(entropy, 2)
