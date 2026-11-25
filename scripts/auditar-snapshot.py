#!/usr/bin/env python3
"""Read-only release snapshot triage. Never publishes or prints matched secrets."""
import argparse
import re
import subprocess
from pathlib import PurePosixPath

PATTERNS = {
    "private-key": rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----",
    "github-token": rb"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})",
    "openai-style-key": rb"sk-(?:proj-)?[A-Za-z0-9_-]{30,}",
    "google-api-key": rb"AIza[0-9A-Za-z_-]{35}",
    "aws-access-key": rb"(?:AKIA|ASIA)[0-9A-Z]{16}",
}
RESEARCH = re.compile(rb"ARANDU-[A-Za-z0-9_-]+-PRIVATE|SeedHome|eca_experiments|eca_bridge|ECA Lab", re.I)
MAX_BLOB = 5 * 1024 * 1024

def git(*args):
    return subprocess.check_output(["git", *args], stderr=subprocess.PIPE)

def inspect_path(path):
    p = PurePosixPath(path)
    low = [part.lower() for part in p.parts]
    if any(part.endswith("-private") or part in {".ssh", ".gnupg", "backups", "seedhome"} for part in low):
        return "restricted-path"
    if p.name.lower() in {".env", "id_rsa", "id_ed25519", "credentials.json", "secrets.json"} or p.name.lower().startswith(".env."):
        return "credential-path"
    if p.suffix.lower() in {".pem", ".key", ".p12", ".pfx", ".sqlite", ".sqlite3", ".db", ".zip", ".gz", ".7z"}:
        return "opaque-or-sensitive-path"
    return None

def inspect_bytes(data):
    return [name for name, pattern in PATTERNS.items() if re.search(pattern, data)]

def scan(ref):
    commit = git("rev-parse", "--verify", ref + "^{commit}").decode().strip()
    entries = git("ls-tree", "-r", "-z", commit).split(b"\0")
    count = 0
    flags = []
    review = []
    for entry in entries:
        if not entry:
            continue
        meta, name = entry.split(b"\t", 1)
        mode, kind, oid = meta.decode("ascii").split()
        path = name.decode("utf-8", "backslashreplace")
        count += 1
        issue = inspect_path(path)
        if issue:
            flags.append((path, issue))
        if kind != "blob" or mode not in ("100644", "100755"):
            flags.append((path, "non-regular-entry"))
            continue
        size = int(git("cat-file", "-s", oid))
        if size > MAX_BLOB:
            flags.append((path, "oversize-unreviewed"))
            continue
        data = git("cat-file", "blob", oid)
        if b"\0" in data:
            flags.append((path, "binary-review-required"))
        if data.startswith(b"version https://git-lfs.github.com/spec/v1"):
            flags.append((path, "unresolved-lfs-pointer"))
        flags.extend((path, tag) for tag in inspect_bytes(data))
        if RESEARCH.search(data):
            review.append(path)
    return commit, count, flags, review

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="HEAD", help="Git commit or ref in local repository")
    args = parser.parse_args()
    commit, count, flags, review = scan(args.ref)
    print(f"Snapshot: {commit}; entries examined: {count}")
    for path, tag in flags:
        print(f"BLOCK: {tag}: {path!r}")
    for path in review:
        print(f"MANUAL RESEARCH REVIEW: {path!r}")
    print(f"Blocking indicators: {len(flags)}; research references: {len(review)}")
    print("Screening only: no license, ownership, historical-secret or release approval.")
    return int(bool(flags))

if __name__ == "__main__":
    raise SystemExit(main())
