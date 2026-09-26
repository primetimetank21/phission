# Phission

**A little pause. A clearer perspective.**

Phission is an interactive learning workspace for looking more carefully at email requests and link destinations. This release is a **synthetic-only demo**, not a security product or a live phishing detector.

Choose one of five authored emails, select a link, and explicitly run demo analysis. Every result is **simulated**. No email URL is opened, fetched, or submitted to a service. There is no mailbox connection, credential setup, arbitrary URL input, upload feature, analytics, database, or hidden live-mode switch.

## Run locally

Requirements: [uv](https://docs.astral.sh/uv/), Python **3.13 or 3.14**, and the platform prerequisites in the [Reflex installation guide](https://reflex.dev/docs/getting-started/installation/) (including `unzip` on Linux). Python dependencies are locked in `uv.lock`; Reflex is pinned to **0.9.12**. The generated `reflex.lock/bun.lock` and `reflex.lock/package.json` pin frontend dependencies. `.python-version` selects Python 3.13 by default. This setup is validated on Linux/WSL; native Windows and macOS are not yet verified.

```sh
make setup   # locked Python dependencies + initialize project-local Bun
make run
```

Open **http://127.0.0.1:3000**. `make run` builds and serves the frontend and Python backend together in production mode, bound to loopback. Stop it with Ctrl+C. Changes require a restart/rebuild. The Makefile invokes uv with the committed lockfile and keeps the uv cache in `.cache/uv`.

Dependencies and the first frontend build require network downloads. `make setup` initializes Reflex's project-local **Bun 1.4.0**; app builds do not require a separate Node/npm installation. The Makefile selects local Bun and refuses to build if it is missing, preventing silent npm fallback and lock replacement. `rxconfig.py` enables frozen frontend installs; CI also checks that the frontend lock files stay unchanged. The Makefile keeps downloaded tooling and caches under the project’s ignored `.cache/`, with the virtual environment in `.venv/`. Framework telemetry is disabled in `rxconfig.py` and the Makefile. Runtime example analysis itself does not use external services. System fonts and local assets are used; there are no remote fonts, CDNs, or embedded media.

To select Python 3.14 explicitly, use `UV_PYTHON=3.14 make setup` and the same `UV_PYTHON=3.14` prefix on subsequent commands. Do not add API keys or real email to this repository.

## Check and build

After installing dependencies:

```sh
make check     # Ruff lint + formatting check, then pytest
make test      # behavioral tests only
make format    # explicitly apply Ruff formatting
make build     # optimized production frontend in .web/build/client/
```

Check/test targets do not install dependencies, write Git hooks, or modify source. CI runs checks and a production build on Python 3.13 and 3.14. Tests cover MIME/header/Unicode handling, nested HTML destinations, duplicates and prefix-overlapping links, incomplete coverage, malformed responses, score boundaries including zero, target isolation, loading/empty/error states, and credential-free application import/runtime with outbound connections blocked.

### Browser regressions (optional locally, required in CI)

With `make run` active in one terminal, use a second terminal with **Node 22.23.2+**:

```sh
npm ci --ignore-scripts
npx playwright install chromium
npm run test:browser
```

Chromium also needs its [platform libraries](https://playwright.dev/docs/browsers#install-system-dependencies). These Node dependencies are **test tooling only**, separate from the app's Bun frontend lock. Set `PHISSION_URL=http://127.0.0.1:3157` if using another local port. The checks cover keyboard navigation, score/unknown/no-links flows, session isolation, responsive widths, four axe accessibility scans, no-JS messaging, nested 404s and attempted external browser requests. Screenshots and JSON evidence go to ignored `.scratch/browser-validation/`; CI retains them as artifacts for 30 days. Automated accessibility checks are not a screen-reader or physical-device audit.

For deliberate dependency updates, regenerate and review both frontend lock files with the pinned Bun/Reflex toolchain, then verify a clean build leaves them unchanged. Do not delete a lock or switch package managers merely to make CI pass.

**This is not a standalone static site.** JavaScript and a running Reflex Python backend/WebSocket connection are required for inbox selection and analysis. An exported frontend alone does not make the demo interactive. Production Reflex 0.9.12 serves both parts on a single port; see the [self-hosting documentation](https://reflex.dev/docs/hosting/self-hosting/) before any separate deployment work. This repository does not provision or deploy a service. Do not use a development server as a public deployment.

## What is real, and what is simulated?

| Real application logic                                   | Authored simulation                                              |
| -------------------------------------------------------- | ---------------------------------------------------------------- |
| Standard-library RFC822/MIME parsing                     | All five emails, names and destinations                          |
| Plain text and HTML anchor extraction                    | Local IPQS-shaped result objects                                 |
| Validation of provider success and integer score range   | Scores, concern levels and unavailable result                    |
| Per-session target selection and stale-result prevention | No live reputation lookup or independent phishing classification |

The scenarios include an ordinary workshop notice, an urgent credential lure, a friendly HTML label pointing to a different destination, an unavailable result with an uninspected attachment, and a note without links. Destinations use reserved `.example`/`.test` domains; the recipient uses `example.org`.

A score of **0 is valid**, not an error. Values 0–74 represent a lower signal, 75–84 caution, and 85–100 high concern in this demonstration. These illustrative thresholds are not validated detection performance. A score is **not a probability or a guarantee of safety**. Invalid responses are errors; unavailable results are unknown, not safe. The normalizer accepts already-decoded Python objects and validates them; there is deliberately **no live HTTP/JSON transport adapter**, timeout/retry layer, or provider authentication.

## Architecture and limits

One Python Reflex application; no separate API service, database, queues, or new machine learning.

- `phission/models.py`: typed messages, extracted links, coverage and scan outcomes.
- `phission/parsing.py`: bounded stdlib MIME parser (256 KB / 100 parts), decoded headers/text, HTML-to-text conversion and HTTP(S) link extraction.
- `phission/fixtures/` and `phission/demo.py`: fixed synthetic manifest and deterministic, message-and-URL-bound responses. Files load on the inbox event, not on module import.
- `phission/scanning.py`: success/unknown/error normalization, separate score and cautious guidance.
- `phission/state.py`: in-memory per-session selection/results. Nothing is persisted to disk; a server restart loses sessions. No deep-link or browser-history routing for message selection.
- `phission/phission.py` and `assets/styles.css`: one fixed page, semantic controls and responsive reading workspace. No runtime page generation or compilation on inbox actions.

Original email HTML is never rendered. The reading pane shows plain text; extracted destinations and HTML labels are shown separately, as text inside selection buttons. Text is not destructively rewritten to replace URLs. Attachments, embedded messages, image-only content, relative/non-HTTP links, redirects, obfuscated destinations and some malformed content are outside parsing coverage. Partial, unsupported and malformed messages are distinguished from “no HTTP(S) links found.” This bounded parser is not a production email sanitizer or a comprehensive threat detector.

### Accessibility

The interface uses semantic buttons/headings/landmarks, visible keyboard focus, selected-state text, a polite live status region, reduced-motion styling and a mobile back-to-messages link. Message selection moves focus to the reading heading; tab to destinations and use Enter/Space to select and analyze. Warnings use text, not color alone. Original images and HTML are not embedded.

Read-aloud is **not included** in this slice: there is no server speech engine or browser speech service. Browser/OS reading tools and assistive technology may be used independently. JavaScript-disabled users can read the static introduction and limitation text but cannot interact with the demo. Browser, mobile viewport and assistive-technology checks complement the unit tests; those tests alone do not establish accessibility conformance or physical-device support.

## Historical context

The original Phission prototype was built in **2023 for HCI and affective-computing coursework**, including usability testing. The original findings are no longer available. This refresh does not make outcome claims or reinterpret historical survey scores.

The original Gmail/IPQS integrations, server-local speech, Pynecone configuration, database and raw study artifacts are retired from the maintained tree. They are not archived as a second application. The historical source remains available at exact commit [`0ced1f54baccc2ed6abd307d43971e82315c3961`](https://github.com/primetimetank21/phission/tree/0ced1f54baccc2ed6abd307d43971e82315c3961). No history has been rewritten. Reintroducing real mail or live scanning would require a separate security/privacy scope, not an environment-variable toggle.
