import re
import math


def analyse(pw: str) -> dict:
    """
    Analyse a password and return a dict with:
      - score    : int 0-5
      - entropy  : float (bits)
      - tips     : list[str]  improvement suggestions
      - checks   : list[tuple(str, bool)]  requirement results
      - length   : int
    """
    length     = len(pw)
    has_upper  = bool(re.search(r"[A-Z]", pw))
    has_lower  = bool(re.search(r"[a-z]", pw))
    has_digit  = bool(re.search(r"\d",    pw))
    has_symbol = bool(re.search(r"[^A-Za-z0-9]", pw))

    # Entropy calculation
    pool = (
        (26 if has_lower  else 0) +
        (26 if has_upper  else 0) +
        (10 if has_digit  else 0) +
        (32 if has_symbol else 0)
    )
    entropy = round(length * math.log2(pool), 1) if pool and length else 0.0

    # Strength score (0–5)
    score = 0
    if length >= 8:               score += 1
    if length >= 12:              score += 1
    if has_upper and has_lower:   score += 1
    if has_digit:                 score += 1
    if has_symbol:                score += 1
    score = min(score, 5)

    # Improvement tips
    if length == 0:
        tips = ["Start typing to check your password..."]
    else:
        tips = []
        if length < 8:                    tips.append("Use at least 8 characters")
        if not (has_upper and has_lower): tips.append("Mix uppercase & lowercase letters")
        if not has_digit:                 tips.append("Add numbers (0-9)")
        if not has_symbol:                tips.append("Include symbols (!@#$%...)")
        if length < 12:                   tips.append("Aim for 12+ characters")
        if not tips:                      tips = ["Excellent! Your password looks great."]

    # Requirement checklist
    checks = [
        ("8+ characters",    length >= 8),
        ("12+ characters",   length >= 12),
        ("Uppercase (A-Z)",  has_upper),
        ("Lowercase (a-z)",  has_lower),
        ("Numbers (0-9)",    has_digit),
        ("Symbols (!@#...)", has_symbol),
    ]

    return dict(score=score, entropy=entropy, tips=tips, checks=checks, length=length)
