# Neuralwatt Zero-Cache Tester — Project Notes

*A living doc. Short on purpose. Captures the gold as we go.*

## What this is
A Flask + browser UI (`neuralwatt_test.py`, port 3000) that fires prompts at the Neuralwatt **GLM-5.2** API with **zero caching** — fresh context, random nonce, random seed, temperature jitter, no-cache headers — so every request does real work.

## The point
> "This is just to see how much tokens I can use."

Run the prompt set through the tool and watch the token usage climb. Worst-case by design (no caching).

## The run (how we do it)
- Source of prompts: `prompts_agent1.json` in the repo — **100 prompts**, all heavy "build a complete implementation of X" asks.
- Rhythm: **copy → paste → enter → wait for the green button → repeat**, *"like a human."*
- The cue: the pulsing green **"DONE — READY FOR THE NEXT PROMPT"** banner. When it shows, send the next.
- After each prompt, response is: just **"done."** Nothing more, nothing less.
- **Done = all 100 prompts run.**

## Watching
> "I am on the other end watching."

Live only. **No capture, no video, no recording** — it's a livestream.

## Run mechanics / learnings (the gold)
- **Drive the live UI, not the API directly** — the live view is the show. Type the prompt into the textarea, then **`Tab` → `Space`** to hit Send (there is no Enter-to-send). Calibrated real X-screen textarea center: **`(945, 353)`** on display `:1`.
- **One request at a time. Never stack.** The Neuralwatt account allows only **5 concurrent slots** for `GLM-5.2-FP8`; firing a second request before the first returns burns slots and triggers `429 concurrent_budget_exceeded`. The driver sends one prompt, waits for the `/stats` request counter to tick up (= green banner), *then* sends the next.
- **No `max_tokens` = big, slow responses.** Each "build a complete implementation" prompt generates **~8–12k tokens** and holds a slot for **~3–4 minutes**. Worst-case by design — exactly the point ("see how much tokens I can use"). All 100 ≈ many hours and ~1M tokens.
- Completion is detected server-side by polling `/stats` `total_requests`; `/reset` zeroes the session so the live counter climbs 0 → 100.

## Notes / changelog
- UI refreshed after a GitHub push (commit `added new u2423i`): added the big green done banner + collapsible AI response, stats trimmed to **Total Requests**.
- Built `run_prompts.py` to drive the live UI through all 100 prompts (sequential, completion-gated).
