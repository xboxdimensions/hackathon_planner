# UQ Program Planner

A program planner made by first-year students for first-year students (and everyone else).

> **First-year hackathon project:** This was built during our first-year hackathon as an early learning project. It is a functional prototype, not a polished or production-ready application, and it is not the most advanced implementation. Some features, error handling, data validation, testing, and UI polish are limited.

The application retrieves live UQ program requirements and course metadata, then generates a prerequisite-aware semester plan.

## Architecture

```text
UQ program page
    ↓
scrapePlansAndCore()
    ↓
core courses, elective candidates, plan options
    ↓
courseData()
    ↓
course names, offerings and prerequisite expressions
    ↓
Plan
    ↓
semester-by-semester JSON
    ↓
Flask drag-and-drop frontend
```

The scraper currently handles UQ's embedded `programRequirements` JSON format and the current UQ program-page redirect. Prerequisite expressions are normalized into:

- lists for `AND` requirements
- tuples for `OR` choices
- strings for individual course codes

The planner selects the first option in an `OR` group by default and exposes the alternatives to the frontend.

## Run locally

From the repository root:

```bash
FLASK_RUN_PORT=5088 bash FlaskApp/run.sh
```

Then open:

```text
http://127.0.0.1:5088/
```

The app uses live UQ pages, so generating a plan requires an internet connection. Select:

```text
Computer Science (program 2451)
```

Then choose a starting year and full-time or part-time load.

## API example

```bash
curl -X POST http://127.0.0.1:5088/api \
  -H 'Content-Type: application/json' \
  -d '{"ProgramCode":"2451","startingYear":"2025","Load":"full"}'
```

The response contains:

- `Plan` — courses grouped by year and semester
- `CoreCourses` — unresolved core choices
- `electives` — courses extracted from the selected program
- `errors` — courses that could not be scheduled

## Data-engineering discussion

This is an early data-integration project rather than a modern RAG system. Its relevant engineering concerns are:

- ingesting data from an external source
- handling an upstream HTML/JSON schema change
- parsing semi-structured prerequisite text
- normalizing source data into a usable internal model
- traversing prerequisite dependencies
- applying semester and capacity constraints
- exposing structured data to a frontend

A useful interview summary is:

> We scraped UQ program and course pages, normalized the requirements and prerequisite expressions, and used that data to generate a dependency-aware degree plan. When UQ changed its page serialization, the original parser failed. I updated the ingestion boundary to extract the embedded JSON structurally and added a boolean prerequisite parser for the current `AND`/`OR` format. The same production concerns apply to RAG ingestion: schema drift, validation, observability, caching, and testable transformations.

## Known limitations

- The app intentionally uses live UQ data and depends on UQ's public page structure.
- UQ may change its HTML or embedded JSON again.
- The planner chooses the first alternative in a prerequisite choice rather than optimizing all possible plans.
- The original project has limited automated test coverage.
- UQ program requirements are academic guidance, not official enrolment advice.

This repository is shared as a record of a first-year hackathon project and a starting point for future improvements.