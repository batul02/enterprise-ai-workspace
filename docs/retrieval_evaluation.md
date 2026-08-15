# Retrieval Evaluation

## Objective

Evaluate the quality of semantic retrieval in the Enterprise AI Workspace before introducing the LLM generation layer.

The goal is to establish a small ground-truth evaluation dataset and measure whether the correct document chunks are retrieved within the Top-K results.

---

## Evaluation Document

**Document:** NIST AI Risk Management Framework (AI RMF 1.0)

**Embedding Model:** `BAAI/bge-small-en-v1.5`

**Vector Database:** Qdrant

**Search Configuration:** Top-K retrieval with workspace-level filtering.

---

## Evaluation Method

For each question:

1. Send the question to the semantic search API.
2. Retrieve the Top-5 results.
3. Identify whether the relevant chunk was retrieved.
4. Record whether the relevant chunk appeared at position 1, 3, or 5.
5. Record the best similarity score.
6. Add observations about retrieval quality.

### Metrics

For now, we will record:

- Top-1 retrieval
- Top-3 retrieval
- Top-5 retrieval
- Best similarity score

More formal metrics such as Recall@K and MRR will be automated later.

---

# Ground Truth Questions

| ID | Question | Expected Document | Relevant Chunk? | Top-1? | Top-3? | Top-5? | Best Score | Notes |
|---|---|---|---|---|---|---|---:|---|
| Q1 | What is the purpose of the AI Risk Management Framework? | NIST AI RMF 1.0 | Yes | Yes | Yes | Yes | 0.8181 | chunk_id=31 #1 |
| Q2 | What are the characteristics of trustworthy AI? | NIST AI RMF 1.0 | Yes | Yes | Yes | Yes | 0.8762 | Excellent retrieval. Top-1 directly lists all characteristics of trustworthy AI and explains that they should be balanced according to context of use. |
| Q3 | What are the four core functions of the AI RMF? | NIST AI RMF 1.0 | Yes | Yes | Yes | Yes | 0.8696 | Excellent retrieval. Top-1 directly identifies GOVERN, MAP, MEASURE, and MANAGE and provides additional context about how the Core is structured. |
| Q4 | What does the GOVERN function address? | NIST AI RMF 1.0 | Yes | Yes | Yes | Yes | 0.7874 | Strong retrieval. Top-1 directly addresses GOVERN's roles, responsibilities, decision-making, and organizational risk management. Top-2 and Top-3 provide additional detailed GOVERN responsibilities. |
| Q5 | What is the difference between the MAP and MEASURE functions? | NIST AI RMF 1.0 | Yes | No | Yes | Yes | 0.7317 | Relevant information is retrieved, but the distinction between MAP and MEASURE is not presented as clearly as in Q2–Q4. The Top-3 results mostly explain MEASURE and its dependency on risks identified by MAP. |
| Q6 | What activities are involved in managing AI risks? | NIST AI RMF 1.0 | Yes | Yes | Yes | Yes | 0.8066 | Strong retrieval. Top-1 identifies the four functions that organize AI risk-management activities, while Top-3 provides concrete examples of risk-management activities. |
| Q7 | What does the AI RMF say about measurement of AI risks? | NIST AI RMF 1.0 | Yes | Yes | Yes | Yes | 0.8450 | Excellent retrieval. Top-1 directly discusses measurement of AI risks, including evaluating trustworthiness, tracking risks, assessing metrics, and feeding measurement outcomes into MANAGE. |
| Q8 | What role does governance play in managing AI risks? | NIST AI RMF 1.0 | Yes | No | Yes | Yes | 0.8128 | Strong retrieval. Top-5 contains several highly relevant governance chunks, including its cross-cutting role and its influence on policies, accountability, organizational culture, and risk management. However, the most direct explanation of governance's overall role appears at #5 rather than #1. |
| Q9 | How does the AI RMF describe the identification and management of AI risks? | NIST AI RMF 1.0 | Yes | Yes | Yes | Yes | 0.8723 | Excellent retrieval. Top-1 directly explains that Part 1 frames AI risks and Part 2 provides GOVERN, MAP, MEASURE, and MANAGE to address them in practice. |
| Q10 | What does the AI RMF say about validity and reliability? | NIST AI RMF 1.0 | Yes | No | Yes | Yes | 0.7802 | Partially successful retrieval. The directly relevant chunk is retrieved at #3, but Top-1 is only the table of contents and Top-2 provides only a general mention. The best answer appears within Top-3. |

---

# Detailed Evaluation

## Q1 — Purpose of the AI RMF

**Question:**

> What is the purpose of the AI Risk Management Framework?

**Expected Document:** NIST AI RMF 1.0

**Top-5 Retrieved Results:**

