Yes. We'll leave **multi-query retrieval** aside and move directly into **LangGraph + Agent architecture**.

The goal of this first implementation is **not** to build a sophisticated agent. It's to make the architecture obvious.

# 1. First agentic workflow

We'll build exactly this:

```text
                    User Query
                        │
                        ▼
                     Router
                    /      \
                   /        \
                  ▼          ▼
            RAG Search   Direct Answer
                  │
                  ▼
               Generate
                  │
                  ▼
                Answer
```

This is a great first LangGraph example because it lets you see the difference between a normal RAG chain and a graph with **decision-making**.

---

# 2. What LangGraph gives us

Before coding, understand these five concepts.

### State

State is the information flowing through the graph.

For our first version:

```python
class AgentState(TypedDict):
    query: str
    route: str
    retrieved_chunks: list
    answer: str
```

Think:

```text
State
 ├── query
 ├── route
 ├── retrieved_chunks
 └── answer
```

Every node can read/update this state.

---

### Node

A node is a piece of work.

We'll have:

```text
router
rag_search
direct_answer
generate
```

For example:

```python
def router(state):
    ...
```

and:

```python
def rag_search(state):
    ...
```

A node receives state and returns state updates.

---

### Edge

An edge tells LangGraph:

> After this node finishes, where do I go?

Normal edge:

```text
RAG Search
    ↓
Generate
```

Conditional edge:

```text
Router
  │
  ├── rag
  │     ↓
  │   RAG Search
  │
  └── direct
        ↓
      Direct Answer
```

---

# 3. Router

The router is where we introduce our first **decision**.

For example:

```text
"What does the NIST AI RMF say about trustworthy AI?"
```

→

```text
RAG
```

because the answer should come from enterprise documents.

But:

```text
"Hello"
```

could be:

```text
Direct Answer
```

The router doesn't answer the question.

It decides **which path should handle it**.

That's already different from your existing workflow.

---

# 4. Important distinction: workflow vs agent

Our first implementation is technically an **agentic workflow**, but don't call it a fully autonomous agent yet.

Why?

Because we explicitly define:

```text
Router
 ├── RAG
 └── Direct
```

The possible actions are predetermined.

We're building:

```text
LLM decision
+
predefined graph
```

rather than:

```text
LLM
 ↓
decide any tool
 ↓
execute
 ↓
observe
 ↓
decide next action
 ↓
...
```

The latter is much closer to a traditional tool-using agent loop.

This distinction is important for interviews.

---

# 5. Project structure

I'd add:

```text
app/
└── agents/
        ├── __init__.py
        ├── state.py
        ├── router.py
        ├── nodes.py
        └── graph.py
```

We're deliberately separating:

```text
State
Nodes
Graph
```

so you can see the LangGraph concepts rather than putting everything into one giant file.

---

# 12. What we just built

For a RAG question:

```text
User Query
    ↓
Router
    ↓
route = "rag"
    ↓
RAG Search
    ↓
retrieved_chunks added to State
    ↓
Generate
    ↓
answer added to State
    ↓
END
```

For a direct question:

```text
User Query
    ↓
Router
    ↓
route = "direct"
    ↓
Direct Answer
    ↓
END
```

---

# 13. This is the key LangGraph lesson

Compare your current custom RAG:

```text
Query
 ↓
Retrieve
 ↓
Prompt
 ↓
LLM
 ↓
Answer
```

with LangGraph:

```text
                    State
                      │
                      ▼
                    Router
                   /      \
                  /        \
               RAG          Direct
                │              │
                ▼              ▼
            Generate         Answer
                │
                └──────┬───────┘
                       ▼
                      END
```

The **graph structure itself represents the workflow**.

That's the main thing I want you to understand before we make it more sophisticated.

---

## One correction before you implement

Don't connect this to your FastAPI `/chat` endpoint yet.

First build and test the graph independently:

```text
tests/
└── test_agent_graph.py
```

We want to prove:

### Test 1

```text
"What are the characteristics of trustworthy AI?"
```

produces:

```python
route == "rag"
```

and actually retrieves chunks.

### Test 2

```text
"Hello"
```

produces:

```python
route == "direct"
```

and does not call Qdrant.

Once those work, **then** we'll connect this graph to FastAPI.

That gives us a clean progression:

```text
Custom RAG
    ↓
LangChain RAG
    ↓
Query Transformation
    ↓
LangGraph workflow
    ↓
Conditional routing
    ↓
Tools
    ↓
Agent
```

The **first LangGraph workflow is working end-to-end with your real services**.

We now have:

```text
User Query
    ↓
LangGraph State
    ↓
Router
    ├───────────────┐
    ↓               ↓
   RAG           Direct
    ↓               ↓
Retrieval          LLM
    ↓
Generate
    ↓
LLM
    ↓
Answer
```

And you've verified both paths with real services.

### What we've learned/implemented

* **State** — query, workspace, route, retrieved chunks, answer
* **Nodes** — router, retrieval, direct answer, generate
* **Edges** — normal transitions between nodes
* **Conditional edge** — router chooses `rag` vs `direct`
* **Real service injection** — Qdrant/retrieval, prompt service, and Ollama/LLM
* **Integration tests** — both paths actually execute successfully

### Next: inspect the graph execution

Before adding more agent complexity, I want you to actually **see which nodes execute**.

For example, for:

```text
"What are the characteristics of trustworthy AI?"
```

we should be able to observe:

```text
START
 ↓
router
 ↓
rag_search
 ↓
generate
 ↓
END
```

while:

```text
"Hello"
```

should show:

```text
START
 ↓
router
 ↓
direct_answer
 ↓
END
```

This is the next thing I'd do because it makes **conditional routing in LangGraph tangible**, rather than just something hidden inside `graph.invoke()`.

After that, we'll move to **tool invocation**, which is the important step toward a genuine agent:

```text
Agent
  ↓
decides whether to use tool
  ↓
search_documents()
  ↓
Qdrant
  ↓
observation
  ↓
LLM
```

That's where we'll start moving from **agentic workflow → actual tool-using agent**.
