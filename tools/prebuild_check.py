"""Checks run by build.bat before building, so a release can't ship half-configured."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import config  # noqa: E402

problems = []

url = getattr(config, "LICENSE_SERVER_URL", "")
key = getattr(config, "LICENSE_PUBLIC_KEY", "")
if not url.startswith("https://"):
    problems.append("config.py: set LICENSE_SERVER_URL to your website, e.g. https://www.yourdomain.in")
if not re.fullmatch(r"[0-9a-f]{64}", key or ""):
    problems.append("config.py: set LICENSE_PUBLIC_KEY (copy it from your website's Admin > Releases page)")

iss = (ROOT / "setup.iss").read_text(encoding="utf-8")
match = re.search(r'#define MyAppVersion "([^"]+)"', iss)
if not match or match.group(1) != config.APP_VERSION:
    problems.append(
        f"Version mismatch: config.py APP_VERSION is {config.APP_VERSION} but setup.iss MyAppVersion is "
        f"{match.group(1) if match else 'missing'}. Make them the same."
    )

if problems:
    print("Not ready to build:")
    for problem in problems:
        print("  - " + problem)
    sys.exit(1)

print(f"Building version {config.APP_VERSION} for {url}")