1. the AI RMF is put into\nuse, additional lessons will be learned to inform future updates and additional resources.\nThe Framework is divided into two parts. Part 1 discusses how organizations can frame\nthe risks related to AI and describes the intended audience. Next, AI risks and trustworthi-\nness are analyzed, outlining the characteristics of trustworthy AI systems, which include\nPage 2\n\nNIST AI 100-1\nAI RMF 1.0\nvalid and reliable, safe, secure and resilient, accountable and transparent, explainable and\ninterpretable, privacy enhanced, and fair with their harmful biases managed.\nPart 2 comprises the “Core” of the Framework. It describes four specific functions to help\norganizations address the risks of AI systems in practice. These functions – GOVERN,\nMAP, MEASURE, and MANAGE – are broken down further into categories and subcate-\ngories. While GOVERN applies to all stages of organizations’ AI risk management pro-\n
2. and characterizations for\nAI risk.\n5. Be easily usable and fit well with other aspects of risk management. Use of the\nFramework should be intuitive and readily adaptable as part of an organization’s\nbroader risk management strategy and processes. It should be consistent or aligned\nwith other approaches to managing AI risks.\n6. Be useful to a wide range of perspectives, sectors, and technology domains. The AI\nRMF should be universally applicable to any AI technology and to context-specific\nuse cases.\n7. Be outcome-focused and non-prescriptive. The Framework should provide a catalog\nof outcomes and approaches rather than prescribe one-size-fits-all requirements.\n8. Take advantage of and foster greater awareness of existing standards, guidelines, best\npractices, methodologies, and tools for managing AI risks – as well as illustrate the\nneed for additional, improved resources.\n9. Be law- and regulation-agnostic.\nThe Framework should support organizations’\n
3. e advantage of those devel-\nopments and work towards a future of AI that is both trustworthy and responsible.\nPage 39\n\nNIST AI 100-1\nAI RMF 1.0\nAppendix C:\nAI Risk Management and Human-AI Interaction\nOrganizations that design, develop, or deploy AI systems for use in operational settings\nmay enhance their AI risk management by understanding current limitations of human-\nAI interaction. The AI RMF provides opportunities to clearly define and differentiate the\nvarious human roles and responsibilities when using, interacting with, or managing AI\nsystems.\nMany of the data-driven approaches that AI systems rely on attempt to convert or represent\nindividual and social observational and decision-making practices into measurable quanti-\nties. Representing complex human phenomena with mathematical models can come at the\ncost of removing necessary context. This loss of context may in turn make it difficult to\nunderstand individual and societal impacts that are key to AI risk management efforts.\n
4. nd identify op-\nportunities to maximize positive impacts. Effectively managing the risk of potential harms\ncould lead to more trustworthy AI systems and unleash potential benefits to people (individ-\nuals, communities, and society), organizations, and systems/ecosystems. Risk management\ncan enable AI developers and users to understand impacts and account for the inherent lim-\nitations and uncertainties in their models and systems, which in turn can improve overall\nsystem performance and trustworthiness and the likelihood that AI technologies will be\nused in ways that are beneficial.\nThe AI RMF is designed to address new risks as they emerge. This flexibility is particularly\nimportant where impacts are not easily foreseeable and applications are evolving. While\nsome AI risks and benefits are well-known, it can be challenging to assess negative impacts\nand the degree of harms. Figure 1 provides examples of potential harms that can be related\nto AI systems.\n
5. es, methodologies, and tools for managing AI risks – as well as illustrate the\nneed for additional, improved resources.\n9. Be law- and regulation-agnostic.\nThe Framework should support organizations’\nabilities to operate under applicable domestic and international legal or regulatory\nregimes.\n10. Be a living document. The AI RMF should be readily updated as technology, under-\nstanding, and approaches to AI trustworthiness and uses of AI change and as stake-\nholders learn from implementing AI risk management generally and this framework\nin particular.\nPage 42\n\nThis publication is available free of charge from:\nhttps://doi.org/10.6028/NIST.AI.100-1\n

**Relevant Chunk:** chunk_id=31

**Best Similarity Score:** 0.8181

**Top-1:** 

**Top-3:** 

**Top-5:** 

**Notes:**

---

## Q2 — Characteristics of Trustworthy AI

**Question:**

> What are the characteristics of trustworthy AI?

**Expected Document:** NIST AI RMF 1.0

**Top-5 Retrieved Results:**

