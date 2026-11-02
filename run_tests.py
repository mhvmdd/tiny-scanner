
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SAMPLES_DIR = ROOT / "test_samples"
MAIN = ROOT / "main.py"
OUTPUT_NAME = "tokens_output.txt"


def parse_tokens(text):
    tokens = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "," not in line:
            continue
        value, ttype = line.split(",", 1)
        value = value.strip()
        ttype = ttype.strip()
        if not value or not ttype:
            continue
        tokens.append((value, ttype.lower()))
    return tokens


def read_file(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def run_sample(sample_file):
    print(f"\nTesting {sample_file.name}...")
    with tempfile.TemporaryDirectory(prefix="tiny-test-") as tmp:
        work = Path(tmp)
        shutil.copyfile(sample_file, work / "input.tiny")
        if not MAIN.exists():
            print("  SKIP: main.py not found")
            return None

        try:
            proc = subprocess.run(
                [sys.executable, str(MAIN), "input.tiny"],
                cwd=work,
                capture_output=True,
                text=True,
                timeout=30,
            )
        except Exception as e:
            print(f"  FAIL: could not run scanner: {e}")
            return False

        out_path = work / OUTPUT_NAME
        out_text = read_file(out_path) if out_path.exists() else ""
        all_out = (proc.stdout or "") + "\n" + (proc.stderr or "") + "\n" + out_text

        exp = sample_file.with_name(sample_file.stem + "_expected.txt")
        errf = sample_file.with_name(sample_file.stem + "_error.txt")

        if exp.exists():
            try:
                expected = parse_tokens(read_file(exp))
                got = parse_tokens(out_text)
                if expected == got:
                    print("  PASS")
                    return True
                else:
                    print("  FAIL: token mismatch")
                    print("  Expected:", expected)
                    print("  Got:", got)
                    return False
            except Exception as e:
                print(f"  FAIL: {e}")
                return False

        if errf.exists():
            frags = []
            for l in read_file(errf).splitlines():
                l = l.strip()
                if l and not l.startswith("#"):
                    frags.append(l.lower())
            if not frags:
                print("  FAIL: no error fragments")
                return False
            if "traceback" in all_out.lower():
                print("  FAIL: scanner crashed")
                return False
            for f in frags:
                if f not in all_out.lower():
                    print(f"  FAIL: missing expected error: {f}")
                    return False
            print("  PASS")
            return True

        print("  FAIL: no _expected.txt or _error.txt found")
        return False


def main():
    print("TINY Scanner - Simple Test")
    print("==========================")
    if not SAMPLES_DIR.exists():
        print("No test_samples folder found.")
        return

    samples = sorted(SAMPLES_DIR.glob("*.tiny"))
    if not samples:
        print("No .tiny files in test_samples.")
        return

    passed = 0
    failed = 0
    skipped = 0

    for s in samples:
        # quick skip if missing companion
        exp = s.with_name(s.stem + "_expected.txt")
        errf = s.with_name(s.stem + "_error.txt")
        if not exp.exists() and not errf.exists():
            print(f"\nSkipping {s.name}: no expected/error file")
            skipped += 1
            continue
        res = run_sample(s)
        if res is None:
            skipped += 1
            continue
        if res:
            passed += 1
        else:
            failed += 1

    print("\n==========================")
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped")
    if failed == 0:
        print("All tests passed!")
    else:
        print("Some tests failed.")


if __name__ == "__main__":
    main()
