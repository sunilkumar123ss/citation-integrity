# Citation and quotation integrity

Runnable educational demo/starter with synthetic examples.

Checks that every cited source exists and the supplied quotation occurs in that source after case/whitespace normalization. It explicitly does not infer whether a quote entails a claim or whether a source is true. The result says “quoted_evidence_found,” not “fact verified.” Missing citations and invented quotations fail.

## Run

Python 3.10+; standard library only. From this directory:

```sh
python3 main.py
python3 main.py --help
python3 -m unittest -v
```

No network requests, credentials, or paid services are used. Any model/provider integration would be a separate adapter; the current implementation performs only the operations described here.

Read `main.py` for the public functions and `test_main.py` for success/failure invariants. Fixture content is synthetic and safe to replace with local non-sensitive examples.

## Scope

This is an educational implementation with synthetic fixtures. Run the tests and inspect the documented limits before adapting it.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