1. ng characteristics of\ntrustworthy AI and offers guidance for addressing them. Characteristics of trustworthy AI\nsystems include: valid and reliable, safe, secure and resilient, accountable and trans-\nparent, explainable and interpretable, privacy-enhanced, and fair with harmful bias\nmanaged. Creating trustworthy AI requires balancing each of these characteristics based\non the AI system’s context of use. While all characteristics are socio-technical system at-\ntributes, accountability and transparency also relate to the processes and activities internal\nto an AI system and its external setting. Neglecting these characteristics can increase the\nprobability and magnitude of negative consequences.\nFig. 4. Characteristics of trustworthy AI systems. Valid & Reliable is a necessary condition of\ntrustworthiness and is shown as the base for other trustworthiness characteristics. Accountable &\nTransparent is shown as a vertical box because it relates to all other characteristics.\n
2. isting and emergent risks.\nPage 10\n\nNIST AI 100-1\nAI RMF 1.0\nFig. 3. AI actors across AI lifecycle stages. See Appendix A for detailed descriptions of AI actor tasks, including details about testing,\nevaluation, verification, and validation tasks. Note that AI actors in the AI Model dimension (Figure 2) are separated as a best practice, with\nthose building and using the models separated from those verifying and validating the models.\nPage 11\n\nNIST AI 100-1\nAI RMF 1.0\n3.\nAI Risks and Trustworthiness\nFor AI systems to be trustworthy, they often need to be responsive to a multiplicity of cri-\nteria that are of value to interested parties. Approaches which enhance AI trustworthiness\ncan reduce negative AI risks. This Framework articulates the following characteristics of\ntrustworthy AI and offers guidance for addressing them. Characteristics of trustworthy AI\nsystems include: valid and reliable, safe, secure and resilient, accountable and trans-\n
3. aque and uninterpretable systems,\nand inaccurate but secure, privacy-enhanced, and transparent systems are all unde-\nsirable. A comprehensive approach to risk management calls for balancing tradeoffs\namong the trustworthiness characteristics. It is the joint responsibility of all AI ac-\ntors to determine whether AI technology is an appropriate or necessary tool for a\ngiven context or purpose, and how to use it responsibly. The decision to commission\nor deploy an AI system should be based on a contextual assessment of trustworthi-\nness characteristics and the relative risks, impacts, costs, and benefits, and informed\nby a broad set of interested parties.\n3.1\nValid and Reliable\nValidation is the “confirmation, through the provision of objective evidence, that the re-\nquirements for a specific intended use or application have been fulfilled” (Source: ISO\n9000:2015). Deployment of AI systems which are inaccurate, unreliable, or poorly gener-\n
4. plication\ncontext and are performed throughout the AI system lifecycle. See Figure 3\nfor representative AI actors.\n10\nFig. 3\nAI actors across AI lifecycle stages. See Appendix A for detailed descrip-\ntions of AI actor tasks, including details about testing, evaluation, verifica-\ntion, and validation tasks. Note that AI actors in the AI Model dimension\n(Figure 2) are separated as a best practice, with those building and using the\nmodels separated from those verifying and validating the models.\n11\nFig. 4\nCharacteristics of trustworthy AI systems. Valid & Reliable is a necessary\ncondition of trustworthiness and is shown as the base for other trustworthi-\nness characteristics. Accountable & Transparent is shown as a vertical box\nbecause it relates to all other characteristics.\n12\nFig. 5\nFunctions organize AI risk management activities at their highest level to\ngovern, map, measure, and manage AI risks. Governance is designed to be\n
5. dth and diversity of\ninput from interested parties and relevant AI actors throughout the AI lifecycle can en-\nhance opportunities for informing contextually sensitive evaluations, and for identifying\nAI system benefits and positive impacts. These practices can increase the likelihood that\nrisks arising in social contexts are managed appropriately.\nUnderstanding and treatment of trustworthiness characteristics depends on an AI actor’s\nparticular role within the AI lifecycle. For any given AI system, an AI designer or developer\nmay have a different perception of the characteristics than the deployer.\nTrustworthiness characteristics explained in this document influence each other.\nHighly secure but unfair systems, accurate but opaque and uninterpretable systems,\nand inaccurate but secure, privacy-enhanced, and transparent systems are all unde-\nsirable. A comprehensive approach to risk management calls for balancing tradeoffs\n

**Relevant Chunk:** chunk_id=59

**Best Similarity Score:** 0.8762

#1  0.8762  ← exact answer
#2  0.8261  ← also directly relevant
#3  0.8199  ← relevant context
#4  0.7941  ← related
#5  0.7890  ← related

---

## Q3 — Four Core Functions

**Question:**

> What are the four core functions of the AI RMF?

**Expected Document:** NIST AI RMF 1.0

**Top-5 Retrieved Results:**

