# from app.core.dependencies import llm_service


class QueryTransformer:
    """
    Rewrites conversational user queries into standalone
    queries suitable for document retrieval.
    """

    # REWRITE_PROMPT = """
    #     You are a query rewriting component for a document retrieval system.

    #     Your task is to rewrite the user's latest query into a
    #     self-contained search query.

    #     Use the conversation history to resolve:
    #     - pronouns such as "it", "this", "that", "they"
    #     - references such as "the second one"
    #     - omitted subjects
    #     - references to previously discussed entities

    #     Rules:
    #     1. Preserve the original intent.
    #     2. Do not answer the question.
    #     3. Do not add information that is not supported by the conversation.
    #     4. If the query is already self-contained, keep its meaning unchanged.
    #     5. Return ONLY the rewritten query.
    #     6. Do not add explanations, quotes, or prefixes.

    #     Conversation history:
    #     {conversation_history}

    #     Latest user query:
    #     {query}

    #     Standalone search query:
    #     """

    REWRITE_PROMPT = """
        You are a query rewriting component for a document retrieval system.

        Your job is NOT to answer the question.

        Your job is to convert the user's latest message into a
        SELF-CONTAINED search query that can be understood WITHOUT
        the conversation history.

        IMPORTANT:
        - The latest message may be incomplete.
        - Resolve pronouns such as "it", "this", "that", "they".
        - Resolve references such as "the first one", "the second one",
        "the previous one", "that product".
        - Use the conversation history to determine what those references mean.
        - If the latest query refers to something discussed previously,
        explicitly include that entity in the rewritten query.
        - Do not simply repeat an ambiguous query.
        - Do not invent information that is not present in the conversation.
        - Do not answer the question.
        - Return ONLY the rewritten search query.

        Example:

        Conversation:
        User: What are the loan products?
        Assistant: There are three products: Personal Loan, Home Loan and Auto Loan.

        Latest query:
        What about the second one?

        Rewritten query:
        What are the details of the Home Loan?

        Now perform the same transformation.

        Conversation history:
        {conversation_history}

        Latest user query:
        {query}

        Rewritten query:
        """

    def __init__(self, llm_service):
        self.llm_service = llm_service

    def rewrite(
        self,
        query: str,
        conversation_history: list[dict] | None = None,
    ) -> str:
        """
        Rewrite a conversational query into a standalone
        retrieval query.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        conversation_history = conversation_history or []

        history_text = self._format_history(conversation_history)

        prompt = self.REWRITE_PROMPT.format(
            conversation_history=history_text,
            query=query.strip(),
        )
        
        # print("\n========== QUERY REWRITE PROMPT ==========")
        # print(prompt)
        # print("==========================================\n")

        rewritten_query = self.llm_service.generate(prompt)

        if not rewritten_query or not rewritten_query.strip():
            raise ValueError("Query transformer returned an empty query.")

        return rewritten_query.strip()

    @staticmethod
    def _format_history(
        conversation_history: list[dict],
    ) -> str:
        if not conversation_history:
            return "No previous conversation."

        messages = []

        for message in conversation_history:
            role = message.get("role", "unknown")
            content = message.get("content", "")

            if content:
                messages.append(f"{role}: {content}")

        return "\n".join(messages)
