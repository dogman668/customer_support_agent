from openai import OpenAI
from vector_store import VectorStore
from tools import get_order_status, create_ticket
from config import MODEL, ESCALATE_THRESHOLD

client = OpenAI()

class CustomerSupportAgent:
    def __init__(self):
        self.vector_store = VectorStore()
        self.fail_count = 0

    def detect_intent(self, user_input):
        if "订单" in user_input:
            return "order"
        elif "人工" in user_input:
            return "human"
        return "faq"

    def handle_tools(self, intent, user_input):
        if intent == "order":
            order_id = "".join(filter(str.isdigit, user_input))
            return get_order_status(order_id)

        if intent == "human":
            return create_ticket(user_input)

        return None

    def retrieve_knowledge(self, user_input):
        results = self.vector_store.search(user_input)
        context = "\n".join([r["answer"] for r in results])
        return context

    def generate_response(self, user_input):
        intent = self.detect_intent(user_input)

        tool_result = self.handle_tools(intent, user_input)
        if tool_result:
            return tool_result

        context = self.retrieve_knowledge(user_input)

        prompt = f"""你是一个客服助手，请根据知识库回答用户问题。

知识库：
{context}

用户问题：
{user_input}
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "你是一个专业客服"},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

        if "不知道" in answer or len(answer) < 5:
            self.fail_count += 1
        else:
            self.fail_count = 0

        if self.fail_count >= ESCALATE_THRESHOLD:
            return create_ticket(user_input)

        return answer
