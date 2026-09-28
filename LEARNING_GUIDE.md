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

1. **What problem does this project solve, and what is its unit of work?** Explain adapt a small model for support routing, identify support platform developers as the audience, and trace one concrete example through the files above. Use the demonstration output rather than hypothetical impact.
2. **Why did you choose the first design decision?** Fine-tune actual FLAN-T5-small weights locally for three support routing labels. Show the corresponding implementation and a test that would fail if that property were removed.
3. **How do you protect correctness when inputs or execution change?** Split by template family before expanding examples so paraphrase groups cannot leak across splits. Explain the relevant invalid-input or edge-case test and distinguish a checked property from an untested assumption.
4. **How do you make results inspectable and reproducible?** Choose the checkpoint using validation macro F1, then evaluate the test set once against TF-IDF and majority baselines. Point to actual outputs and recorded commands. Explain why a successful example is weaker evidence than a tested boundary or independently reconciled total.
5. **What would you improve before real deployment or real-data use?** Authored synthetic data contain only three labels and a small number of templates. Perfect synthetic holdout scores are not evidence of production accuracy. Inputs truncate at 96 tokens. Model weights require several hundred MB and local CPU time; they are saved locally but excluded from Git. Choose one limitation, describe the missing evidence, and propose a measurable acceptance check rather than promising production readiness.

## Independent exercise

Add a fourth routing class with new, independently split template families and rerun all baselines.

Write down the expected behavior before editing. Add a meaningful regression check, run the existing suite, and describe what changed in your own words.

## Contribution and resume guidance

The implementation was developed with substantial AI assistance under Abhijith Viswanathan's direction. The verified contribution is the working artifact and the learning work actually completed, not invented employment or adoption.

Suggested factual bullet after personally validating the demo:

- Implemented and validated adapt a small model for support routing using PyTorch · Transformers, with fine-tuning and documented correctness checks and limitations.

Use [VERIFICATION.md](VERIFICATION.md) to add only measured numbers. Do not claim production traffic, users, savings, upstream acceptance or cloud deployment without corresponding evidence.
