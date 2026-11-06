# Inverted Index Search

A small search engine that indexes text documents in an inverted index and answers boolean and wildcard queries from a desktop window. Written in Python 3 using only the standard library (tkinter for the GUI).

## Features

- Loads every `.txt` file from a folder, with a built-in five-document sample when no folder exists
- Tokenization, case folding, accent and apostrophe stripping
- Inverted index that records each term's documents and positions
- Boolean queries with `AND`, `OR` and `NOT`; adjacent terms mean `AND`
- Wildcard queries such as `mon*`, `*key` and `m*ey`, using a permuterm index
- GUI with a search input box, a Search button and a read-only result area

## Project structure

| File | Role |
| --- | --- |
| `main.py` | Entry point, wires the modules together |
| `document_loader.py` | 1. Document loading |
| `tokenizer.py` | 2. Tokenization |
| `normalizer.py` | 3. Normalization / case folding |
| `inverted_index.py` | 4. Inverted index construction |
| `query_processor.py` | 5. Query processing |
| `wildcard.py` | 6. Wildcard processing (permuterm index) |
| `gui.py` | 7. Frontend GUI |

## Run

Requires Python 3 with tkinter (included in most Python installers). No other packages are needed.

```bash
python main.py                 # uses ./documents if it exists, otherwise the built-in sample
python main.py path/to/folder  # index your own .txt files
```

Type a query, then press **Search** or Enter.

## Query syntax

| Query | Meaning |
| --- | --- |
| `fox dog` | both terms |
| `fox OR dog` | either term |
| `fox NOT dog` | fox without dog |
| `mon*`, `*key`, `m*ey` | wildcard: `*` stands for any run of characters |

Queries are case-insensitive. `NOT` binds tightest, then `AND`, then `OR`.

## Sample results (built-in corpus)

| Query | Documents |
| --- | --- |
| `fox` | doc1, doc3 |
| `mon*` | doc3, doc5 |
| `*key` | doc3, doc5 |
| `m*ey` | doc3 |
| `fox AND NOT quick*` | doc3 |
| `lazy OR inverted` | doc1, doc2, doc4 |
| `Q*K` | doc1 |

## How it works

1. Documents are loaded, tokenized and normalized, then added to the inverted index (term to documents and word positions).
2. A query is tokenized and normalized the same way and evaluated with set operations over the index.
3. Wildcard terms are expanded through a permuterm index. Every term plus a `$` end marker is stored in all its rotations, so `m*ey` becomes the prefix search `ey$m`, answered by binary search.

## Limitations

Results are unranked, there is no stemming or stop-word removal, parentheses in queries are not supported, and the index is rebuilt in memory at every start.

## Publish to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<repository-name>.git
git push -u origin main
```
