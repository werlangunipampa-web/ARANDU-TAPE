#!/usr/bin/env python3
"""Prepare a reproducible, LOCAL review snapshot; never publish or create a tag."""
import argparse
import hashlib
import importlib.util
import io
import json
from pathlib import Path, PurePosixPath
import re
import tarfile

spec = importlib.util.spec_from_file_location("snapshot_audit", Path(__file__).with_name("auditar-snapshot.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

def snapshot(commit):
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Use the complete immutable commit SHA, not a branch.")
    resolved, count, flags, review = audit.scan(commit)
    if resolved != commit or flags:
        raise ValueError("Snapshot blocked by screening; run auditar-snapshot.py for details.")
    rows, contents = [], {}
    for entry in audit.git("ls-tree", "-r", "-z", commit).split(b"\0"):
        if not entry:
            continue
        meta, raw = entry.split(b"\t", 1)
        mode, kind, oid = meta.decode("ascii").split()
        path = raw.decode("utf-8", "strict")
        parts = path.split("/")
        if any(part in ("", ".", "..") for part in parts) or "\\" in path or any(ord(c)<32 or ord(c)==127 for c in path):
            raise ValueError("Unsafe archive path")
        if kind != "blob" or mode not in ("100644", "100755"):
            raise ValueError("Nonregular entry")
        data = audit.git("cat-file", "blob", oid)
        rows.append(dict(path=path, mode=mode, bytes=len(data), git_blob=oid,
                         sha256=hashlib.sha256(data).hexdigest()))
        contents[path] = data
    rows.sort(key=lambda r:r["path"])
    if len(rows)!=count or len(contents)!=count:
        raise ValueError("Tree count mismatch")
    return dict(schema="arandu-source-manifest-v1", commit=commit,
                git_tree=audit.git("rev-parse", commit+"^{tree}").decode().strip(),
                files=rows, file_count=count, research_review=sorted(review),
                status="LOCAL REVIEW ONLY - NOT RELEASE APPROVAL"), contents

def manifest_bytes(manifest):
    return (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True)+"\n").encode("utf-8")

def archive_bytes(manifest, contents):
    buffer=io.BytesIO()
    prefix="ARANDU-TAPE-"+manifest["commit"]
    # Canonical uncompressed tar: sorted names, fixed metadata, immutable blob bytes.
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for row in manifest["files"]:
            data=contents[row["path"]]
            if len(data)!=row["bytes"] or hashlib.sha256(data).hexdigest()!=row["sha256"]:
                raise ValueError("Manifest mismatch")
            entry=tarfile.TarInfo(prefix+"/"+row["path"])
            entry.size=len(data)
            entry.mode=int(row["mode"][-3:],8)
            entry.mtime=entry.uid=entry.gid=0
            entry.uname=entry.gname=""
            tar.addfile(entry,io.BytesIO(data))
    return buffer.getvalue()

def prepare(commit, output):
    manifest,contents=snapshot(commit)
    raw=manifest_bytes(manifest)
    package=archive_bytes(manifest,contents)
    output=Path(output).expanduser()
    # Never overwrite an existing directory. No chmod or writes to source files.
    output.mkdir(mode=0o700,parents=False,exist_ok=False)
    with (output/"manifest.json").open("xb") as stream:
        stream.write(raw)
    with (output/"source-review.tar").open("xb") as stream:
        stream.write(package)
    hashes = (hashlib.sha256(raw).hexdigest()+"  manifest.json\n"+
              hashlib.sha256(package).hexdigest()+"  source-review.tar\n")
    with (output/"SHA256SUMS").open("x",encoding="ascii",newline="\n") as stream:
        stream.write(hashes)
    return manifest

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit",required=True)
    parser.add_argument("--output",help="New local directory; omit to print manifest only")
    args=parser.parse_args()
    try:
        if args.output:
            m=prepare(args.commit,args.output)
            print(f"LOCAL REVIEW ONLY: {m['commit']}, {m['file_count']} files; {len(m['research_review'])} manual research references.")
            print("Do not upload or distribute before rights, disclosure and release approval.")
        else:
            m,_=snapshot(args.commit)
            print(manifest_bytes(m).decode("utf-8"),end="")
    except (ValueError,OSError) as exc:
        parser.exit(2,f"Preparation failed: {exc}\n")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
