# Derived from: https://llmstxt.org/domains.html
import dataclasses
import os
import sys
import typing as t

from cratedb_about.query.model import CrateDbKnowledgeContextLoader, KnowledgeContextLoader

# Import backends conditionally to avoid errors if dependencies are missing
CLAUDE_AVAILABLE = False
OPENAI_AVAILABLE = False

try:
    from claudette import Chat, contents, models

    CLAUDE_AVAILABLE = True
except ImportError:
    pass

try:
    from openai import OpenAI
    from openai.types.responses import ResponseInputTextParam
    from openai.types.responses.response_input_param import Message
    from openai.types.shared_params import Reasoning

    OPENAI_AVAILABLE = True
except ImportError:
    pass


@dataclasses.dataclass
class CrateDbKnowledgeConversation:
    """
    Manage conversations about CrateDB.

    Requires:
    - OPENAI_API_KEY environment variable when using "openai" backend
    - ANTHROPIC_API_KEY environment variable when using "claude" backend
    """

    backend: t.Literal["claude", "openai"] = "openai"
    use_knowledge: bool = True
    context: KnowledgeContextLoader = dataclasses.field(
        default_factory=CrateDbKnowledgeContextLoader
    )

    def __post_init__(self):
        """Validate configuration."""
        if self.backend == "openai" and not OPENAI_AVAILABLE:
            raise ImportError("The 'openai' package is required when using the OpenAI backend")
        if self.backend == "claude" and not CLAUDE_AVAILABLE:
            raise ImportError("The 'claudette' package is required when using the Claude backend")
        if self.backend == "openai" and not os.environ.get("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY environment variable is required when using 'openai' backend"
            )
        if self.backend == "claude" and not os.environ.get("ANTHROPIC_API_KEY"):
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable is required when using 'claude' backend"
            )

    def ask(self, question: str) -> str:
        """
        Ask a question about CrateDB using the configured LLM backend.

        Args:
            question: The question to ask about CrateDB

        Returns:
            str: The response from the LLM

        Raises:
            NotImplementedError: If an unsupported backend is specified
            ValueError: If required environment variables are missing
            RuntimeError: If there's an error communicating with the LLM API
        """
        if self.backend == "openai":
            return self.ask_gpt(question)
        if self.backend == "claude":
            return self.ask_claude(question)
        raise NotImplementedError("Please select an available LLM backend")

    def ask_claude(self, question: str) -> str:
        # FIXME: API does not provide lookup by name.
        model = models[1]  # Sonnet 3.5
        chat = Chat(model, sp=self.context.instructions)
        if self.use_knowledge:
            try:
                chat(self.context.get_prompt())
            except Exception as e:
                print(f"Warning: Failed to load knowledge context: {e}", file=sys.stderr)  # noqa: T201
        try:
            result = chat(question)
            return contents(result)
        except Exception as e:
            raise RuntimeError(f"Claude API error: {e}") from e

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

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        input_messages: t.List[Message] = []

        # Optionally add topic domain knowledge.
        if self.use_knowledge:
            try:
                prompt = self.context.get_prompt()
                input_messages.append(
                    Message(
                        content=[ResponseInputTextParam(text=prompt, type="input_text")],
                        role="developer",
                        status="completed",
                        type="message",
                    )
                )
            except Exception as e:
                print(f"Warning: Failed to load knowledge context: {e}", file=sys.stderr)  # noqa: T201

        # Always add the user question.
        input_messages.append(
            Message(
                content=[ResponseInputTextParam(text=question, type="input_text")],
                role="user",
                status="completed",
                type="message",
            )
        )

        # model = "gpt-4o"  # noqa: ERA001
        model = "gpt-4.1"  # noqa: ERA001
        # model = "o4-mini"  # noqa: ERA001
        # model = "o3"  # noqa: ERA001
        reasoning = None
        if model == "o4-mini":
            reasoning = Reasoning(
                effort="high",
                # Your organization must be verified to generate reasoning summaries
                # summary="detailed",  # noqa: ERA001
            )

        response = client.responses.create(
            model=model,
            reasoning=reasoning,
            instructions=self.context.instructions,
            input=input_messages,  # type: ignore[arg-type]
        )
        return response.output_text
