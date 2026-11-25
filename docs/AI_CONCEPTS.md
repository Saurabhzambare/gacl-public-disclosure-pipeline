# AI concepts — technical and ELI5 guide

Updated: 25 November 2026. Learning companion to the
[Phase 2 build order](PHASE_2_BUILD_ORDER.md). A definition here does not mean
the corresponding feature is implemented. Use [status](STATUS.md) for evidence.

## The complete idea

The completed data pipeline is the checked ledger. Document retrieval is the
library catalogue. A future embedding model adds meaning-based search; a
language model writes from supplied evidence; an agent eventually selects
approved read tools. Each layer needs its own evaluation.

## Sources and data engineering

| Concept | Technical meaning in this project | ELI5 |
|---|---|---|
| Data grain | What one record represents: a monthly site daily-average rate or an annual standalone company total | Read the label before comparing two numbers |
| Provenance / lineage | Source, document version, page, period, scope and original value behind a fact | The number's address and travel history |
| SHA-256 | Fingerprint of bytes used to detect differences from an approved document | Check that this is the same book; it does not prove the author is right |
| Manifest | Structured record of inputs, versions, parameters and outputs | A packing list showing what went into the build |
| Extraction | Reading embedded characters or selected table values from a PDF | Copying words and numbers from a page |
| OCR | Recognizing text from an image; not implemented in the baseline | Teaching the computer to read a photograph |
| Normalization | Consistent representations without changing meaning, such as exact decimal strings | Put entries in the same format |
| Validation | Required-field, scope, unit, period and reconciliation checks | Check the homework against explicit rules |
| Decimal | Decimal arithmetic used for source values and comparisons | A calculator that preserves the chosen decimal representation |
| Idempotency | Reprocessing the same accepted inputs does not create extra records | Pressing save twice does not create two facts |
| Atomic replacement | Replace the old index only after the new one is successfully built and closed | Finish the new catalogue before replacing the old one |
| Versioning | Retain which source/configuration/model produced an artifact | Label each edition so answers can be traced |

## Retrieval and evidence

| Concept | Technical meaning in this project | ELI5 |
|---|---|---|
| Corpus | The two approved public documents being searched | The books on our allowed shelf |
| Page evidence | Exact extracted page text with source/version/page metadata | A photocopy with its book and page label |
| Chunk | Exact span of extracted page text; currently at most 1,800 characters | A smaller reading card |
| Overlap | Repeated context between adjacent chunks; target 250 characters, adjusted at line boundaries | Repeat a little so the next card makes sense |
| Metadata | Descriptions such as source ID, hash, offsets, page and scope | The address label attached to the card |
| Full-text index | Search structure for matching terms in stored passages | A word catalogue |
| Tokenization | Split text into units used by a search engine or model; their tokenizers differ | Decide what pieces of text to work with |
| Stop words | Selected common terms removed by the lexical query policy | Skip words that usually add little to this search |
| Stemming | Reduce some word forms to a common stem; not full synonym understanding | Recognize some word-family members |
| BM25 | Lexical ranking method accounting for matching terms, frequency and passage length | Order the cards by useful word matches |
| Top-k | Return up to k ranked candidates; current evaluation uses distinct source/pages | Show a shortlist of five pages |
| Deduplication | Prevent multiple chunks from the same page taking every page-result slot | Do not put five copies of one page on the shortlist |
| Answerability | Whether available evidence supports an answer; not assessed by current lexical search | Finding related words does not mean we found the answer |
| Citation | Evidence identifier/page link supporting a particular claim | Let the reader check the page |

## Models and language

