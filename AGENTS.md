# AGENTS.md

## Cursor Cloud specific instructions

### What this is
Single-file Python/Flask web app: `neuralwatt_test.py` ("Neuralwatt Zero-Cache Tester"). It serves a dark-themed UI at `http://localhost:3000` and proxies prompts to the external Neuralwatt API (`https://api.neuralwatt.com/v1`, model `glm-5.2`) to measure per-request energy/cost. `prompta.json` is just a dataset of sample prompts (not loaded by the app).

### Run
- `python3 neuralwatt_test.py` (Flask dev server with `debug=True` on port `3000`).
- Routes: `GET /` (UI), `POST /chat` (inference), `GET /stats` (JSON), `POST /reset`.
- Quick smoke test without the browser:
  `curl -s -X POST http://localhost:3000/chat -H "Content-Type: application/json" -d '{"prompt":"Say hi"}'`

### Non-obvious caveats
- Core functionality (`POST /chat`) requires **outbound internet** to the Neuralwatt API. The UI loads without it, but `/chat` returns a 500 if the API is unreachable. The API key is currently hardcoded in `neuralwatt_test.py` (the `NEURALWATT_API_KEY` env var mentioned in the docstring is NOT actually read by the code).
- Stats are in-memory only and reset on every server restart (no database).
- `debug=True` enables the reloader, so editing `neuralwatt_test.py` auto-restarts the server and wipes stats.
- There is no lint config and no test suite in the repo.