1. "gement with interested parties and relevant AI actors; and\n• augmented capacity for TEVV of AI systems and associated risks.\nPage 19\n\nNIST AI 100-1\nAI RMF 1.0\nPart 2: Core and Profiles\n5.\nAI RMF Core\nThe AI RMF Core provides outcomes and actions that enable dialogue, understanding, and\nactivities to manage AI risks and responsibly develop trustworthy AI systems. As illus-\ntrated in Figure 5, the Core is composed of four functions: GOVERN, MAP, MEASURE,\nand MANAGE. Each of these high-level functions is broken down into categories and sub-\ncategories. Categories and subcategories are subdivided into specific actions and outcomes.\nActions do not constitute a checklist, nor are they necessarily an ordered set of steps.\nFig. 5. Functions organize AI risk management activities at their highest level to govern, map,\nmeasure, and manage AI risks. Governance is designed to be a cross-cutting function to inform\nand be infused throughout the other three functions.\n"
2. the AI RMF is put into\nuse, additional lessons will be learned to inform future updates and additional resources.\nThe Framework is divided into two parts. Part 1 discusses how organizations can frame\nthe risks related to AI and describes the intended audience. Next, AI risks and trustworthi-\nness are analyzed, outlining the characteristics of trustworthy AI systems, which include\nPage 2\n\nNIST AI 100-1\nAI RMF 1.0\nvalid and reliable, safe, secure and resilient, accountable and transparent, explainable and\ninterpretable, privacy enhanced, and fair with their harmful biases managed.\nPart 2 comprises the “Core” of the Framework. It describes four specific functions to help\norganizations address the risks of AI systems in practice. These functions – GOVERN,\nMAP, MEASURE, and MANAGE – are broken down further into categories and subcate-\ngories. While GOVERN applies to all stages of organizations’ AI risk management pro-\n
3. "in conjunction with AI systems.\nAI risk management approaches for human-AI configurations will be augmented by on-\ngoing research and evaluation. For example, the degree to which humans are empowered\nand incentivized to challenge AI system output requires further studies. Data about the fre-\nquency and rationale with which humans overrule AI system output in deployed systems\nmay be useful to collect and analyze.\nPage 41\n\nNIST AI 100-1\nAI RMF 1.0\nAppendix D:\nAttributes of the AI RMF\nNIST described several key attributes of the AI RMF when work on the Framework first\nbegan. These attributes have remained intact and were used to guide the AI RMF’s devel-\nopment. They are provided here as a reference.\nThe AI RMF strives to:\n1. Be risk-based, resource-efficient, pro-innovation, and voluntary.\n2. Be consensus-driven and developed and regularly updated through an open, trans-\nparent process. All stakeholders should have the opportunity to contribute to the AI\nRMF’s development.\n"
4. "e\n9\n3\nAI Risks and Trustworthiness\n12\n3.1\nValid and Reliable\n13\n3.2\nSafe\n14\n3.3\nSecure and Resilient\n15\n3.4\nAccountable and Transparent\n15\n3.5\nExplainable and Interpretable\n16\n3.6\nPrivacy-Enhanced\n17\n3.7\nFair – with Harmful Bias Managed\n17\n4\nEffectiveness of the AI RMF\n19\nPart 2: Core and Profiles\n20\n5\nAI RMF Core\n20\n5.1\nGovern\n21\n5.2\nMap\n24\n5.3\nMeasure\n28\n5.4\nManage\n31\n6\nAI RMF Profiles\n33\nAppendix A: Descriptions of AI Actor Tasks from Figures 2 and 3\n35\nAppendix B: How AI Risks Differ from Traditional Software Risks\n38\nAppendix C: AI Risk Management and Human-AI Interaction\n40\nAppendix D: Attributes of the AI RMF\n42\nList of Tables\nTable 1 Categories and subcategories for the GOVERN function.\n22\nTable 2 Categories and subcategories for the MAP function.\n26\nTable 3 Categories and subcategories for the MEASURE function.\n29\nTable 4 Categories and subcategories for the MANAGE function.\n32\ni\n\nNIST AI 100-1\nAI RMF 1.0\nList of Figures\nFig. 1\n"
5. "agement resources based on\nassessed and prioritized risks. It is incumbent on Framework users to continue to apply\nthe MANAGE function to deployed AI systems as methods, contexts, risks, and needs or\nexpectations from relevant AI actors evolve over time.\nPage 31\n\nNIST AI 100-1\nAI RMF 1.0\nPractices related to managing AI risks are described in the NIST AI RMF Playbook. Table\n4 lists the MANAGE function’s categories and subcategories.\nTable 4: Categories and subcategories for the MANAGE function.\nMANAGE 1: AI\nrisks based on\nassessments and\nother analytical\noutput from the\nMAP and MEASURE\nfunctions are\nprioritized,\nresponded to, and\nmanaged.\nMANAGE 1.1: A determination is made as to whether the AI\nsystem achieves its intended purposes and stated objectives and\nwhether its development or deployment should proceed.\nMANAGE 1.2: Treatment of documented AI risks is prioritized\nbased on impact, likelihood, and available resources or methods.\n"

**Relevant Chunk:** chunk_id=86

**Best Similarity Score:** 0.8696

#1  0.8696  ← Direct answer
#2  0.8151  ← Direct answer repeated in Part 1
#3  0.8046  ← General AI RMF context
#4  0.7662  ← Table of contents containing the four functions
#5  0.7644  ← MANAGE-specific information

---

## Q4 — GOVERN Function

**Question:**

> What does the GOVERN function address?

**Expected Document:** NIST AI RMF 1.0

**Top-5 Retrieved Results:**

1. The GOVERN function provides organizations with the opportunity to clarify and define the roles and responsibilities for humans in Human-AI team configurations and those overseeing AI system performance. It also creates mechanisms to make decision-making processes more explicit to help counter systemic biases.
   **Score:** 0.7874 — `chunk_id=151`

2. The GOVERN function cultivates and implements a culture of risk management within organizations designing, developing, deploying, evaluating, or acquiring AI systems.
   **Score:** 0.7606 — `chunk_id=89`

3. The GOVERN function cultivates risk-management culture, outlines processes for identifying and managing risks, incorporates impact assessment processes, aligns AI risk management with organizational principles and policies, and connects technical AI development with organizational values.
   **Score:** 0.7549 — `chunk_id=90`

4. GOVERN applies across all stages of an organization's AI risk-management processes, while MAP, MEASURE, and MANAGE can be applied to AI-system-specific contexts and lifecycle stages.
   **Score:** 0.7314 — `chunk_id=32`

5. This result discusses the MANAGE function and how it uses information established through GOVERN and MAP. It is related to the overall framework but does not directly answer what GOVERN addresses.
   **Score:** 0.7087 — `chunk_id=120`

