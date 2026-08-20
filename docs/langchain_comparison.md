# Custom RAG vs LangChain RAG

This experiment compares the project's original custom RAG implementation
with the LangChain-based implementation.

Both implementations use the same:

- Qdrant collection
- embedding model
- source documents
- top-K retrieval
- Ollama LLM

The goal is to understand what LangChain actually abstracts rather than
assuming that using a framework automatically improves retrieval quality.

---

## Architecture Comparison

### Custom RAG

EmbeddingService
↓
Qdrant retrieval
↓
SearchResult
↓
Prompt construction
↓
Ollama
↓
Answer

### LangChain RAG

Embeddings
↓
Qdrant VectorStore
↓
Retriever
↓
LangChain Document
↓
Prompt
↓
Ollama
↓
Answer

---

## Comparison Results

| Question | Custom RAG | LangChain RAG | Retrieval |
|---|---|---|---|
| What are the characteristics of trustworthy AI? | Correct topic, but generated a highly repetitive and overly long answer | Concise list of the seven characteristics | Same relevant NIST chunks |
| What are the four core functions of the AI RMF? | Correctly identified GOVERN, MAP, MEASURE and MANAGE | Correctly identified all four functions | Same top relevant chunk |
| What does the GOVERN function address? | Provided a reasonable explanation focused on roles, responsibilities and decision-making | Provided a detailed explanation of the GOVERN responsibilities | Highly overlapping retrieved chunks |
| What is the difference between MAP and MEASURE? | Partially correct but somewhat vague | Concisely described MAP as risk assessment and MEASURE as quantitative/qualitative analysis | Relevant MAP/MEASURE chunks retrieved |
| What does the AI RMF say about validity and reliability? | General discussion of AI RMF and risk management, but missed the most specific definition | Returned a general AI RMF description rather than the strongest validity/reliability explanation | Relevant chunk containing validity/reliability was retrieved |

---

## Key Observation

The retrieval behavior between the two implementations is very similar.

This is expected because both implementations query the same Qdrant
collection using the same underlying embedding model.

LangChain therefore does not automatically make retrieval more accurate.

Instead, LangChain introduces standardized abstractions such as:

- `Document`
- VectorStore
- Retriever
- PromptTemplate
- Chat model integrations

The experiment shows that the framework mainly reduces the amount of
infrastructure code that needs to be written manually.

---

## What LangChain Actually Saved Us From Writing

Our custom implementation manually handles:

```text
Qdrant search
↓
SearchResult objects
↓
context extraction
↓
prompt construction
↓
LLM invocation

```



================================================================================
QUESTION
What are the characteristics of trustworthy AI?
================================================================================

