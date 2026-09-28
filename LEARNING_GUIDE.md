# Ticket Tuner — learning guide

## What it does

Adapt a small model for support routing. The intended user is support platform developers. Browser controls → validated Flask API → project analysis/workflow → results and export.

## Run and demonstrate

Follow the README installation block, then: Generate the corpus, run train.py, and inspect artifacts/evaluation.json. Start the app and classify a short ticket. Try an out-of-domain request and explain why a human review policy is still required.

## Important files

- `app.py` — local HTTP interface and request/error handling.
- `core.py` — project-specific logic.
- `tests/` — regression and correctness checks.
- `reports/` — recorded outputs and verification evidence.

## Three engineering decisions

1. Fine-tune actual FLAN-T5-small weights locally for three support routing labels.
2. Split by template family before expanding examples so paraphrase groups cannot leak across splits.
3. Choose the checkpoint using validation macro F1, then evaluate the test set once against TF-IDF and majority baselines.

## Five interview questions

1. **What was actually fine-tuned?** A pinned FLAN-T5-small sequence-to-sequence model was trained locally for three support-routing labels. The recorded outputs and evaluation come from an actual CPU training run.

2. **Why split by template family?** Randomly splitting near-identical templates can leak phrasing across train and test. Holding out template families creates a more useful, though still limited, generalization check.

3. **Why include a TF-IDF baseline?** A lightweight classifier may solve the same narrow task more cheaply. The evaluation compares the fine-tuned model with that baseline rather than assuming an LLM is necessary.

4. **Does the perfect test score imply production readiness?** No. The 72 test examples are authored synthetic cases from a narrow template space. The measured macro F1 of 1.0 says nothing about messy real support traffic without further evaluation.

5. **Why are the trained weights not in Git?** The checkpoint is large. The repository includes pinned model provenance, training code and measured artifacts; users regenerate the checkpoint before running local inference.

## Independent exercise

Add a fourth routing class with new, independently split template families and rerun all baselines.

Write down the expected behavior before editing. Add a meaningful regression check, run the existing suite, and describe what changed in your own words.

## Contribution and resume guidance

The implementation was developed with substantial AI assistance under Abhijith Viswanathan's direction. The verified contribution is the working artifact and the learning work actually completed, not invented employment or adoption.

Suggested factual bullet after personally validating the demo:

- Fine-tuned FLAN-T5-small locally for three support-routing labels with template-family holdouts; measured macro F1 of 1.0 on 72 limited synthetic test examples.

Use [VERIFICATION.md](VERIFICATION.md) to add only measured numbers. Do not claim production traffic, users, savings, upstream acceptance or cloud deployment without corresponding evidence.
