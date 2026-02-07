# csv2json

> Convert CSV to JSON or JSONL on the command line, with optional type inference.

## Why

`csv2json` turns a CSV file into JSON without pulling in pandas. It is one
stdlib-only file you can drop into a container or a CI job.

## Install

No dependencies. Copy the file, or:

```
git clone https://github.com/USER/csv2json
cd csv2json
python csv2json.py --help
```

## Usage

```
python csv2json.py data.csv                # JSON array of objects
python csv2json.py data.csv --lines        # JSONL, one object per line
python csv2json.py data.csv --infer        # parse numbers/booleans/empties
python csv2json.py data.tsv -d $'\t'       # tab separated
cat data.csv | python csv2json.py -        # read from stdin
```

## Type inference

`--infer` is off by default because CSV is all strings and guessing can bite.
When it is on:

| CSV cell        | JSON value |
|-----------------|------------|
| `42`            | `42`       |
| `3.5`           | `3.5`      |
| `true` / `FALSE`| `true` / `false` |
| `` (empty)      | `null`     |
| `null` / `none` | `null`     |
| anything else   | string     |

Leading zeros stay strings, so zip codes and IDs survive.
