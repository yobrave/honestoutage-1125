"""Outage status line courier: relocate the authored line to the judged zone."""
import json
import os
import pathlib
import sys


class LineService:
    LIMIT = 160
    STAMP = "outg-11252010"

    def __init__(self, home):
        self.home = pathlib.Path(home)
        self.text = ""

    def load(self):
        raw = (self.home / "entry.txt").read_bytes()
        self.text = raw.decode("utf-8").replace("\r", "").strip()
        return self

    def guarded(self):
        if not self.text:
            raise SystemExit("entry text is blank")
        if len(self.text) > self.LIMIT:
            raise SystemExit(f"entry exceeds {self.LIMIT} characters")
        return self.text

    def deliver(self, folder=None):
        zone = pathlib.Path(folder or os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
        zone.mkdir(parents=True, exist_ok=True)
        spot = zone / "entry.txt"
        spot.write_bytes((self.text + "\n").encode("utf-8"))
        return spot


def main(argv):
    home = pathlib.Path(argv[0]).resolve() if argv else pathlib.Path(__file__).resolve().parent
    svc = LineService(home).load()
    kept = svc.guarded()
    spot = svc.deliver()
    echo_back = spot.read_bytes().decode("utf-8").strip()
    if echo_back != kept:
        raise SystemExit("delivered bytes diverge from the guarded line")
    print(json.dumps({"ok": True, "stamp": LineService.STAMP, "chars": len(kept), "spot": str(spot)}))


if __name__ == "__main__":
    main(sys.argv[1:])