--- LANGCHAIN DOCUMENT ---
Content: ng characteristics of
trustworthy AI and offers guidance for addressing them. Characteristics of tru
Metadata: {'_id': 59, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: isting and emergent risks.
Page 10

NIST AI 100-1
AI RMF 1.0
Fig. 3. AI actors across AI lifecycle s
Metadata: {'_id': 58, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: aque and uninterpretable systems,
and inaccurate but secure, privacy-enhanced, and transparent syste
Metadata: {'_id': 64, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: plication
context and are performed throughout the AI system lifecycle. See Figure 3
for representat
Metadata: {'_id': 22, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: dth and diversity of
input from interested parties and relevant AI actors throughout the AI lifecycl
Metadata: {'_id': 63, '_collection_name': 'enterprise_documents'}

--- CUSTOM RAG ---
{'answer': 'The characteristics of trustworthy AI include:\n\n1. Valid and reliable\n2. Safe and secure\n3. Resilient and resilient\n4. Accountable and transparent\n5. Explainable and interpretable\n6. Privacy-enhanced\n7. Fair with harmful bias\n8. Managed with privacy and security\n9. Accountable for its purposes\n10. Translucent and open\n11. Accurate and reliable\n12. Transparent and consistent\n13. Diverse and inclusive\n14. Accurate and inclusive\n15. Accurate and transparent\n16. Accurate and diverse\n17. Accurate and inclusive\n18. Accurate and transparent\n19. Accurate and diverse\n20. Accurate and inclusive\n21. Accurate and transparent\n22. Diverse and inclusive\n23. Accurate and transparent\n24. Accountable and transparent\n25. Accountable and diverse\n26. Accountable and inclusive\n27. Accountable and transparent\n28. Accountable and diverse\n29. Accountable and inclusive\n30. Accountable and transparent\n31. Accountable and diverse\n32. Accountable and inclusive\n33. Accountable and transparent\n34. Accountable and diverse\n35. Accountable and inclusive\n36. Accountable and transparent\n37. Accountable and diverse\n38. Accountable and inclusive\n39. Accountable and transparent\n40. Accountable and diverse\n41. Accountable and inclusive\n42. Accountable and transparent\n43. Accountable and diverse\n44. Accountable and inclusive\n45. Accountable and transparent\n46. Accountable and diverse\n47. Accountable and inclusive\n48. Accountable and transparent\n49. Accountable and diverse\n50. Accountable and inclusive\n51. Accountable and transparent\n52. Accountable and diverse\n53. Accountable and inclusive\n54. Accountable and transparent\n55. Accountable and diverse\n56. Accountable and inclusive\n57. Accountable and transparent\n58. Accountable and diverse\n59. Valid & Reliable is a necessary condition of trustworthiness and is shown as the base for other trustworthiness characteristics.\n\nThese characteristics help in balancing each other to ensure AI systems are trustworthy and meet the requirements of their users.', 'sources': [SearchResult(chunk_id=59, content='ng characteristics of\ntrustworthy AI and offers guidance for addressing them. Characteristics of trustworthy AI\nsystems include: valid and reliable, safe, secure and resilient, accountable and trans-\nparent, explainable and interpretable, privacy-enhanced, and fair with harmful bias\nmanaged. Creating trustworthy AI requires balancing each of these characteristics based\non the AI system’s context of use. While all characteristics are socio-technical system at-\ntributes, accountability and transparency also relate to the processes and activities internal\nto an AI system and its external setting. Neglecting these characteristics can increase the\nprobability and magnitude of negative consequences.\nFig. 4. Characteristics of trustworthy AI systems. Valid & Reliable is a necessary condition of\ntrustworthiness and is shown as the base for other trustworthiness characteristics. Accountable &\nTransparent is shown as a vertical box because it relates to all other characteristics.\n', score=0.8762168, document_id=34, chunk_index=42, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=58, content='isting and emergent risks.\nPage 10\n\nNIST AI 100-1\nAI RMF 1.0\nFig. 3. AI actors across AI lifecycle stages. See Appendix A for detailed descriptions of AI actor tasks, including details about testing,\nevaluation, verification, and validation tasks. Note that AI actors in the AI Model dimension (Figure 2) are separated as a best practice, with\nthose building and using the models separated from those verifying and validating the models.\nPage 11\n\nNIST AI 100-1\nAI RMF 1.0\n3.\nAI Risks and Trustworthiness\nFor AI systems to be trustworthy, they often need to be responsive to a multiplicity of cri-\nteria that are of value to interested parties. Approaches which enhance AI trustworthiness\ncan reduce negative AI risks. This Framework articulates the following characteristics of\ntrustworthy AI and offers guidance for addressing them. Characteristics of trustworthy AI\nsystems include: valid and reliable, safe, secure and resilient, accountable and trans-\n', score=0.8261244, document_id=34, chunk_index=41, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=64, content='aque and uninterpretable systems,\nand inaccurate but secure, privacy-enhanced, and transparent systems are all unde-\nsirable. A comprehensive approach to risk management calls for balancing tradeoffs\namong the trustworthiness characteristics. It is the joint responsibility of all AI ac-\ntors to determine whether AI technology is an appropriate or necessary tool for a\ngiven context or purpose, and how to use it responsibly. The decision to commission\nor deploy an AI system should be based on a contextual assessment of trustworthi-\nness characteristics and the relative risks, impacts, costs, and benefits, and informed\nby a broad set of interested parties.\n3.1\nValid and Reliable\nValidation is the “confirmation, through the provision of objective evidence, that the re-\nquirements for a specific intended use or application have been fulfilled” (Source: ISO\n9000:2015). Deployment of AI systems which are inaccurate, unreliable, or poorly gener-\n', score=0.8199266, document_id=34, chunk_index=47, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=22, content='plication\ncontext and are performed throughout the AI system lifecycle. See Figure 3\nfor representative AI actors.\n10\nFig. 3\nAI actors across AI lifecycle stages. See Appendix A for detailed descrip-\ntions of AI actor tasks, including details about testing, evaluation, verifica-\ntion, and validation tasks. Note that AI actors in the AI Model dimension\n(Figure 2) are separated as a best practice, with those building and using the\nmodels separated from those verifying and validating the models.\n11\nFig. 4\nCharacteristics of trustworthy AI systems. Valid & Reliable is a necessary\ncondition of trustworthiness and is shown as the base for other trustworthi-\nness characteristics. Accountable & Transparent is shown as a vertical box\nbecause it relates to all other characteristics.\n12\nFig. 5\nFunctions organize AI risk management activities at their highest level to\ngovern, map, measure, and manage AI risks. Governance is designed to be\n', score=0.79414666, document_id=34, chunk_index=5, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=63, content='dth and diversity of\ninput from interested parties and relevant AI actors throughout the AI lifecycle can en-\nhance opportunities for informing contextually sensitive evaluations, and for identifying\nAI system benefits and positive impacts. These practices can increase the likelihood that\nrisks arising in social contexts are managed appropriately.\nUnderstanding and treatment of trustworthiness characteristics depends on an AI actor’s\nparticular role within the AI lifecycle. For any given AI system, an AI designer or developer\nmay have a different perception of the characteristics than the deployer.\nTrustworthiness characteristics explained in this document influence each other.\nHighly secure but unfair systems, accurate but opaque and uninterpretable systems,\nand inaccurate but secure, privacy-enhanced, and transparent systems are all unde-\nsirable. A comprehensive approach to risk management calls for balancing tradeoffs\n', score=0.789013, document_id=34, chunk_index=46, page_number=None, filename='nist.ai.100-1.pdf')]}

--- LANGCHAIN RAG ---
The characteristics of trustworthy AI include:

1. Valid and Reliable: A necessary condition of trustworthiness and shown as the base for other trustworthiness characteristics.
2. Safe: A vertical box because it relates to all other characteristics.
3. Secure and Resilient: A necessary condition of trustworthiness and shown as the base for other trustworthiness characteristics.
4. Accountable and Transparent: A vertical box because it relates to all other characteristics.
5. Explainable and Interpretable: A necessary condition of trustworthiness and shown as the base for other trustworthiness characteristics.
6. Privacy-enhanced: A necessary condition of trustworthiness and shown as the base for other trustworthiness characteristics.
7. Fair with Harmful Bias Managed: A necessary condition of trustworthiness and shown as the base for other trustworthiness characteristics.

================================================================================
QUESTION
What are the four core functions of the AI RMF?
================================================================================

--- LANGCHAIN DOCUMENT ---
Content: gement with interested parties and relevant AI actors; and
• augmented capacity for TEVV of AI syste
Metadata: {'_id': 86, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: the AI RMF is put into
use, additional lessons will be learned to inform future updates and addition
Metadata: {'_id': 31, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: in conjunction with AI systems.
AI risk management approaches for human-AI configurations will be au
Metadata: {'_id': 153, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: e
9
3
AI Risks and Trustworthiness
12
3.1
Valid and Reliable
13
3.2
Safe
14
3.3
Secure and Resilient
Metadata: {'_id': 20, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: agement resources based on
assessed and prioritized risks. It is incumbent on Framework users to con
Metadata: {'_id': 122, '_collection_name': 'enterprise_documents'}

--- CUSTOM RAG ---
{'answer': 'The four core functions of the AI RMF are:\n1. **GOVERN**: This function aims to provide an overarching framework for discussing AI risks, making them more understandable and actionable for organizations. It is designed to be cross-cutting throughout the other three functions.\n2. **MAP**: This function focuses on mapping out the current state and state of play of AI systems. It identifies areas of potential risk and challenges that need to be addressed.\n3. **MEASURE**: This function involves quantifying and analyzing the current state and state of play of AI systems. It identifies areas of potential risk and challenges that need to be addressed.\n4. **MANAGE**: This function involves taking corrective actions to address identified issues. It includes prioritizing and responding to specific AI risks, and ensuring the development and deployment of AI systems are aligned with organizational objectives.', 'sources': [SearchResult(chunk_id=86, content='gement with interested parties and relevant AI actors; and\n• augmented capacity for TEVV of AI systems and associated risks.\nPage 19\n\nNIST AI 100-1\nAI RMF 1.0\nPart 2: Core and Profiles\n5.\nAI RMF Core\nThe AI RMF Core provides outcomes and actions that enable dialogue, understanding, and\nactivities to manage AI risks and responsibly develop trustworthy AI systems. As illus-\ntrated in Figure 5, the Core is composed of four functions: GOVERN, MAP, MEASURE,\nand MANAGE. Each of these high-level functions is broken down into categories and sub-\ncategories. Categories and subcategories are subdivided into specific actions and outcomes.\nActions do not constitute a checklist, nor are they necessarily an ordered set of steps.\nFig. 5. Functions organize AI risk management activities at their highest level to govern, map,\nmeasure, and manage AI risks. Governance is designed to be a cross-cutting function to inform\nand be infused throughout the other three functions.\n', score=0.86959267, document_id=34, chunk_index=69, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=31, content='the AI RMF is put into\nuse, additional lessons will be learned to inform future updates and additional resources.\nThe Framework is divided into two parts. Part 1 discusses how organizations can frame\nthe risks related to AI and describes the intended audience. Next, AI risks and trustworthi-\nness are analyzed, outlining the characteristics of trustworthy AI systems, which include\nPage 2\n\nNIST AI 100-1\nAI RMF 1.0\nvalid and reliable, safe, secure and resilient, accountable and transparent, explainable and\ninterpretable, privacy enhanced, and fair with their harmful biases managed.\nPart 2 comprises the “Core” of the Framework. It describes four specific functions to help\norganizations address the risks of AI systems in practice. These functions – GOVERN,\nMAP, MEASURE, and MANAGE – are broken down further into categories and subcate-\ngories. While GOVERN applies to all stages of organizations’ AI risk management pro-\n', score=0.8151324, document_id=34, chunk_index=14, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=153, content='in conjunction with AI systems.\nAI risk management approaches for human-AI configurations will be augmented by on-\ngoing research and evaluation. For example, the degree to which humans are empowered\nand incentivized to challenge AI system output requires further studies. Data about the fre-\nquency and rationale with which humans overrule AI system output in deployed systems\nmay be useful to collect and analyze.\nPage 41\n\nNIST AI 100-1\nAI RMF 1.0\nAppendix D:\nAttributes of the AI RMF\nNIST described several key attributes of the AI RMF when work on the Framework first\nbegan. These attributes have remained intact and were used to guide the AI RMF’s devel-\nopment. They are provided here as a reference.\nThe AI RMF strives to:\n1. Be risk-based, resource-efficient, pro-innovation, and voluntary.\n2. Be consensus-driven and developed and regularly updated through an open, trans-\nparent process. All stakeholders should have the opportunity to contribute to the AI\nRMF’s development.\n', score=0.80455595, document_id=34, chunk_index=136, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=20, content='e\n9\n3\nAI Risks and Trustworthiness\n12\n3.1\nValid and Reliable\n13\n3.2\nSafe\n14\n3.3\nSecure and Resilient\n15\n3.4\nAccountable and Transparent\n15\n3.5\nExplainable and Interpretable\n16\n3.6\nPrivacy-Enhanced\n17\n3.7\nFair – with Harmful Bias Managed\n17\n4\nEffectiveness of the AI RMF\n19\nPart 2: Core and Profiles\n20\n5\nAI RMF Core\n20\n5.1\nGovern\n21\n5.2\nMap\n24\n5.3\nMeasure\n28\n5.4\nManage\n31\n6\nAI RMF Profiles\n33\nAppendix A: Descriptions of AI Actor Tasks from Figures 2 and 3\n35\nAppendix B: How AI Risks Differ from Traditional Software Risks\n38\nAppendix C: AI Risk Management and Human-AI Interaction\n40\nAppendix D: Attributes of the AI RMF\n42\nList of Tables\nTable 1 Categories and subcategories for the GOVERN function.\n22\nTable 2 Categories and subcategories for the MAP function.\n26\nTable 3 Categories and subcategories for the MEASURE function.\n29\nTable 4 Categories and subcategories for the MANAGE function.\n32\ni\n\nNIST AI 100-1\nAI RMF 1.0\nList of Figures\nFig. 1\n', score=0.7661985, document_id=34, chunk_index=3, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=122, content='agement resources based on\nassessed and prioritized risks. It is incumbent on Framework users to continue to apply\nthe MANAGE function to deployed AI systems as methods, contexts, risks, and needs or\nexpectations from relevant AI actors evolve over time.\nPage 31\n\nNIST AI 100-1\nAI RMF 1.0\nPractices related to managing AI risks are described in the NIST AI RMF Playbook. Table\n4 lists the MANAGE function’s categories and subcategories.\nTable 4: Categories and subcategories for the MANAGE function.\nMANAGE 1: AI\nrisks based on\nassessments and\nother analytical\noutput from the\nMAP and MEASURE\nfunctions are\nprioritized,\nresponded to, and\nmanaged.\nMANAGE 1.1: A determination is made as to whether the AI\nsystem achieves its intended purposes and stated objectives and\nwhether its development or deployment should proceed.\nMANAGE 1.2: Treatment of documented AI risks is prioritized\nbased on impact, likelihood, and available resources or methods.\n', score=0.76437366, document_id=34, chunk_index=105, page_number=None, filename='nist.ai.100-1.pdf')]}

--- LANGCHAIN RAG ---
The four core functions of the AI RMF are:

1. **GOVERN**
2. **MAP**
3. **MEASURE**
4. **MANAGE**


================================================================================
QUESTION
What does the GOVERN function address?
================================================================================

--- LANGCHAIN DOCUMENT ---
Content: rences, traits, and skills.
The GOVERN function provides organizations with the opportunity to clari
Metadata: {'_id': 151, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: s. Some organizations may choose
to select from among the categories and subcategories; others may c
Metadata: {'_id': 89, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: egory decisions.
5.1
Govern
The GOVERN function:
• cultivates and implements a culture of risk manag
Metadata: {'_id': 90, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: ractice. These functions – GOVERN,
MAP, MEASURE, and MANAGE – are broken down further into categorie
Metadata: {'_id': 32, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: ontext(s) and across the AI lifecycle
are informed by input from domain experts and relevant AI ac-

Metadata: {'_id': 120, '_collection_name': 'enterprise_documents'}

--- CUSTOM RAG ---
{'answer': "The GOVERN function addresses the role and responsibilities for the humans in the Human-AI team configurations and those overseeing the AI system performance. It provides organizations with a clear definition of who should be involved in defining and monitoring the AI system's performance and trustworthiness. The GOVERN function also helps organizations make their decision-making processes more explicit, as it suggests mechanisms for organizations to define and document processes for operator and practitioner proficiency with AI system performance and trustworthiness concepts.", 'sources': [SearchResult(chunk_id=151, content='rences, traits, and skills.\nThe GOVERN function provides organizations with the opportunity to clarify and define\nthe roles and responsibilities for the humans in the Human-AI team configurations and\nthose who are overseeing the AI system performance. The GOVERN function also creates\nmechanisms for organizations to make their decision-making processes more explicit, to\nhelp counter systemic biases.\nThe MAP function suggests opportunities to define and document processes for operator\nand practitioner proficiency with AI system performance and trustworthiness concepts, and\nto define relevant technical standards and certifications. Implementing MAP function cat-\negories and subcategories may help organizations improve their internal competency for\nanalyzing context, identifying procedural and system limitations, exploring and examining\nimpacts of AI-based systems in the real world, and evaluating decision-making processes\nthroughout the AI lifecycle.\n', score=0.7873659, document_id=34, chunk_index=134, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=89, content='s. Some organizations may choose\nto select from among the categories and subcategories; others may choose and have\nthe capacity to apply all categories and subcategories. Assuming a governance struc-\nture is in place, functions may be performed in any order across the AI lifecycle as\ndeemed to add value by a user of the framework. After instituting the outcomes in\nGOVERN, most users of the AI RMF would start with the MAP function and con-\ntinue to MEASURE or MANAGE. However users integrate the functions, the process\nshould be iterative, with cross-referencing between functions as necessary. Simi-\nlarly, there are categories and subcategories with elements that apply to multiple\nfunctions, or that logically should take place before certain subcategory decisions.\n5.1\nGovern\nThe GOVERN function:\n• cultivates and implements a culture of risk management within organizations design-\ning, developing, deploying, evaluating, or acquiring AI systems;\n', score=0.76059633, document_id=34, chunk_index=72, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=90, content='egory decisions.\n5.1\nGovern\nThe GOVERN function:\n• cultivates and implements a culture of risk management within organizations design-\ning, developing, deploying, evaluating, or acquiring AI systems;\n• outlines processes, documents, and organizational schemes that anticipate, identify,\nand manage the risks a system can pose, including to users and others across society\n– and procedures to achieve those outcomes;\n• incorporates processes to assess potential impacts;\n• provides a structure by which AI risk management functions can align with organi-\nzational principles, policies, and strategic priorities;\n• connects technical aspects of AI system design and development to organizational\nvalues and principles, and enables organizational practices and competencies for the\nindividuals involved in acquiring, training, deploying, and monitoring such systems;\nand\n• addresses full product lifecycle and associated processes, including legal and other\n', score=0.7549062, document_id=34, chunk_index=73, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=32, content='ractice. These functions – GOVERN,\nMAP, MEASURE, and MANAGE – are broken down further into categories and subcate-\ngories. While GOVERN applies to all stages of organizations’ AI risk management pro-\ncesses and procedures, the MAP, MEASURE, and MANAGE functions can be applied in AI\nsystem-specific contexts and at specific stages of the AI lifecycle.\nAdditional resources related to the Framework are included in the AI RMF Playbook,\nwhich is available via the NIST AI RMF website:\nhttps://www.nist.gov/itl/ai-risk-management-framework.\nDevelopment of the AI RMF by NIST in collaboration with the private and public sec-\ntors is directed and consistent with its broader AI efforts called for by the National AI\nInitiative Act of 2020, the National Security Commission on Artificial Intelligence recom-\nmendations, and the Plan for Federal Engagement in Developing Technical Standards and\nRelated Tools. Engagement with the AI community during this Framework’s development\n', score=0.7314216, document_id=34, chunk_index=15, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=120, content='ontext(s) and across the AI lifecycle\nare informed by input from domain experts and relevant AI ac-\ntors to validate whether the system is performing consistently as\nintended. Results are documented.\nMEASURE 4.3: Measurable performance improvements or de-\nclines based on consultations with relevant AI actors, in-\ncluding affected communities, and field data about context-\nrelevant risks and trustworthiness characteristics are identified\nand documented.\nCategories\nSubcategories\n5.4\nManage\nThe MANAGE function entails allocating risk resources to mapped and measured risks on\na regular basis and as defined by the GOVERN function. Risk treatment comprises plans to\nrespond to, recover from, and communicate about incidents or events.\nContextual information gleaned from expert consultation and input from relevant AI actors\n– established in GOVERN and carried out in MAP – is utilized in this function to decrease\n', score=0.70874393, document_id=34, chunk_index=103, page_number=None, filename='nist.ai.100-1.pdf')]}

--- LANGCHAIN RAG ---
The GOVERN function addresses the following:

1. Cultivates and implements a culture of risk management within organizations designing, developing, deploying, evaluating, or acquiring AI systems.

2. Outlines processes, documents, and organizational schemes that anticipate, identify, and manage the risks a system can pose, including to users and others across society – and procedures to achieve those outcomes.

3. Incorporates processes to assess potential impacts.

4. Provides a structure by which AI risk management functions can align with organizational principles, policies, and strategic priorities.

5. Connects technical aspects of AI system design and development to organizational values and principles, enabling organizational practices and competencies for individuals involved in acquiring, training, deploying, and monitoring such systems.

6. Addresses full product lifecycle and associated processes, including legal and other practices.


================================================================================
QUESTION
What is the difference between the MAP and MEASURE functions?
================================================================================

--- LANGCHAIN DOCUMENT ---
Content: dge limits. Safety metrics re-
flect system reliability and robustness, real-time monitoring, and
re
Metadata: {'_id': 117, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: ble
3 lists the MEASURE function’s categories and subcategories.
Table 3: Categories and subcategori
Metadata: {'_id': 114, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: rom those external to the team that developed
or deployed the AI system, or other data are identifie
Metadata: {'_id': 110, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: ractice. These functions – GOVERN,
MAP, MEASURE, and MANAGE – are broken down further into categorie
Metadata: {'_id': 32, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: antitative, may need to be
developed. The degree to which each measurement type provides unique and 
Metadata: {'_id': 113, '_collection_name': 'enterprise_documents'}

--- CUSTOM RAG ---
{'answer': 'The MAP function and MEASURE function are related in that they both help to analyze AI risks by collecting data, identifying potential risks, and measuring their impact. The main difference between the two is that the MEASURE function is a specific tool designed to measure and analyze AI risks, while the MAP function is a broader framework that encompasses the MEASURE function, other tools and methods, and processes for risk management and analysis.', 'sources': [SearchResult(chunk_id=117, content='dge limits. Safety metrics re-\nflect system reliability and robustness, real-time monitoring, and\nresponse times for AI system failures.\nMEASURE 2.7: AI system security and resilience – as identified\nin the MAP function – are evaluated and documented.\nMEASURE 2.8: Risks associated with transparency and account-\nability – as identified in the MAP function – are examined and\ndocumented.\nMEASURE 2.9: The AI model is explained, validated, and docu-\nmented, and AI system output is interpreted within its context –\nas identified in the MAP function – to inform responsible use and\ngovernance.\nMEASURE 2.10: Privacy risk of the AI system – as identified in\nthe MAP function – is examined and documented.\nMEASURE 2.11: Fairness and bias – as identified in the MAP\nfunction – are evaluated and results are documented.\nMEASURE 2.12: Environmental impact and sustainability of AI\nmodel training and management activities – as identified in the\nMAP function – are assessed and documented.\n', score=0.7316745, document_id=34, chunk_index=100, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=114, content='ble\n3 lists the MEASURE function’s categories and subcategories.\nTable 3: Categories and subcategories for the MEASURE function.\nMEASURE 1:\nAppropriate\nmethods and metrics\nare identified and\napplied.\nMEASURE 1.1: Approaches and metrics for measurement of AI\nrisks enumerated during the MAP function are selected for imple-\nmentation starting with the most significant AI risks. The risks\nor trustworthiness characteristics that will not – or cannot – be\nmeasured are properly documented.\nMEASURE 1.2: Appropriateness of AI metrics and effectiveness\nof existing controls are regularly assessed and updated, including\nreports of errors and potential impacts on affected communities.\nMEASURE 1.3: Internal experts who did not serve as front-line\ndevelopers for the system and/or independent assessors are in-\nvolved in regular assessments and updates.\nDomain experts,\nusers, AI actors external to the team that developed or deployed\nthe AI system, and affected communities are consulted in support\n', score=0.7305645, document_id=34, chunk_index=97, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=110, content='rom those external to the team that developed\nor deployed the AI system, or other data are identified and\ndocumented.\nCategories\nSubcategories\nContinued on next page\nPage 27\n\nNIST AI 100-1\nAI RMF 1.0\nTable 2: Categories and subcategories for the MAP function. (Continued)\nMAP 5.2: Practices and personnel for supporting regular en-\ngagement with relevant AI actors and integrating feedback about\npositive, negative, and unanticipated impacts are in place and\ndocumented.\nCategories\nSubcategories\n5.3\nMeasure\nThe MEASURE function employs quantitative, qualitative, or mixed-method tools, tech-\nniques, and methodologies to analyze, assess, benchmark, and monitor AI risk and related\nimpacts. It uses knowledge relevant to AI risks identified in the MAP function and informs\nthe MANAGE function. AI systems should be tested before their deployment and regu-\nlarly while in operation. AI risk measurements include documenting aspects of systems’\nfunctionality and trustworthiness.\n', score=0.71570915, document_id=34, chunk_index=93, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=32, content='ractice. These functions – GOVERN,\nMAP, MEASURE, and MANAGE – are broken down further into categories and subcate-\ngories. While GOVERN applies to all stages of organizations’ AI risk management pro-\ncesses and procedures, the MAP, MEASURE, and MANAGE functions can be applied in AI\nsystem-specific contexts and at specific stages of the AI lifecycle.\nAdditional resources related to the Framework are included in the AI RMF Playbook,\nwhich is available via the NIST AI RMF website:\nhttps://www.nist.gov/itl/ai-risk-management-framework.\nDevelopment of the AI RMF by NIST in collaboration with the private and public sec-\ntors is directed and consistent with its broader AI efforts called for by the National AI\nInitiative Act of 2020, the National Security Commission on Artificial Intelligence recom-\nmendations, and the Plan for Federal Engagement in Developing Technical Standards and\nRelated Tools. Engagement with the AI community during this Framework’s development\n', score=0.71421194, document_id=34, chunk_index=15, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=113, content='antitative, may need to be\ndeveloped. The degree to which each measurement type provides unique and meaningful\ninformation to the assessment of AI risks should be considered. Framework users will en-\nhance their capacity to comprehensively evaluate system trustworthiness, identify and track\nexisting and emergent risks, and verify efficacy of the metrics. Measurement outcomes will\nbe utilized in the MANAGE function to assist risk monitoring and response efforts. It is in-\ncumbent on Framework users to continue applying the MEASURE function to AI systems\nas knowledge, methodologies, risks, and impacts evolve over time.\nPage 28\n\nNIST AI 100-1\nAI RMF 1.0\nPractices related to measuring AI risks are described in the NIST AI RMF Playbook. Table\n3 lists the MEASURE function’s categories and subcategories.\nTable 3: Categories and subcategories for the MEASURE function.\nMEASURE 1:\nAppropriate\nmethods and metrics\nare identified and\napplied.\n', score=0.70830745, document_id=34, chunk_index=96, page_number=None, filename='nist.ai.100-1.pdf')]}

--- LANGCHAIN RAG ---
The MAP function is a framework for assessing AI risks, while the MEASURE function employs quantitative, qualitative, or mixed-method tools, techniques, and methodologies to analyze, assess, benchmark, and monitor AI risks and related impacts.


================================================================================
QUESTION
What does the AI RMF say about validity and reliability?
================================================================================

--- LANGCHAIN DOCUMENT ---
Content: e
9
3
AI Risks and Trustworthiness
12
3.1
Valid and Reliable
13
3.2
Safe
14
3.3
Secure and Resilient
Metadata: {'_id': 20, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: the AI RMF is put into
use, additional lessons will be learned to inform future updates and addition
Metadata: {'_id': 31, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content:  evidence, that the re-
quirements for a specific intended use or application have been fulfilled” (
Metadata: {'_id': 65, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: in conjunction with AI systems.
AI risk management approaches for human-AI configurations will be au
Metadata: {'_id': 153, '_collection_name': 'enterprise_documents'}

--- LANGCHAIN DOCUMENT ---
Content: phenomenon, AI sys-
tems can potentially increase the speed and scale of biases and perpetuate and a
Metadata: {'_id': 83, '_collection_name': 'enterprise_documents'}

--- CUSTOM RAG ---
{'answer': 'The AI RMF is designed to provide a structured approach to managing AI risks, emphasizing the importance of validity and reliability in the context of AI systems. It outlines four specific functions to help organizations address the risks of AI systems in practice: GOVERN, MAP, MEASURE, and MANAGE. These functions are broken down further into categories and subcategories, each with specific definitions and criteria for successful implementation. The AI RMF seeks to balance the need for accuracy and robustness with the potential risks associated with AI systems, advocating for a risk-based approach that is resource-efficient, innovation-oriented, and voluntary.', 'sources': [SearchResult(chunk_id=20, content='e\n9\n3\nAI Risks and Trustworthiness\n12\n3.1\nValid and Reliable\n13\n3.2\nSafe\n14\n3.3\nSecure and Resilient\n15\n3.4\nAccountable and Transparent\n15\n3.5\nExplainable and Interpretable\n16\n3.6\nPrivacy-Enhanced\n17\n3.7\nFair – with Harmful Bias Managed\n17\n4\nEffectiveness of the AI RMF\n19\nPart 2: Core and Profiles\n20\n5\nAI RMF Core\n20\n5.1\nGovern\n21\n5.2\nMap\n24\n5.3\nMeasure\n28\n5.4\nManage\n31\n6\nAI RMF Profiles\n33\nAppendix A: Descriptions of AI Actor Tasks from Figures 2 and 3\n35\nAppendix B: How AI Risks Differ from Traditional Software Risks\n38\nAppendix C: AI Risk Management and Human-AI Interaction\n40\nAppendix D: Attributes of the AI RMF\n42\nList of Tables\nTable 1 Categories and subcategories for the GOVERN function.\n22\nTable 2 Categories and subcategories for the MAP function.\n26\nTable 3 Categories and subcategories for the MEASURE function.\n29\nTable 4 Categories and subcategories for the MANAGE function.\n32\ni\n\nNIST AI 100-1\nAI RMF 1.0\nList of Figures\nFig. 1\n', score=0.78023887, document_id=34, chunk_index=3, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=31, content='the AI RMF is put into\nuse, additional lessons will be learned to inform future updates and additional resources.\nThe Framework is divided into two parts. Part 1 discusses how organizations can frame\nthe risks related to AI and describes the intended audience. Next, AI risks and trustworthi-\nness are analyzed, outlining the characteristics of trustworthy AI systems, which include\nPage 2\n\nNIST AI 100-1\nAI RMF 1.0\nvalid and reliable, safe, secure and resilient, accountable and transparent, explainable and\ninterpretable, privacy enhanced, and fair with their harmful biases managed.\nPart 2 comprises the “Core” of the Framework. It describes four specific functions to help\norganizations address the risks of AI systems in practice. These functions – GOVERN,\nMAP, MEASURE, and MANAGE – are broken down further into categories and subcate-\ngories. While GOVERN applies to all stages of organizations’ AI risk management pro-\n', score=0.77917427, document_id=34, chunk_index=14, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=65, content=' evidence, that the re-\nquirements for a specific intended use or application have been fulfilled” (Source: ISO\n9000:2015). Deployment of AI systems which are inaccurate, unreliable, or poorly gener-\nalized to data and settings beyond their training creates and increases negative AI risks and\nreduces trustworthiness.\nReliability is defined in the same standard as the “ability of an item to perform as required,\nwithout failure, for a given time interval, under given conditions” (Source: ISO/IEC TS\n5723:2022). Reliability is a goal for overall correctness of AI system operation under the\nconditions of expected use and over a given period of time, including the entire lifetime of\nthe system.\nPage 13\n\nNIST AI 100-1\nAI RMF 1.0\nAccuracy and robustness contribute to the validity and trustworthiness of AI systems, and\ncan be in tension with one another in AI systems.\nAccuracy is defined by ISO/IEC TS 5723:2022 as “closeness of results of observations,\n', score=0.7748358, document_id=34, chunk_index=48, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=153, content='in conjunction with AI systems.\nAI risk management approaches for human-AI configurations will be augmented by on-\ngoing research and evaluation. For example, the degree to which humans are empowered\nand incentivized to challenge AI system output requires further studies. Data about the fre-\nquency and rationale with which humans overrule AI system output in deployed systems\nmay be useful to collect and analyze.\nPage 41\n\nNIST AI 100-1\nAI RMF 1.0\nAppendix D:\nAttributes of the AI RMF\nNIST described several key attributes of the AI RMF when work on the Framework first\nbegan. These attributes have remained intact and were used to guide the AI RMF’s devel-\nopment. They are provided here as a reference.\nThe AI RMF strives to:\n1. Be risk-based, resource-efficient, pro-innovation, and voluntary.\n2. Be consensus-driven and developed and regularly updated through an open, trans-\nparent process. All stakeholders should have the opportunity to contribute to the AI\nRMF’s development.\n', score=0.77166617, document_id=34, chunk_index=136, page_number=None, filename='nist.ai.100-1.pdf'), SearchResult(chunk_id=83, content='phenomenon, AI sys-\ntems can potentially increase the speed and scale of biases and perpetuate and amplify\nharms to individuals, groups, communities, organizations, and society. Bias is tightly asso-\nciated with the concepts of transparency as well as fairness in society. (For more informa-\ntion about bias, including the three categories, see NIST Special Publication 1270, Towards\na Standard for Identifying and Managing Bias in Artificial Intelligence.)\nPage 18\n\nNIST AI 100-1\nAI RMF 1.0\n4.\nEffectiveness of the AI RMF\nEvaluations of AI RMF effectiveness – including ways to measure bottom-line improve-\nments in the trustworthiness of AI systems – will be part of future NIST activities, in\nconjunction with the AI community.\nOrganizations and other users of the Framework are encouraged to periodically evaluate\nwhether the AI RMF has improved their ability to manage AI risks, including but not lim-\n', score=0.7562502, document_id=34, chunk_index=66, page_number=None, filename='nist.ai.100-1.pdf')]}

--- LANGCHAIN RAG ---
The AI RMF says that it is focused on risk-based, resource-efficient, innovation-driven, and voluntary. It aims to be consensus-driven and regularly updated through an open, transparent process. All stakeholders should have the opportunity to contribute to the AI RMF's development.
PASSED

============================================================ warnings summary =============================================================
.venv\Lib\site-packages\fastapi\testclient.py:1
  D:\batul\project\enterprise-ai-workspace\backend\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

app\services\embedding_service.py:51
  D:\batul\project\enterprise-ai-workspace\backend\app\services\embedding_service.py:51: FutureWarning: The `get_sentence_embedding_dimension` method has been renamed to `get_embedding_dimension`.
    return self.model.get_sentence_embedding_dimension()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================================ 1 passed,