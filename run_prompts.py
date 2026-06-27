"""
Live UI driver: pastes each prompt from prompts_agent1.json into the
NeuralWatt Zero-Cache Tester UI (localhost:3000), clicks Send, and waits
for the request to complete (green DONE banner) before the next one.

Drives the real visible Chrome window via xdotool + clipboard paste, and
detects completion server-side by polling /stats total_requests.
"""
import json
import os
import subprocess
import sys
import time

import requests

DISPLAY = ":1"
BASE = "http://localhost:3000"
# Real X-screen coordinates (calibrated) for the prompt textarea center.
TEXTAREA = (945, 353)
PER_PROMPT_TIMEOUT = 300  # seconds to wait for each completion
ENV = {**os.environ, "DISPLAY": DISPLAY}


def sh(*args):
    return subprocess.run(args, env=ENV, capture_output=True, text=True)


def find_window():
    r = sh("xdotool", "search", "--name", "NeuralWatt")
    ids = [x for x in r.stdout.split() if x.strip()]
    if not ids:
        r = sh("xdotool", "search", "--name", "Neuralwatt")
        ids = [x for x in r.stdout.split() if x.strip()]
    return ids[0] if ids else None


def set_clipboard(text):
    subprocess.run(["xclip", "-selection", "clipboard"],
                   input=text.encode("utf-8"), env=ENV)


def click(wid, x, y):
    sh("xdotool", "windowactivate", "--sync", wid)
    sh("xdotool", "mousemove", "--sync", str(x), str(y))
    sh("xdotool", "click", "1")


def get_count():
    try:
        return requests.get(f"{BASE}/stats", timeout=10).json().get("total_requests", 0)
    except Exception:
        return None


def paste_and_send(wid, prompt):
    # focus + clear textarea
    click(wid, *TEXTAREA)
    time.sleep(0.25)
    sh("xdotool", "key", "--clearmodifiers", "ctrl+a")
    sh("xdotool", "key", "Delete")
    time.sleep(0.1)
    # type the prompt directly into the textarea
    sh("xdotool", "type", "--delay", "6", prompt)
    time.sleep(0.25)
    # Tab moves focus from textarea to the Send button, Space activates it
    sh("xdotool", "key", "Tab")
    time.sleep(0.15)
    sh("xdotool", "key", "space")


def main():
    prompts = json.load(open("prompts_agent1.json"))
    total = len(prompts)
    print(f"Loaded {total} prompts", flush=True)

    wid = find_window()
    if not wid:
        print("ERROR: could not find the NeuralWatt browser window", flush=True)
        sys.exit(1)
    print(f"Driving window id {wid}", flush=True)

    # reset session stats so the live counter starts at 0
    try:
        requests.post(f"{BASE}/reset", timeout=10)
    except Exception as e:
        print(f"WARN reset failed: {e}", flush=True)

    completed = 0
    for i, prompt in enumerate(prompts, start=1):
        baseline = get_count()
        if baseline is None:
            baseline = completed
        target = baseline + 1

        sent_ok = False
        for attempt in (1, 2):
            paste_and_send(wid, prompt)
            deadline = time.time() + PER_PROMPT_TIMEOUT
            while time.time() < deadline:
                c = get_count()
                if c is not None and c >= target:
                    sent_ok = True
                    break
                time.sleep(1.0)
            if sent_ok:
                break
            print(f"  (prompt {i} attempt {attempt} timed out, retrying)", flush=True)

        if sent_ok:
            completed += 1
            # brief beat so the green banner is clearly visible live
            time.sleep(0.6)
            print(f"done {i}/{total}", flush=True)
        else:
            print(f"FAILED {i}/{total} (no completion after retries)", flush=True)

    # final totals
    try:
        s = requests.get(f"{BASE}/stats", timeout=10).json()
        print("=== FINAL ===", flush=True)
        print(json.dumps({
            "total_requests": s.get("total_requests"),
            "total_tokens": s.get("total_tokens"),
            "total_prompt_tokens": s.get("total_prompt_tokens"),
            "total_completion_tokens": s.get("total_completion_tokens"),
        }, indent=2), flush=True)
    except Exception as e:
        print(f"WARN final stats failed: {e}", flush=True)


if __name__ == "__main__":
    main()
