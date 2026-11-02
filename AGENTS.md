# cs003_vector_db_for_rag

Vector Databases for RAG. The user writes course notes under `lessons/`; the
`lesson-script` skill writes the runnable script for each. If you can't load skills
and are asked for it, read `.agents/skills/lesson-script/SKILL.md` and follow it.

## Self-contained projects

A folder under `lessons/` with its own `pyproject.toml` is an independent project, not a
lesson, so the skill doesn't apply. Follow its own README and Makefile, use its own
`.venv`, never import `app.config` from it or add its dependencies to
`devtools/requirements.txt`, and add it to `extend-exclude` in `devtools/pyproject.toml`.

## Conventions

- Python 3.14, venv at `.venv`, dependencies unpinned in `devtools/requirements.txt`.
- `make lint` / `make lint-check`: ruff fix / check only (line length 120, config
  `devtools/pyproject.toml`).
- Don't commit unless asked. A commit-msg hook enforces conventional commits (`feat:`,
  `fix:`, `chore:`, ...); `make commit` runs commitizen.
- `output/` is gitignored: never commit generated files. `make clean-output` deletes them.
- Use `git mv` when moving tracked files.
- `README.md` is the human-facing doc; update it when the architecture changes.
- Skills live in `.agents/skills/<name>/`, so edit them there. `.claude/skills/<name>` is
  a relative symlink to each, for Claude Code.
