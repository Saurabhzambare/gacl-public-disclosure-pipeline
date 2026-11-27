# Document retrieval — first AI-extension milestone

Status: implemented and verified locally on feature/document-retrieval,
24 November 2026. This is a keyword-search foundation for later RAG. It does not
use embeddings, generate answers, train a model or execute agent tools. The
existing observation pipeline, cloud load and Power BI report remain separate.

Learning context, 25 November: this is the earlier reference implementation,
not proof of learner implementation. Follow [Master Build Order](PHASE_2_BUILD_ORDER.md)
Steps 1–10 to inspect/build/test the same responsibilities personally. Use the learning log for current learner progress. Do not overwrite existing files or run commands from
an unpublished feature that is absent from the actual checkout.

Current guided checkpoint, 27 November: Step 5 is complete on the published
feature/phase2-guided branch; documentation merge 98c14ec is verified. Use
[the Step 6 lesson](PHASE_2_STEP_06.md) for the current learner's storage build,
read-only status, exact edits and tests. Its --build-index / --index-status
commands become available only after implementation. The commands and search
capabilities below still describe the separate earlier reference prototype;
they are not automatically installed by reading these documents.

[Concepts](AI_CONCEPTS.md) explain methods; [contracts](AI_CONTRACTS.md) distinguish
current search output from future numerical/RAG/agent interfaces; the
[evaluation plan](AI_EVALUATION_PLAN.md) defines subsequent comparisons.

## What works

- Verify both cached PDF files against config/sources.json SHA-256 pins.
- Index usable embedded text from each page, retaining exact text offsets and
  source/document hashes, physical PDF page numbers and source URLs.
- Attach printed-page numbers only where explicitly reviewed. Unknown printed
  pages remain null; there is no guessed page offset.
- Preserve two short, version-pinned reviewed annotations separately from
  extracted text. Section labels are not inferred; section remains null.
- Return ranked candidate passages using SQLite FTS5/Porter/BM25, one hit per
  distinct source/page. Lower BM25 scores rank first; they are not probabilities.
- Filter by approved source ID or document reporting scope. Scope metadata is
  not an inferred period or a classification of every sentence on a page.
- Rebuild atomically into a separate local index. Missing/changed source files,
  invalid mappings or failed replacement preserve the previous index.
- Search/read through read-only connections, with quoted token queries,
  parameterized filters and chunk/page/citation consistency checks.
- Evaluate page relevance with versioned reference cases and explicit limitations.

No new Python dependency, model download, API key, cloud query or paid service is
needed. FTS5 must be available in the interpreter's SQLite build. The tests use
synthetic PDFs in temporary directories; they are not GACL data.

## Windows commands

Run these after the feature files are available in your local clone, from the
repository root in PowerShell. The existing .venv and cached PDFs are used.

```powershell
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval build
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval info
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval search "What was April 2025 fresh water consumption at Dahej?" --top-k 3
```

For a specific source or reviewed page:

```powershell
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval search "renewable energy" --source gacl_brsr_2025_26
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval page --source gacl_dahej_plot3_ec_2025_h1 --pdf-page 5
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval page --source gacl_brsr_2025_26 --pdf-page 1
```

Linux/macOS: replace the interpreter path with .venv/bin/python.
The global --root option, if needed, goes before the subcommand. A missing index
or source produces a nonzero exit with instructions. If PDFs are missing, first
run the normal verified PDF pipeline described in the main README. The
--from-examples route does not provide PDF pages and cannot build this index.

The search JSON deliberately contains answer=null and answerability=not_assessed.
A lexical match is not an answer or proof that the question is answerable. Use
page to inspect the full extracted context and the linked original PDF. Future
numerical answers must use the validated observation route, not guessed table
column interpretation by a language model.

## Local artifacts and provenance

The generated database is data/retrieval/index.sqlite. The directory is ignored
by Git, including local evaluation outputs. It does not replace or migrate
 data/warehouse/gacl.sqlite. The metadata table contains a build manifest with:

- document IDs, source hashes/URLs, document scopes and physical page counts;
- index build time (not a new document retrieval time);
- extraction/chunk/query versions, runtime versions and chunk parameters;
- counts of chunks/indexed pages and skipped-page reasons;
- a fingerprint of the source register and retrieval configuration.

The reader rejects a configuration/source-version mismatch until rebuild.
Chunk IDs include source/version, exact content hash, page, offsets, printed
mapping and any reviewed annotation. Rebuilding identical inputs yields the
same chunk IDs even though build timestamps differ. This is integrity checking,
not a signed or tamper-proof database security boundary.

Known coverage from the real-source run:

| Source | Physical pages | Indexed pages | Chunks |
|---|---:|---:|---:|
| Dahej Plot 3 April–September 2025 | 21 | 20 | 60 |
| BRSR FY 2025–26 | 50 | 50 | 76 |
| Total | 71 | 70 | 136 |

The monthly PDF's first page has no usable embedded text and is explicitly
skipped. OCR is not implemented. Other pages can have partial text: some BRSR
labels and footnotes visible in a PDF renderer are absent from extraction.
A pinned PDF and nonempty text do not guarantee complete table extraction.

config/retrieval.json has two short reviewed annotations, for BRSR PDF pages 1
and 37. Their printed pages and visual source statements were rechecked on
24 November. They describe the standalone boundary/reporting year and the
comparative-methodology/annual-production notes. reviewed_note is always
separate from text and labelled as reviewed metadata, not automatic extraction.
No missing labels elsewhere are silently reconstructed. Chunking preserves
extracted text and overlaps line windows, but does not reconstruct all table
headers; a returned chunk may lack year/unit context available on the full page.

## Evaluate the baseline

```powershell
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval evaluate --split development
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval evaluate --split holdout
```

The 40 cases in evaluation/retrieval_cases.json include 20 numeric/reference,
8 boundary/definition, 8 unsupported and 4 adversarial questions. There are
24 development and 16 holdout cases. The set is assistant-authored and
source-checked; independent human annotation review remains pending. Both
partitions use the same two documents and are not an external blind benchmark.
The initial query/ranking policy was retained after observing holdout results.
Do not tune on that partition and continue describing it as unseen.

Only the 28 answerable cases receive recall/hit/MRR scores. The evaluator first
checks source hashes, printed-page mappings and evidence anchors against the
indexed full pages and separate reviewed annotations. Unsupported/adversarial
cases are diagnostic retrieval runs. They do not demonstrate answer refusal,
prompt-injection resistance or agent safety, because none of those layers exists.
All reported answer/abstention accuracy values remain null.

Results are in [the baseline report](RETRIEVAL_EVALUATION.md). The local
prototype also retains a curated `evaluation/baseline_results.json`; that
prototype-only JSON is not included in this documentation-only publication.
No claim of production answer accuracy follows from these page-level metrics.

## Next work

Independent reference review and a Windows laptop/CI run are pending for this
feature branch. Next, compare semantic retrieval against this frozen lexical
baseline. Then add a separate validated-metric read tool and cited generation.
Agentic tool choice and an interface follow only after those checks work.

The 30-step order now places deterministic numerical evidence tools before
generated answers. Embeddings are a pretrained ML inference application;
generation and dynamic tools are distinct later gates. Model/runtime/optional
dependency choices remain unset. No hosted vector store or paid provider is
required or enabled by these lexical commands.

Technical references:
https://sqlite.org/fts5.html
https://docs.python.org/3.11/library/sqlite3.html
