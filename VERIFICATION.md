# Ticket Tuner — verification

Verification date: 28 September 2026. Tests and examples were executed; they are not illustrative pass claims.

- Project checks: 7 passed.
- Dependency/setup verification: fresh isolated Python 3.12 environment passed.
- Main browser/API workflow: verified locally; actual result saved in reports/example-output.json.
- Publication: [public repository](https://github.com/abhijith-abhii/ticket-tuner) verified under **abhijith-abhii**.
- Actual application screenshot: reports/screenshots/app.png. Browser rendered successfully at 1280px width.

## Actual model run
Pinned FLAN-T5-small fine-tuning completed in 19.37 seconds on CPU. Split sizes: {'train': 216, 'validation': 72, 'test': 72}. Test macro F1: 1.000; TF-IDF baseline macro F1: 0.667. These are authored synthetic examples with limited template diversity, not real ticket performance.

## Evidence
- `reports/test-results.txt`: actual test output.
- `reports/clean-setup.json`: isolated setup result where applicable.
- `reports/publication-check.json`: credential-pattern and file audit.
- `DATA_AND_SOURCES.md`: source and license notes.

## GitHub verification

- [Verify: passed](https://github.com/abhijith-abhii/ticket-tuner/actions/runs/36416636372)

Verified source revision: `4e49601e96050a3d9f78970bd64d3ba31e5e78ab`. Subsequent presentation-only changes do not change that implementation evidence.
