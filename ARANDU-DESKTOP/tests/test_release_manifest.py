"""Offline tests for deterministic source review packages."""
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("prepare_snapshot", ROOT/"scripts"/"preparar-snapshot.py")
prepare=importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)

class ReviewSnapshot(unittest.TestCase):
    def test_current_commit_reproducibility(self):
        sha=prepare.audit.git("rev-parse","HEAD").decode().strip()
        manifest,contents=prepare.snapshot(sha)
        self.assertEqual(manifest["file_count"],len(contents))
        self.assertEqual(manifest["commit"],sha)
        self.assertEqual(manifest["git_tree"],prepare.audit.git("rev-parse",sha+"^{tree}").decode().strip())
        self.assertEqual(prepare.manifest_bytes(manifest),prepare.manifest_bytes(prepare.snapshot(sha)[0]))
        blob=prepare.archive_bytes(manifest,contents)
        self.assertEqual(blob,prepare.archive_bytes(manifest,contents))
        with tarfile.open(fileobj=io.BytesIO(blob),mode="r:") as archive:
            members=archive.getmembers()
            self.assertEqual(len(members),manifest["file_count"])
            for member,row in zip(members,manifest["files"]):
                self.assertTrue(member.isfile())
                self.assertEqual(member.name,"ARANDU-TAPE-"+sha+"/"+row["path"])
                self.assertEqual(member.mtime,0)
                self.assertEqual(member.mode,int(row["mode"][-3:],8))
                self.assertEqual(hashlib.sha256(archive.extractfile(member).read()).hexdigest(),row["sha256"])

    def test_no_overwrite_and_checksum(self):
        sha=prepare.audit.git("rev-parse","HEAD").decode().strip()
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/"review"
            prepare.prepare(sha,target)
            before=(target/"manifest.json").read_bytes()
            with self.assertRaises(FileExistsError):
                prepare.prepare(sha,target)
            self.assertEqual(before,(target/"manifest.json").read_bytes())
            for line in (target/"SHA256SUMS").read_text().splitlines():
                digest,name=line.split("  ")
                self.assertEqual(digest,hashlib.sha256((target/name).read_bytes()).hexdigest())
            self.assertEqual(json.loads(before)["commit"],sha)

    def test_reject_moving_refs(self):
        for ref in ("HEAD","main","abc123","--all"):
            with self.assertRaises(ValueError):
                prepare.snapshot(ref)

    def test_only_committed_content_and_block_sensitive_tree(self):
        previous=Path.cwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                def git(*args):
                    return subprocess.check_output(["git",*args],stderr=subprocess.DEVNULL).decode().strip()
                git("init","-q")
                git("config","user.name","Synthetic Test")
                git("config","user.email","synthetic@example.invalid")
                Path("demo.txt").write_text("committed")
                git("add","demo.txt")
                git("commit","-qm","fixture")
                sha=git("rev-parse","HEAD")
                Path("demo.txt").write_text("uncommitted")
                Path("not-tracked.txt").write_text("excluded")
                m,data=prepare.snapshot(sha)
                self.assertEqual(data,{"demo.txt":b"committed"})
                self.assertEqual(m["file_count"],1)
                Path(".env").write_text("synthetic")
                git("add",".env")
                git("commit","-qm","blocked fixture")
                with self.assertRaises(ValueError):
                    prepare.snapshot(git("rev-parse","HEAD"))
            finally:
                os.chdir(previous)

if __name__=="__main__":
    unittest.main()