**Relevant Chunk:** `chunk_id=151`
**Also strongly relevant:** `chunk_id=89`, `chunk_id=90`

**Best Similarity Score:** `0.7874`

```text
#1  0.7874  ← Directly discusses GOVERN's roles, responsibilities, and decision-making
#2  0.7606  ← Directly describes the purpose and activities of GOVERN
#3  0.7549  ← Detailed description of GOVERN responsibilities
#4  0.7314  ← Relevant context about GOVERN's scope across the AI lifecycle
#5  0.7087  ← Mostly about MANAGE; only indirectly related to GOVERN
```

**Q4 = successful, strong retrieval.**

One interesting difference from Q2/Q3: the best score is only **0.7874**, but the result is still clearly correct. This is another good reason **not to establish a hard similarity threshold from these scores alone**.

---

## Q5 — MAP vs MEASURE

**Question:**

> What is the difference between the MAP and MEASURE functions?

**Expected Document:** NIST AI RMF 1.0

**Top-5 Retrieved Results:**

1. `chunk_id=117` — Discusses MEASURE evaluating security, resilience, transparency, accountability, explainability, privacy, fairness, and bias **as identified in the MAP function**.
   **Score:** 0.7317

2. `chunk_id=114` — Describes MEASURE methods and metrics, including metrics for AI risks identified during MAP.
   **Score:** 0.7306

3. `chunk_id=110` — Directly describes MEASURE as using quantitative, qualitative, or mixed-method approaches to analyze, assess, benchmark, and monitor AI risk, using knowledge of risks identified in MAP.
   **Score:** 0.7157

4. `chunk_id=32` — Provides general context about GOVERN, MAP, MEASURE, and MANAGE and their application across the AI lifecycle.
   **Score:** 0.7142

5. `chunk_id=113` — Describes MEASURE's purpose, including evaluating trustworthiness, tracking risks, and using measurement outcomes for MANAGE.
   **Score:** 0.7083

**Relevant Chunk:** `chunk_id=110`

**Best Similarity Score:** `0.7317`

```text
#1  0.7317  ← Relevant, but mainly describes MEASURE's relationship with MAP
#2  0.7306  ← Relevant to MEASURE and risks identified during MAP
#3  0.7157  ← Strongest conceptual explanation of MEASURE
#4  0.7142  ← General framework context
#5  0.7083  ← Relevant to MEASURE but not the MAP-vs-MEASURE distinction
```

### Important observation

**Q5 is our first weaker retrieval result.**

The correct conceptual relationship is partially present:

```text
MAP
 ↓
identifies/characterizes AI risks
 ↓
MEASURE
 ↓
analyzes/assesses/monitors those identified risks
```

But none of the Top-5 chunks gives a clean **MAP vs MEASURE comparison**.

So I would mark:

```text
Relevant chunk? YES
Top-1? NO
Top-3? YES
Top-5? YES
```

This is exactly the kind of result we want to capture in our evaluation rather than forcing every query to be considered a success.

**Q5 = partially successful retrieval; Top-3 contains useful evidence, but Top-1 does not directly answer the comparison question.**

---

## Q6 — AI Risk Management Activities

**Question:**

> What activities are involved in managing AI risks?

**Expected Document:** NIST AI RMF 1.0

**Top-5 Retrieved Results:**

1. `chunk_id=23` — Describes the AI RMF's four high-level functions: GOVERN, MAP, MEASURE, and MANAGE, which organize AI risk-management activities. It also provides context about the risks posed by AI systems.
   **Score:** 0.8066

2. `chunk_id=26` — Explains AI risk management as part of responsible AI development and use, including considering context and potential positive and negative impacts.
   **Score:** 0.8016

3. `chunk_id=124` — Provides concrete MANAGE activities, including allocating resources, sustaining deployed systems, responding to previously unknown risks, deactivating systems when necessary, and managing third-party AI risks.
   **Score:** 0.8012

4. `chunk_id=147` — Discusses defining human roles and responsibilities when using, interacting with, or managing AI systems.
   **Score:** 0.7904

5. `chunk_id=146` — Discusses addressing harmful bias, generative-AI risks, security concerns, attack surfaces, third-party technologies, transfer learning, and monitoring technological advances.
   **Score:** 0.7830

**Relevant Chunk:** `chunk_id=23`
**Also relevant:** `chunk_id=124`, `chunk_id=26`, `chunk_id=146`

**Best Similarity Score:** `0.8066`

```text
#1  0.8066  ← Explains the four functions that organize AI risk-management activities
#2  0.8016  ← Explains the broader purpose and activities of AI risk management
#3  0.8012  ← Contains concrete MANAGE activities
#4  0.7904  ← Relevant to human roles in AI risk management
#5  0.7830  ← Relevant risk-management considerations and examples
```

### Observation

This is a slightly different query from Q3.

Q3 asked:

> What are the four functions?

The retriever found the **exact definition** at Top-1.

Q6 asks more broadly:

> What activities are involved in managing AI risks?

The results are therefore more distributed across the document. That's reasonable: there isn't necessarily one single chunk containing the complete answer.

