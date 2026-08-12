# Retrieval Evaluation

## Purpose

Evaluate whether semantic search retrieves the correct document
chunks for representative user questions.

The evaluation focuses on retrieval quality before introducing
the generation/LLM layer.

---

## Embedding Model

Model:

BAAI/bge-small-en-v1.5

---

## Vector Database

Qdrant

---

## Evaluation Method

For each question:

1. Generate query embedding.
2. Search Qdrant.
3. Retrieve Top-3 chunks.
4. Check whether the expected relevant chunk appears.
5. Record the best similarity score.
6. Record observations.

---

## Questions

| Question | Top-3 Relevant? | Best Score | Retrieved File | Notes |
|---|---|---:|---|---|
| What is the personal loan interest rate? | | | | |
| Who is eligible for the personal loan? | | | | |
| What documents are required? | | | | |
| What is the maximum loan amount? | | | | |
| What is the repayment period? | | | | |

---

## Results

### Top-3 Retrieval Accuracy

Relevant questions retrieved in Top-3:

`X / 5`

Top-3 retrieval accuracy:

`X%`

---

## Observations

### What worked

-

### What failed

-

### Potential improvements

-