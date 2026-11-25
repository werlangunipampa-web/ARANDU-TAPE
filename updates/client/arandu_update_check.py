#!/usr/bin/env python3
"""ARANDU Update: read-only GitHub release discovery. Never downloads or executes."""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

API = "https://api.github.com/repos/werlangunipampa-web/ARANDU-TAPE/releases/latest"
TAG_RE = re.compile(r"^v?[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")
MAX_BYTES = 128 * 1024

def check(timeout=5):
    request = urllib.request.Request(API, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "ARANDU-Update-ReadOnly/0.1",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            if response.status != 200:
                return {"status": "unavailable", "reason": "http_status"}
            length = response.headers.get("Content-Length")
            if length and int(length) > MAX_BYTES:
                return {"status": "unavailable", "reason": "oversize"}
            data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                return {"status": "unavailable", "reason": "oversize"}
    except urllib.error.HTTPError as error:
        if error.code == 404:
            # /releases/latest excludes prereleases. Confirm that the official
            # repository is reachable before treating 404 as an empty stable channel.
            probe = urllib.request.Request(
                "https://api.github.com/repos/werlangunipampa-web/ARANDU-TAPE",
                headers={
                    "Accept": "application/vnd.github+json",
                    "User-Agent": "ARANDU-Update-ReadOnly/0.3",
                    "X-GitHub-Api-Version": "2022-11-28",
                })
            try:
                with urllib.request.urlopen(probe, timeout=timeout) as response:
                    if response.status == 200:
                        return {"status": "no_stable_release"}
            except (urllib.error.URLError, TimeoutError, ValueError, OSError):
                pass
            return {"status": "unavailable", "reason": "release_404_repository_unconfirmed"}
        if error.code in (403, 429):
            return {"status": "unavailable", "reason": "rate_limited_or_forbidden", "http_status": error.code}
        return {"status": "unavailable", "reason": "http_error", "http_status": error.code}
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        return {"status": "unavailable", "reason": "network"}
    try:
        obj = json.loads(data)
        if not isinstance(obj, dict):
            raise ValueError("not an object")
        tag = obj.get("tag_name")
        if obj.get("draft") is not False or obj.get("prerelease") is not False:
            return {"status": "no_stable_release"}
        if not isinstance(tag, str) or not TAG_RE.fullmatch(tag):
            return {"status": "unavailable", "reason": "invalid_tag"}
        url = obj.get("html_url")
        expected = "https://github.com/werlangunipampa-web/ARANDU-TAPE/releases/tag/"
        if not isinstance(url, str) or not url.startswith(expected):
            return {"status": "unavailable", "reason": "invalid_url"}
        return {"status": "stable_release_found", "version": tag, "release_url": url,
                "installation_enabled": False, "package_verified": False}
    except (ValueError, TypeError):
        return {"status": "unavailable", "reason": "invalid_json"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=float, default=5)
    args = parser.parse_args()
    if not 0.5 <= args.timeout <= 15:
        parser.error("timeout must be between 0.5 and 15 seconds")
    result = check(args.timeout)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