The Top-3 combination is actually useful:

```text
GOVERN / MAP / MEASURE / MANAGE
          +
concrete MANAGE activities
          +
responsible AI / risk considerations
```

So I would classify this as **successful retrieval**, although the answer would likely require combining information from multiple retrieved chunks.

**Q6 = successful, strong retrieval.**


---

## Q7 — Measurement of AI Risks

**Question:**

> What does the AI RMF say about measurement of AI risks?

**Expected Document:** NIST AI RMF 1.0

**Top-5 Retrieved Results:**

1. `chunk_id=113` — Directly discusses measurement of AI risks. It explains that different measurement types should provide unique and meaningful information for assessing AI risks, and that measurement helps evaluate trustworthiness, identify and track existing and emerging risks, and verify the effectiveness of metrics. It also states that measurement outcomes are used by the MANAGE function for risk monitoring and response.
   **Score:** 0.8450

2. `chunk_id=31` — Provides general context about the AI RMF and identifies MEASURE as one of its four functions for addressing AI risks.
   **Score:** 0.8438

3. `chunk_id=153` — Discusses ongoing research and evaluation related to human-AI configurations and the need to collect and analyze data about human interactions with AI systems.
   **Score:** 0.8437

4. `chunk_id=20` — Table of contents showing the MEASURE section and its position within the AI RMF Core.
   **Score:** 0.8383

5. `chunk_id=155` — Describes general attributes of the AI RMF, including its use of standards, guidelines, methodologies, and tools for managing AI risks.
   **Score:** 0.8203

**Relevant Chunk:** `chunk_id=113`

**Best Similarity Score:** `0.8450`

```text
#1  0.8450  ← Directly answers the question about measuring AI risks
#2  0.8438  ← Relevant general context about MEASURE
#3  0.8437  ← Related to evaluation, but focused on human-AI interaction
#4  0.8383  ← Contains the MEASURE section reference, but little substantive information
#5  0.8203  ← General AI RMF information
```
### Observation

Q7 is particularly strong because **Top-1 directly answers the question**, rather than merely mentioning the MEASURE function.

The most useful part of the retrieved chunk is the relationship:

```text
Measurement
    ↓
Evaluate trustworthiness
    ↓
Identify & track existing/emerging risks
    ↓
Verify metric effectiveness
    ↓
MANAGE function uses measurement outcomes
```

One thing worth noting for our evaluation: **Top-2 and Top-3 have very similar scores to Top-1**, but they aren't equally useful. Top-3, for example, is about human-AI interaction rather than the core question.

This is a good example of why **ranking and semantic relevance need to be evaluated separately from raw similarity score**.

**Q7 = successful, excellent retrieval.**

---

## Q8 — Role of Governance

**Question:**

> What role does governance play in managing AI risks?

**Expected Document:** NIST AI RMF 1.0

**Top-5 Retrieved Results:**

1. `chunk_id=98` — Describes governance processes for AI testing, incident identification, information sharing, engagement with relevant AI actors, feedback integration, and third-party AI risks.
   **Score:** 0.8128

2. `chunk_id=26` — Explains that AI risk management supports responsible AI development and use by helping organizations consider context and potential positive and negative impacts.
   **Score:** 0.8094

3. `chunk_id=95` — Describes governance accountability structures, including clearly defined roles and responsibilities for mapping, measuring, and managing AI risks, as well as AI risk-management training.
   **Score:** 0.8069

4. `chunk_id=23` — Explicitly states that governance is a **cross-cutting function** designed to inform and be infused throughout MAP, MEASURE, and MANAGE.
   **Score:** 0.8037

5. `chunk_id=92` — Directly discusses how strong governance establishes policies, risk tolerance, organizational culture, documentation, transparency, human review, and accountability.
   **Score:** 0.8032

**Relevant Chunk:** `chunk_id=92`

**Also strongly relevant:** `chunk_id=23`, `chunk_id=95`, `chunk_id=98`

**Best Similarity Score:** `0.8128`

```text
#1  0.8128  ← Strong governance activities and organizational processes
#2  0.8094  ← General AI risk-management context
#3  0.8069  ← Governance accountability and responsibilities
#4  0.8037  ← Explicitly describes governance as cross-cutting
#5  0.8032  ← Directly explains governance's role in policies, culture, and accountability
```

### Observation

This is another useful case for our evaluation.

The **Top-1 result is relevant**, but it focuses on specific GOVERN activities rather than answering the broader question of **what role governance plays**.

The particularly useful result is actually **Top-5 (`chunk_id=92`)**, which explains that governance:

```text
Governance
    ↓
Policies + mission + goals + values + risk tolerance
    ↓
Organizational risk culture
    ↓
AI risk-management practices
    ↓
Transparency + human review + accountability
```

And Top-4 (`chunk_id=23`) gives us another important point: governance is a **cross-cutting function** that informs and is integrated throughout MAP, MEASURE, and MANAGE.

So:

```text
Relevant chunk?  YES
Top-1?            NO
Top-3?            YES
Top-5?            YES
```

**Q8 = successful at Top-3/Top-5, but not ideal Top-1 retrieval.**

---

