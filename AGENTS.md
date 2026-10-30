# cs003_vector_db_for_rag

Vector Databases for RAG.
The user writes course notes; you write one runnable script per set of notes.

## The standing task

When the user points at a doc under `lessons/` ("do `module01/01_similarity_search.md`",
"here is a new doc"), read it and write the script for it. The doc is the spec - no
need to ask what to build.

## Layout contract

Notes, script and generated files share one stem and live together:

```
lessons/module01/01_similarity_search.md        # notes (the user writes these)
lessons/module01/01_similarity_search.py        # the script (you write this)
lessons/module01/output/01_similarity_search/   # what it generates, if anything (gitignored)
    similarities.csv
    nearest_neighbors.json
```

- The script filename matches the doc filename exactly, `.md` -> `.py`, beside it.
- Module folders are zero padded: `module01`, never `module1`.
- A new module folder needs no configuration.

### Self-contained projects

A folder under `lessons/` that holds its own `pyproject.toml` (e.g.
`lessons/moduleNN/some_project/`) is an independent project, not a lesson
script. The rules above and below do not apply to it. Follow its own README and
Makefile, use its own `.venv`, and never import `app.config` from it or add its
dependencies to `devtools/requirements.txt`. Add each one to `extend-exclude` in
`devtools/pyproject.toml`.

## Writing a lesson script

Cover the concepts the doc actually describes, in the doc's order, one short
section per concept with a one-line comment introducing it. Flat top-level code:
no `main()`, no argparse, no try/except. These are read as examples, so they
should contain only the code the doc is about.

**Never hardcode a path or a model id.** Import them from `app/config/envs.py`:

| Need                          | Use                                                                       |
| ----------------------------- | ------------------------------------------------------------------------- |
| the doc this script came from | `doc_path(__file__)`                                                      |
| somewhere to write a file     | `output_path(__file__, "similarities.csv")` (parent directory is created) |
| which model                   | its constant in `envs.py` (see below)                                     |
| an LLM's reply limit          | `DEFAULT_MAX_TOKENS`                                                      |

Both path helpers derive everything from `__file__`, so renaming or moving a
lesson needs no edit anywhere.

Where results go:

- text, or anything you would just look at -> `print("[section label]", ...)`
- file shaped (`.json`, `.csv`, `.md`, ...) -> write through `output_path(...)`

The first lesson that needs a model (an LLM, an embedding model, ...) adds its id
to `app/config/envs.py` as a constant, with a one-line comment saying which lessons
use it. Model ids move faster than training data, so an unfamiliar id there is
more likely new than wrong: keep it, don't swap in one you recognise.

Keys load themselves: importing `app.config.envs` runs `load_dotenv()`. A lesson
that needs an API key adds the variable, empty, to `devtools/.env.sample`, and the
user puts the value in `.env`. Clients that read their key from the environment
(`ChatAnthropic` and `ANTHROPIC_API_KEY`, say) then need no argument.

## Verify without spending the user's money

A lesson that calls a paid API (Claude, say) makes real billed calls. **Ask before
running one for real.** Verify it for free first by stubbing the model and running
the script unchanged from a scratchpad file - this exercises the prompts, parsers
and file writes. For a LangChain chat model:

```python
import runpy

import langchain_anthropic
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage

# one AIMessage per model call the script makes, in order
canned = iter([AIMessage("..."), AIMessage('{"key": "value"}'), AIMessage("a, b, c")])
langchain_anthropic.ChatAnthropic = lambda **kwargs: GenericFakeChatModel(messages=canned)
runpy.run_path("lessons/moduleNN/<nn>_<name>.py", run_name="__main__")
```

Give one canned `AIMessage` per model call, in order, each shaped for whatever
parser consumes it. Run it with `PYTHONPATH=.`. Afterwards delete the stub output
or restore the real files, so `output/` only ever holds genuine runs.

## Commands

| Command                                                       | Does                                                                     |
| ------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `make lesson LESSON=lessons/module01/01_similarity_search.py` | run one lesson (sets `PYTHONPATH=.`, which nested scripts need)          |
| `make lint` / `make lint-check`                               | ruff fix / check only; line length 120, config `devtools/pyproject.toml` |
| `make clean-output`                                           | delete every `lessons/**/output/` folder                                 |
| `make commit`                                                 | commit through commitizen                                                |

## Repo conventions

- Do not commit unless asked. A commit-msg hook enforces conventional commits
  (`feat:`, `fix:`, `chore:`, ...).
- `output/` is gitignored. Never commit generated files.
- Use `git mv` when moving tracked files.
- Python 3.14, venv at `.venv`, dependencies unpinned in `devtools/requirements.txt`.
- `README.md` is the human-facing doc; update it when the architecture changes.
