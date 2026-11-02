# CS003: Vector Databases for RAG: An Introduction

Certificate available at:

## Requirements

- Python 3.14.7 (see `.tool-versions`)

## Setup

```bash
make venv       # create .venv
make env        # copy devtools/.env.sample to .env (won't overwrite an existing one)
make install    # install dependencies and the git hooks
```

When a lesson needs an API key, it is listed in `devtools/.env.sample`: put its
value in `.env`.

On commit, the pre-commit hook fixes the staged files (trailing whitespace, final
newline, `ruff check --fix`, `ruff format`) and re-stages the fixes, so the commit only
fails on issues that cannot be fixed automatically. A file with extra unstaged edits is
not re-staged (that would clash with pre-commit's stash): stage the whole file and
commit again. The commit message must be a conventional commit (`feat: ...`,
`chore: ...`) with a header of at most 72 characters.

## Usage

| Command                     | Does                                                        |
| --------------------------- | ----------------------------------------------------------- |
| `make main`                 | Run `main.py`                                               |
| `make lesson LESSON=<path>` | Run one lesson script                                       |
| `make clean-output`         | Delete every generated `output/` folder under `lessons/`    |
| `make lint`                 | Lint and format, applying fixes                             |
| `make lint-check`           | Lint and format checks only, no writes                      |
| `make commit`               | Commit through commitizen (conventional commit messages)    |
| `make hooks`                | (Re)install the pre-commit and commit-msg hooks             |
| `make update-hooks`         | Bump the pinned hook revisions in `.pre-commit-config.yaml` |
| `make check-updates`        | List outdated dependencies                                  |
| `make reinstall`            | Force a clean reinstall of all dependencies                 |

## Layout

```
lessons/             # the course: notes, scripts and generated files, by module
app/config/envs.py   # model settings, notes/output path mapping
main.py              # entry point
devtools/            # requirements, tool config (ruff, commitizen), .env.sample
.agents/skills/      # agent skills (lesson-script)
.claude/skills/      # symlinks to .agents/skills, for Claude Code
```

Every command that needs the tool config passes `--config devtools/pyproject.toml`.

## Lessons

Each lesson keeps its notes, its script and its results together. Module folders are
zero padded (`module01`, not `module1`) so they keep sorting past module 9.

```
lessons/
  module01/
    01_similarity_search.md      # the notes (you write these)
    01_similarity_search.py      # the script (the lesson-script skill writes it)
    output/
      01_similarity_search/      # what the script generates (gitignored)
        similarities.csv
        nearest_neighbors.json
```

Write the notes, then call the skill with their path:

```
/lesson-script lessons/module01/01_similarity_search.md    # Claude Code, Cursor, Copilot
$lesson-script lessons/module01/01_similarity_search.md    # Codex
```

The script finds its notes and output folder through `app/config/envs.py`, so it holds
no paths or model ids. Run it with:

```bash
make lesson LESSON=lessons/module01/01_similarity_search.py
```

## Self-contained projects

Some lessons are full apps instead of single scripts, each in its own folder under
`lessons/moduleNN/`. Each one has its own venv, `pyproject.toml`, `Makefile`, `.env`
and README, and it does not use the root `.venv` or `app/config`. Set it up and run
it from inside its own folder. Add the folder to `extend-exclude` in
`devtools/pyproject.toml`, because each project lints itself.

## Agents

`AGENTS.md` holds the always-loaded instructions for coding agents; `CLAUDE.md` only
imports it (`@AGENTS.md`), so edit `AGENTS.md`. Skills use the
[Agent Skills](https://agentskills.io) format in `.agents/skills/<name>/`, read by
Codex, Cursor and Copilot. Claude Code reads `.claude/skills/` instead, so each skill
gets a symlink there:

```bash
ln -s ../../.agents/skills/<name> .claude/skills/<name>
```
