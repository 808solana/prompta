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

## Notes / changelog
- UI refreshed after a GitHub push (commit `added new u2423i`): added the big green done banner + collapsible AI response, stats trimmed to **Total Requests**.
