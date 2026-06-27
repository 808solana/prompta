# Answer Engine Cost Test — Run Brief

*An ever-evolving doc. Lightweight by design; we'll grow it as things change.*

## The gist
Drive the "answer engine" (the Flask app at `http://localhost:3000`, Neuralwatt `glm-5.2`) through every prompt in `prompta.json` to feel out the API's real, **zero-cache** cost. *"All you really need to focus on is really just entering those prompts."*

## How we run it
- **The slow, faithful way.** Open the UI, paste a prompt, hit **Send Request →**, wait for the answer to fully render, then paste the next one.
- **Strictly sequential** — one at a time, never in parallel.
- **All of them.** 99 prompts in `prompta.json`, in order, start to finish. *"It's gonna be a long time."*
- **Zero caching** — already baked into the app (random nonce + random seed + temperature jitter + no-cache headers), so every call is genuinely fresh.

## The livestream
- **Live Cloud Agent Desktop view only.** *"If I come back to my desk, I can see the live update of it."*
- **Nothing saved.** No screen recording, no screenshots, no fallback log. *"Nothing to fall back off. I am okay with that trade off."*

## When it ends
- Just say **done** and end the livestream. No report, no numbers — *"you don't even have to give me anything."*

## If it breaks
- **Stop everything, ping me, no retries.** *"If you run into an error, just stop everything and just let me know, and we'll just stop from there."*

## Decoration (ignore)
- Cost / energy / token stats and the `$5.00/M` baseline shown in the UI.
- Model stays `glm-5.2` (the "5.5" was a slip).

## Open / evolving
- _(Add new decisions here as we wing it.)_