## Q9 — Identification and Management of AI Risks

**Question:**

> How does the AI RMF describe the identification and management of AI risks?

**Expected Document:** NIST AI RMF 1.0

**Top-5 Retrieved Results:**

1. `chunk_id=31` — Explains that Part 1 of the AI RMF helps organizations **frame the risks related to AI**, while Part 2 provides the Core's four functions — GOVERN, MAP, MEASURE, and MANAGE — to help organizations address AI risks in practice.
   **Score:** 0.8723

2. `chunk_id=153` — Discusses AI risk management in human-AI configurations, including research, evaluation, and understanding human roles and interactions with AI systems.
   **Score:** 0.8660

3. `chunk_id=156` — Describes the AI RMF as a living framework that supports standards, guidelines, best practices, methodologies, and tools for managing AI risks.
   **Score:** 0.8417

4. `chunk_id=24` — Explains that AI risks can emerge in different ways and vary in duration, probability, scale, and impact. It also discusses why AI risks can differ from traditional software risks.
   **Score:** 0.8404

5. `chunk_id=147` — Discusses human roles and responsibilities in AI risk management and the importance of understanding limitations in human-AI interaction.
   **Score:** 0.8400

**Relevant Chunk:** `chunk_id=31`

**Best Similarity Score:** `0.8723`

```text
#1  0.8723  ← Directly explains how the AI RMF frames and addresses AI risks
#2  0.8660  ← Related to AI risk management and human-AI interaction
#3  0.8417  ← General information about managing AI risks
#4  0.8404  ← Explains the nature and characteristics of AI risks
#5  0.8400  ← Related to AI risk management through human-AI interaction
```

### Observation

Q9 is a **strong Top-1 retrieval**.

The Top-1 result gives us the high-level structure:

```text
Part 1
  ↓
Frame AI risks
  ↓
Understand risks + trustworthiness

Part 2 — AI RMF Core
  ↓
GOVERN
MAP
MEASURE
MANAGE
  ↓
Address AI risks in practice
```

The other results are somewhat less direct, but they provide supporting context around the nature of AI risks and how risk management evolves.

So:

```text
Relevant chunk?  YES
Top-1?           YES
Top-3?           YES
Top-5?           YES
```

**Q9 = successful, excellent retrieval.**

We're now at **9/10 questions**. After Q10, we'll have enough results to calculate our initial **Top-1, Top-3, and Top-5 retrieval performance** and identify where the retriever is weak.


---

## Q10 — Validity and Reliability

**Question:**

> What does the AI RMF say about validity and reliability?

**Expected Document:** NIST AI RMF 1.0

**Top-5 Retrieved Results:**

1. `chunk_id=20` — Table of contents showing **“Valid and Reliable”** as section 3.1 under AI Risks and Trustworthiness, but it does not contain the substantive explanation.
   **Score:** 0.7802

2. `chunk_id=31` — Identifies **valid and reliable** as one of the characteristics of trustworthy AI, but provides little detail about what validity and reliability mean.
   **Score:** 0.7792

3. `chunk_id=65` — Directly discusses validity and reliability. It explains that inaccurate, unreliable, or poorly generalized AI systems can increase negative AI risks and reduce trustworthiness. It also defines reliability in terms of performing as required without failure under expected conditions and explains the role of accuracy and robustness in validity and trustworthiness.
   **Score:** 0.7748

4. `chunk_id=153` — Discusses human-AI interaction, evaluation, and AI risk-management approaches, but does not directly address validity and reliability.
   **Score:** 0.7717

5. `chunk_id=83` — Discusses bias and the effectiveness of the AI RMF rather than validity and reliability specifically.
   **Score:** 0.7563

**Relevant Chunk:** `chunk_id=65`

**Best Similarity Score:** `0.7802`

```text
#1  0.7802  ← Mentions Valid and Reliable but is only the table of contents
#2  0.7792  ← Identifies valid and reliable as a trustworthiness characteristic
#3  0.7748  ← Directly explains validity and reliability
#4  0.7717  ← Mostly unrelated to the question
#5  0.7563  ← Mostly about bias and AI RMF effectiveness
```

### Observation

This is our **second clear case where Top-1 retrieval isn't ideal**.

The most important problem is that the **highest-scoring result isn't actually the best answer**:

```text
#1 → chunk 20
     Table of contents
     "3.1 Valid and Reliable"

#2 → chunk 31
     Mentions valid and reliable

#3 → chunk 65
     Actually explains validity and reliability
```

This is particularly useful for our evaluation because it demonstrates that **embedding similarity doesn't guarantee that the highest-scoring chunk contains the best answer**.

The retrieval system did still succeed at Top-3:

```text
Relevant chunk?  YES
Top-1?           NO
Top-3?           YES
Top-5?           YES
```

**Q10 = successful at Top-3/Top-5, but weak Top-1 retrieval.**

---

# Final Evaluation — Q1 to Q10

Now that we have all 10 questions, our initial results are:

