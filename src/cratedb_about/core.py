# Derived from: https://llmstxt.org/domains.html
import dataclasses
import os
import typing as t

from cratedb_about.model import Settings


@dataclasses.dataclass
class CrateDBConversation:
    """
    Manage conversations about CrateDB.
    """

    backend: t.Literal["claude", "openai"] = "openai"
    use_knowledge: bool = True

    def ask(self, question: str) -> str:
        if self.backend == "openai":
            return self.ask_gpt(question)
        if self.backend == "claude":
            return self.ask_claude(question)
        raise NotImplementedError("Please select an available LLM backend")

    def ask_claude(self, question: str) -> str:
        from claudette import Chat, contents, models

        model = models[1]  # Sonnet 3.5
        chat = Chat(model, sp=Settings.instructions)
        chat(Settings.get_prompt())
        result = chat(question)
        return contents(result)

    def ask_gpt(self, question: str) -> str:
        """
        Ask the machine, enriched with CrateDB context, catalyzed through OpenAI's GPT.

        Models like o3 and o4-mini are reasoning models.
        https://platform.openai.com/docs/guides/reasoning

        The OpenAI API provides different kinds of roles for messages. Let's use the
        `developer` role to relay information on top of the user's question.

        - https://community.openai.com/t/the-system-role-how-it-influences-the-chat-behavior/87353
        - https://community.openai.com/t/understanding-role-management-in-openais-api-two-methods-compared/253289
        - https://community.openai.com/t/how-is-developer-message-better-than-system-prompt/1062784
        """
        from openai import OpenAI
        from openai.types.responses import ResponseInputTextParam
        from openai.types.shared_params import Reasoning

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        from openai.types.responses.response_input_param import Message

        response = client.responses.create(
            # model="gpt-4o",  # noqa: ERA001
            model="o4-mini",
            reasoning=Reasoning(
                effort="medium",
                # Your organization must be verified to generate reasoning summaries
                # summary="detailed",  # noqa: ERA001
            ),
            instructions=Settings.instructions,
            input=[
                Message(
                    content=[ResponseInputTextParam(text=Settings.get_prompt(), type="input_text")],
                    role="developer",
                    status="completed",
                    type="message",
                ),
                Message(
                    content=[ResponseInputTextParam(text=question, type="input_text")],
                    role="user",
                    status="completed",
                    type="message",
                ),
            ],
        )
        return response.output_text
