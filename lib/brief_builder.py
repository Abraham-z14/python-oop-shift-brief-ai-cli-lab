class HandoffBriefBuilder:
    """Builds prompts and verifies output for shift handoff briefs."""

    REQUIRED_SECTIONS = (
        "Shift Summary:",
        "Open Issues:",
        "Action Items:",
        "Follow-Up Questions:",
        "Risk Notes:",
    )

    def build_brief_prompt(self, notes):
        if not isinstance(notes, str) or not notes.strip():
            raise ValueError("Shift notes cannot be empty")

        cleaned_notes = notes.strip()

        sections = "\n".join(self.REQUIRED_SECTIONS)

        return (
            "Create a clear shift handoff brief using only the shift notes below.\n"
            "Do not invent or make up unsupported details.\n"
            'If information is not provided, use "Unknown".\n\n'
            "Use exactly these section labels:\n"
            f"{sections}\n\n"
            "Shift notes:\n"
            f"{cleaned_notes}"
        )

    def build_revision_prompt(self, feedback):
        if not isinstance(feedback, str) or not feedback.strip():
            raise ValueError("Revision feedback cannot be empty")

        cleaned_feedback = feedback.strip()

        sections = "\n".join(self.REQUIRED_SECTIONS)

        return (
            "Revise the previous shift handoff brief using the manager's "
            "revision feedback below.\n"
            "Use the previous conversation for context.\n"
            "Do not invent or make up unsupported details.\n\n"
            "Keep exactly these section labels:\n"
            f"{sections}\n\n"
            "Revision feedback:\n"
            f"{cleaned_feedback}"
        )

    def is_usable_brief(self, response_text):
        if not isinstance(response_text, str) or not response_text.strip():
            return False

        return all(
            section in response_text
            for section in self.REQUIRED_SECTIONS
        )

    def format_brief(self, response_text):
        return f"\nShift Handoff Brief\n\n{response_text}"

    def create_brief(self, ai_client, notes):
        prompt = self.build_brief_prompt(notes)
        response = ai_client.send(prompt)

        if not self.is_usable_brief(response):
            raise RuntimeError(
                "AI response did not include required sections"
            )

        return self.format_brief(response)

    def revise_brief(self, ai_client, feedback):
        prompt = self.build_revision_prompt(feedback)
        response = ai_client.send(prompt)

        if not self.is_usable_brief(response):
            raise RuntimeError(
                "AI response did not include required sections"
            )

        return f"\nRevised Shift Handoff Brief\n\n{response}"