| Question | Top-1  | Top-3 | Top-5 | Best Score |
| -------- | ------ | ----- | ----- | ---------: |
| Q1       | Yes    | Yes   | Yes   |     0.8181 |
| Q2       | Yes    | Yes   | Yes   |     0.8762 |
| Q3       | Yes    | Yes   | Yes   |     0.8696 |
| Q4       | Yes    | Yes   | Yes   |     0.7874 |
| Q5       | **No** | Yes   | Yes   |     0.7317 |
| Q6       | Yes    | Yes   | Yes   |     0.8066 |
| Q7       | Yes    | Yes   | Yes   |     0.8450 |
| Q8       | **No** | Yes   | Yes   |     0.8128 |
| Q9       | Yes    | Yes   | Yes   |     0.8723 |
| Q10      | **No** | Yes   | Yes   |     0.7802 |

### Initial retrieval performance

```text
Top-1 = 7/10 = 70%

Top-3 = 10/10 = 100%

Top-5 = 10/10 = 100%
```

This is actually **very useful evidence for the next stage of the project**.

Your current system is doing a good job of getting relevant information into the retrieval set, but **ranking the best chunk first is the main weakness**.

In particular:

* **Q5:** comparison question → relevant information was distributed across multiple chunks.
* **Q8:** broad governance question → strongest explanation appeared at #5.
* **Q10:** table-of-contents chunk outranked the actual explanatory chunk.

That gives us a concrete next problem to solve rather than randomly tuning the similarity threshold.

**The important conclusion:** your current retrieval pipeline has **excellent recall@3/recall@5 on this small ground-truth set, but only 70% Top-1 accuracy.** This is exactly why we started evaluation before moving further into the RAG pipeline.


---

# Evaluation Summary

After completing all 10 questions, summarize the results here.

| Metric | Result |
|---|---:|
| Total Questions | 10 |
| Top-1 Relevant | 7 |
| Top-3 Relevant | 10 |
| Top-5 Relevant | 10 |
| Top-1 Accuracy | 70% |
| Top-3 Accuracy | 100% |
| Top-5 Accuracy | 100% |
| Average Best Score | 0.8200 |

---

# Observations

## What worked well

- All 10 evaluation questions retrieved at least one relevant chunk within the Top-3 results.
- All 10 questions had relevant information within the Top-5 results.
- Top-3 and Top-5 retrieval achieved 100% relevance on this initial evaluation dataset.
- 7 out of 10 questions retrieved the most relevant chunk at Top-1.
- Direct factual questions performed particularly well. For example, questions about the characteristics of trustworthy AI and the four core functions of the AI RMF returned highly relevant chunks at Top-1.
- The workspace filtering and metadata returned with the results allow retrieved chunks to be traced back to their source document.
- The evaluation shows that the current embedding + Qdrant retrieval pipeline is capable of finding relevant information without using a framework such as LangChain.

## Retrieval failures

- Top-1 retrieval was unsuccessful for Q5, Q8, and Q10.
- Q5 asked for a comparison between the MAP and MEASURE functions. Relevant information was retrieved, but the results mainly focused on MEASURE rather than directly explaining the distinction between the two functions.
- Q8 asked about the role of governance. Several relevant governance chunks were retrieved, but the strongest explanation of governance's overall role appeared lower in the ranking rather than at Top-1.
- Q10 retrieved a table-of-contents chunk as Top-1 for the question about validity and reliability. The actual explanatory chunk appeared at position 3.
- Similarity score alone did not always indicate the most useful result. Some lower-scoring chunks contained more directly relevant information than higher-scoring chunks.
- The current evaluation does not include page metadata because page-level metadata was intentionally deferred.

## Possible causes

- The embedding model measures semantic similarity, but does not understand whether a chunk provides the complete answer to a question.
- Some questions require information from multiple chunks rather than a single chunk.
- Table-of-contents and structural text can have high semantic similarity to queries while providing little useful answer content.
- Chunk boundaries can separate related concepts, making it harder for one chunk to contain the complete answer.
- The current retrieval pipeline uses only vector similarity and does not perform reranking.
- The similarity threshold has not yet been calibrated against a sufficiently large evaluation dataset.
- The current evaluation contains only 10 questions and therefore should be treated as an initial baseline rather than a definitive measurement.

## Improvements to investigate

- Improve chunking so that related concepts are kept together where possible.
- Investigate a reranking step after initial vector retrieval.
- Experiment with different `top_k` values and similarity thresholds using the evaluation dataset.
- Add more evaluation questions covering different question types, including factual, comparison, multi-part, and broad conceptual questions.
- Investigate filtering or handling of low-value chunks such as table-of-contents content.
- Add page metadata so retrieved chunks can later support document citations.
- Automate the retrieval evaluation instead of manually checking Top-1, Top-3, and Top-5 results.
- Calculate formal retrieval metrics such as Recall@K and eventually MRR.

---

# Important Question

If the correct chunk appears at position 4 in the Top-5 results, the retrieval system technically retrieved the correct information, but the result is weaker than if it appeared at position 1.

The significance depends on how many chunks we eventually pass to the generation model.

For example:

```text
Top-1
  ↓
Excellent retrieval position

Top-3
  ↓
Usually useful

Top-5
  ↓
Retrieved, but lower ranking

Outside Top-5
  ↓
Not retrieved for a Top-5 RAG pipeline