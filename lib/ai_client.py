import ollama


class OllamaChatClient:
    """Generic reusable client for interacting with a local chat model service."""

    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name
        self.history = []

    def send(self, prompt):
        # Reject missing, empty, or whitespace-only prompts.
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        cleaned_prompt = prompt.strip()

        user_message = {
            "role": "user",
            "content": cleaned_prompt,
        }

        # Save the user message before making the service call.
        self.history.append(user_message)

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=self.history,
            )

            # Support dictionary-style responses.
            if isinstance(response, dict):
                message = response.get("message")

                if not isinstance(message, dict):
                    raise ValueError("Invalid assistant response")

                content = message.get("content")

            # Support object-style responses.
            else:
                message = getattr(response, "message", None)

                if message is None:
                    raise ValueError("Invalid assistant response")

                content = getattr(message, "content", None)

            # Assistant content must be a usable string.
            if not isinstance(content, str) or not content.strip():
                raise ValueError("Invalid assistant response")

            cleaned_content = content.strip()

            assistant_message = {
                "role": "assistant",
                "content": cleaned_content,
            }

            self.history.append(assistant_message)

            return cleaned_content

        except Exception as error:
            # Remove only the failed user message.
            if self.history and self.history[-1] == user_message:
                self.history.pop()

            raise RuntimeError(
                f"AI service request failed: {error}"
            ) from error

    def reset(self):
        self.history = []

    def message_count(self):
        return len(self.history)

    def get_transcript(self):
        return [
            message.copy()
            for message in self.history
        ]