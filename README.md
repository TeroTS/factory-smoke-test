# factory-smoke-test

Dependency-free calculator fixture for the software factory PoC. The baseline
provides `calculator.py:add(a, b)` and standard-library addition tests.

Run from this repository's root; no package installation is needed:

```sh
python3 -m unittest discover -s tests -v
```

The later agent task is to add `multiply(a, b)` and tests for positive, negative,
and zero operands while preserving addition. Multiplication is intentionally
absent from this baseline. Both demonstration gates start from the same recorded
baseline commit, publish separate task branches/PRs targeting `main`, and leave
those PRs unmerged for human review.
