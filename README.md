# 🛍️ ScrapItChat

**Drop in a URL, get a salesperson.** Paste any website into the chat, and an LLM scrapes the page (plus a few relevant sub-pages it picks itself), then role-plays an enthusiastic sales rep who answers your questions about whatever that page is selling — a product, a service, a brand, or a person's skills.

It's a fun little side-project that stitches together **headless-browser scraping**, **LLM-driven link selection**, and a **streaming Gradio chat** — swappable between OpenAI, Anthropic, and a local Ollama model with a single dropdown.

---

## ⚡ Quickstart (≈5 minutes)

You'll need [**uv**](https://docs.astral.sh/uv/) (Python package/environment manager) and API keys for OpenAI and/or Anthropic.

```bash
# 1. Install dependencies into a local .venv
uv sync

# 2. One-time: install the Chromium browser Playwright drives
uv run playwright install

# 3. Add your API keys (see below)

# 4. Launch — opens automatically in your browser
uv run python main.py
```

### Configure your keys

Create a `.env` file in the project root (it's gitignored):

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

> You only need the key for the provider(s) you actually plan to use. The **GPT** option needs `OPENAI_API_KEY`, **Claude** needs `ANTHROPIC_API_KEY`, and **Llama** needs a local [Ollama](https://ollama.com/) server running at `http://localhost:11434` (no key required).

That's it — a Gradio chat window opens. Send it a full URL (including `https://`) as your first message, then start asking questions.

---

## 🎬 How it works

1. **First message = the URL.** The app scrapes the landing page with a headless Chromium browser, so JavaScript-heavy sites render properly.
2. **The LLM picks relevant sub-pages.** It scans every link on the page and chooses the useful ones (About, Company, Careers…), skipping noise like Terms of Service and Privacy.
3. **Those pages are scraped too** and concatenated into a single sales-context prompt.
4. **Now you chat.** Every following message is answered by the LLM in character as a persuasive salesperson, grounded in the scraped content — with responses **streamed** token-by-token.

---

## ✨ Features

- 🌐 **Paste-a-URL chat** — the first message you send is the website; everything after is a conversation about it.
- 🎭 **Persuasive sales persona** — the LLM role-plays an enthusiastic sales rep and answers grounded in the page's actual content.
- 🧭 **LLM-driven link discovery** — instead of blindly crawling, an LLM call selects the most relevant sub-pages (About / Company / Careers-type) and ignores legal/contact clutter.
- 🕸️ **Headless-browser scraping** — Playwright + Chromium renders JS-heavy pages (`domcontentloaded`), then BeautifulSoup extracts clean text (scripts, styles, images, and inputs stripped).
- 🔀 **Multi-provider, one dropdown** — switch between **GPT** (OpenAI), **Claude** (Anthropic), and **Llama** (local Ollama) live in the UI. All three go through the OpenAI SDK, differing only by `base_url`/`api_key`.
- 📐 **Structured link output** — link selection uses a strict `json_schema` for Claude and `json_object` mode for the others, validated against a Pydantic model.
- 💬 **Streaming responses** — answers appear token-by-token as they're generated.
- 🛟 **Resilient sub-page fetching** — if one relevant sub-page fails to load, it's skipped so a single slow link doesn't break the turn; only a failed *landing* page stops the flow and re-prompts you for a valid URL.
- 🧠 **Conversation memory** — the built system prompt and scraped context persist across turns via Gradio state, so follow-up questions stay in context.

---

## 🏗️ Project layout

| Path | What's in it |
| --- | --- |
| [main.py](main.py) | Entry point — launches the Gradio app. |
| [helpers/chat.py](helpers/chat.py) | Gradio wiring, provider/model selection, and the two LLM entry points. |
| [helpers/scraper.py](helpers/scraper.py) | Playwright + BeautifulSoup scraping and link selection. |
| [helpers/prompt_maker.py](helpers/prompt_maker.py) | All prompt strings (pure functions returning text). |
| `lab.ipynb` | Scratchpad notebook for experimentation — not part of the app runtime. |

---

## 🔧 Good to know

- **Requires Python ≥ 3.12.**
- **No test suite, linter, or build step** — this is a focused side-project.
- **Content gets trimmed aggressively:** each scraped page is capped at 2,000 characters, and the entire assembled sales prompt is capped at 5,000 characters. Large sites are heavily condensed before the model sees them.
- **Dev extras** (Jupyter / ipykernel) install with `uv sync --group dev`.
- **Provider notes:** the model IDs live in `define_model_and_provider()` in [helpers/chat.py](helpers/chat.py) — that one function is the single place to swap or add models.