| Concept | Technical meaning | ELI5 |
|---|---|---|
| AI | Broad class of systems performing tasks associated with intelligence | The overall toolbox |
| ML | Models learn patterns from examples during training | Learn from examples instead of writing every rule |
| Neural network / deep learning | Learned parameterized computation; deep networks have multiple layers | Many adjustable stages work together |
| Parameter / weight | A learned model value changed by training | One of the tool's learned internal settings |
| Pretraining | Earlier training on a broad dataset | The tool learned before we brought it here |
| Inference | Running a trained model on new input | Use the learned tool |
| Embedding | Numeric vector representing text according to a trained model | Put text on a meaning map |
| Vector dimension | Number of components in that representation | How many coordinates describe each point |
| Cosine similarity | Compare vector directions under a declared convention | Look for nearby directions on the map |
| Semantic retrieval | Retrieve passages using learned text representations | Find related meanings even with different words |
| Bi-encoder | Encode query and passages separately for comparison | Put question and cards on the same map |
| Reranker / cross-encoder | Jointly score query-candidate pairs after initial retrieval | Re-read shortlisted cards more carefully |
| Hybrid retrieval | Combine lexical and semantic signals through an explicitly evaluated policy | Consult both kinds of librarian |
| Vector database | Storage/search system for vectors; optional at this corpus size | A specialized filing cabinet, if needed |
| Generative AI | Produce new content using a trained model | A writer |
| LLM | Language model that processes/generates token sequences | A writer trained on language patterns |
| Prompt | Instructions and context supplied for an inference request | The assignment given to the writer |
| Context window | Limit on tokens processed in an interaction under the chosen runtime | How much can fit on the writer's desk |
| Temperature | Generation sampling control where supported; not a factuality guarantee | How varied the wording may be |
| Fine-tuning | Additional training that changes model parameters | Teach the writer through more training exercises |
| RAG | Retrieve evidence and include it in the context for generated answers | Give the writer the relevant pages before writing |
| Grounding | Tie output claims to supplied evidence and validated tool results | Each factual sentence needs a checked basis |
| Hallucination | Unsupported or incorrect model output, including plausible text | The writer says something the evidence does not support |
| Abstention | Explicitly state insufficient evidence instead of inventing an answer | Say that the book does not tell us |

Embedding generation is inference, not custom model training. Similarity and
BM25 ranking are not calibrated confidence. A pinned citation proves location,
not that the cited page supports the particular sentence. A generated explanation
does not override the validated numerical inputs.

## Workflows, agents and operational checks

| Concept | Technical meaning | ELI5 |
|---|---|---|
| Workflow | Predetermined application control flow | Follow a recipe |
| Tool | Validated application function exposed to a model | An approved button |
| Tool schema | Allowed function name and structured argument/result contract | Label the button and define what it accepts |
| Agent | Model dynamically chooses tools and follow-up steps within enforced limits | A coordinator selects approved buttons |
| State | Explicit question, evidence, calls and progress retained during a run | The coordinator's working clipboard |
| Budget | Application-enforced limits on calls, time, tokens or output | A limit on how long and how often buttons can be pressed |
| Tool trace | Recorded arguments, results, evidence IDs and outcomes | A receipt for what actually happened |
| Prompt injection | Untrusted text attempts to change operating instructions or tool behavior | A book page tries to order the librarian around |
| Allowlist | Only explicitly registered operations can execute | Only approved buttons are connected |
| Replay | Re-run recorded deterministic tools against identified inputs/versions | Recheck the calculator using the same figures |
| Latency | Measured response time, including declared warm/cold conditions | How long a question takes |
| Reproducibility | Enough versions, inputs and instructions to inspect/repeat a result | Someone else can follow the same recipe |

## Evaluation

A baseline is a simple reference method. Retrieval Recall@5 checks whether
expected evidence appears among five results. MRR@5 rewards the first relevant
result appearing earlier. The current 26/28 result measures expected page hits,
not generated-answer accuracy or universal report coverage.

Development cases help improve the system. A final evaluation set should not
be repeatedly consulted during tuning. Data leakage occurs when unavailable
or evaluation information influences development and makes results misleading.
Independent review and newly reserved questions strengthen this small pilot;
both original partitions still use the same two documents.

Unit tests check individual functions; integration tests check connected parts;
regression tests protect previously working behavior. AI evaluation checks
retrieval relevance, exact numbers, claim support, citations, abstention and tool
behavior separately. Passing one kind does not establish all the others.

## Running example

Question: how did April compare with September 2025?

1. Identify `freshwater_average_daily`, Dahej Plot 3, the two monthly periods and
   KL/day. The facts tool reads 12,540.8 and 11,738.1 from validated records.
2. The comparison tool calculates later minus earlier: -802.7 KL/day. Percentage
   change is approximately -6.40%, with display rounding separate from values.
3. The explanation identifies two reported daily-average rates and cites PDF
   page 5 / printed page 4. It does not claim a six-month total volume saved.
4. A cause question requires explicit source evidence. Monthly decline alone
   does not establish cause. The separate annual production-related footnote
   cannot automatically explain the monthly trend.

## Why forecasting waits

Eighteen mixed-grain records are not eighteen samples of one target. There are
only six monthly points and two annual periods per annual metric. Custom
forecasting would require a specific target, substantially more compatible
history, a temporal split, a naive baseline, uncertainty and error analysis.
Training, feature stores and predictive-maintenance claims are outside the
current Phase 2 deliverable.

## Reference reading

- [SQLite FTS5](https://sqlite.org/fts5.html)
- [Sentence Transformers retrieve and rerank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)
- [Workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)
- [scikit-learn common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)

These explain methods. They do not select or install a framework/model for the
project. Model-specific behavior and installation will be checked at its lesson.
