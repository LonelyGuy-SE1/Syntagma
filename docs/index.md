---
title: PESU Curriculum Automation
permalink: /
---

# PESU Curriculum Automation

PESU Curriculum Automation is a FastAPI and static frontend application for collecting course submissions, refining them into curriculum-ready records, previewing PDF output, staging reviewable edits, and preserving curriculum snapshots.

## System Overview

| Layer | Location | Responsibility |
| --- | --- | --- |
| Static frontend | `frontend/` | Course entry, course management, PDF preview, live editor, and version history |
| API backend | `backend/app/` | FastAPI routes, validation, refinement, previews, drafts, chat, and snapshots |
| Persistence | Supabase | Raw submissions, refined courses, agent drafts, chat history, attachments, and curriculum versions |
| Rendering | Jinja2 and WeasyPrint | Curriculum summary pages, course detail pages, and PDF exports |
| Model provider | OpenRouter | Submission refinement and live editor chat with tool calls |

## Runtime Flow

1. Faculty submit raw course data through `frontend/form/`.
2. `POST /api/submissions` validates the payload and stores it in `submissions`.
3. A background refinement task builds deterministic academic fields, calls the model for prose fields, and writes `refined_submissions`.
4. Course management and preview pages read refined records through `/api/courses` and `/api/preview/*`.
5. The live editor can edit JSON fields directly or create draft changes through agent tools.
6. Drafts are reviewed with generated diffs before being applied to refined records.
7. Version snapshots store complete curriculum states and can restore a prior snapshot.

## Frontend Surfaces

| Route | Purpose |
| --- | --- |
| `/` | Dashboard for the available application surfaces |
| `/form/` | Raw course submission form |
| `/courses/` | Refined course list with filtering and soft delete |
| `/preview/` | Overall or semester PDF preview and download |
| `/live-editor/` | Course preview, chat assistant, JSON editor, draft review, and version restore |
| `/versions/` | Snapshot list, snapshot preview, and editor handoff |

The frontend is plain HTML, CSS, and JavaScript. There is no Node build step.

## API Surface

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/api/submissions` | `POST` | Store a raw submission and queue refinement |
| `/api/submissions/{id}/refine` | `POST` | Manually refine a submission |
| `/api/refined/{refined_id}` | `GET` | Read template-ready course fields |
| `/api/refined/{refined_id}` | `PATCH` | Update editable refined fields |
| `/api/courses` | `GET` | List active refined courses |
| `/api/courses/{refined_id}` | `DELETE` | Archive a refined course |
| `/api/preview/course/{refined_id}` | `GET` | Render one course as HTML |
| `/api/preview/pdf` | `GET` | Render the full curriculum as PDF |
| `/api/preview/semester/{sem}/pdf` | `GET` | Render one semester as PDF |
| `/api/versions` | `GET`, `POST` | List or create curriculum snapshots |
| `/api/versions/{version_id}/restore` | `POST` | Restore a saved curriculum snapshot |
| `/api/agent/drafts` | `GET`, `POST` | List or create reviewable course drafts |
| `/api/agent/drafts/{draft_id}/apply` | `POST` | Apply a proposed draft after review |
| `/api/agent/document-drafts` | `GET`, `POST` | List or create multi-course drafts |
| `/api/chat/sessions` | `GET`, `POST` | Manage live editor chat sessions |
| `/api/chat/sessions/{session_id}/messages` | `GET`, `POST` | Read or stream chat messages |
| `/api/chat/sessions/{session_id}/attachments` | `POST` | Upload document context for chat |
| `/api/health/schema` | `GET` | Check required Supabase tables |

## Submission Contract

`CourseSubmission` is defined in `backend/app/models/submission.py`.

Required fields:

- `faculty_email`
- `course_title`
- `offering_department`: `MA`, `CS`, or `UZ`
- `target_department`: `CSE`, `ECE`, `ME`, `BT`, `EEE`, or `AIML`
- `semester`: string value from `1` to `8`
- `credit_category`: `0`, `2`, `4`, or `5`
- `raw_course_content`: at least 50 characters
- `text_books`: at least 5 characters

Optional fields:

- `reference_books`
- `preferred_tools`

Successful submissions return `message` and the inserted `submission` row.

Validation errors use FastAPI's standard `422` response with a `detail` array.

## Deterministic Fields

The backend computes these fields in `backend/app/services/deterministic.py`:

| Credit category | L | T | P | S | C | Course type |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `5` | 4 | 0 | 2 | 5 | 5 | Core Course-Lab Integrated |
| `4` | 4 | 0 | 0 | 4 | 4 | Core Course |
| `2` | 2 | 0 | 0 | 2 | 2 | Core Theory |
| `0` | 0 | 0 | 0 | 0 | 0 | Foundation Course |

All configured target departments currently map to `B. TECH`.

Agent drafts are not allowed to change deterministic fields such as program, hours, credits, or course type. Drafts that attempt these changes are blocked.

## Database

Run `docs/schema.sql` in the Supabase SQL editor before using the application. The schema creates:

- `submissions`
- `refined_submissions`
- `curriculum_versions`
- `finalized_submissions`
- `agent_document_drafts`
- `agent_drafts`
- `course_revision_history`
- `chat_sessions`
- `chat_messages`
- `chat_attachments`

Use `GET /api/health/schema` to verify that the required tables exist.

## Environment

Required backend variables:

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `OPENROUTER_URL`
- `OPENROUTER_API_KEY`
- `OPENROUTER_MODEL`

Optional backend variables:

- `CURRICULUM_YEAR`
- `SENTRY_DSN`
- `SENTRY_ENVIRONMENT`
- `SENTRY_RELEASE`

Keep environment values in `.env` or platform secrets. Do not expose backend credentials in frontend code.

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd backend
fastapi dev app/main.py
```

The backend serves the static frontend at `http://127.0.0.1:8000/` and mounts the API under `/api`.

Run checks from the repository root:

```bash
source .venv/bin/activate
pytest
python3 -m compileall backend/app
```

## Deployment

The Docker image installs the Python dependencies, copies `backend/` and `frontend/`, and runs:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 7860
```

The included GitHub Actions workflow syncs `main` to the Hugging Face Space configured in `.github/workflows/sync-to-hub.yml`.

The static frontend can also be deployed from `frontend/`. The included `frontend/vercel.json` rewrites `/api/*` requests to the deployed backend.

## Current Checks

The test suite covers:

- Deterministic credit, hour, program, and course type mapping
- Submission refinement helpers
- Preview rendering and curriculum summary behavior
- Agent diffing, protected field checks, and draft tooling
- OpenRouter streaming and error handling
- Static frontend route structure
- Supabase schema status checks
- Attachment extraction safeguards and text/DOCX parsing
