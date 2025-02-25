import os
import google.genai as genai
from google.genai import types
from google.genai.types import Part

from typing import Optional


class LLMMessenger(object):
    def __init__(self):
        self.client = genai.Client()

    def _get_hypothesis_instructions(self, file_path: str) -> types.ContentUnion:
        """Read and package prompt instructions as
        appropriate for Gemeni

        Args:
            file_path (str): path to prompt instruction text file

        Returns:
            types.ContentUnion: prompt instructions
        """
        instructions = []

        with open(os.path.relpath(file_path), "r") as f:
            for line in f.readlines():
                if not line.strip():
                    continue
                instructions.append(line.strip())
        return instructions

    def _create_generation_config(
        self,
        system_instructions: Optional[list[str]] = None,
    ) -> types.GenerateContentConfig:
        config = types.GenerateContentConfig(
            system_instruction=system_instructions,
        )
        return config

    def _build_contents(self, query: list[str], context: list[str]) -> list[Part]:
        # Context has to be formed into a single string
        if len(context) > 1:
            context = " ".join(context)
        return [Part(text=context), Part(text=query)]

    def generate_response(
        self,
        query: list[str],
        model_specification: str = "models/gemini-1.5-flash",
        context: Optional[list[str]] = None,
        instructions: Optional[types.ContentUnion] = None,
    ):
        config = (
            self._create_generation_config(system_instructions=instructions)
            if instructions
            else None
        )
        contents = (
            self._build_contents(query=query, context=context)
            if context
            else [Part(text=query)]
        )
        response = self.client.models.generate_content(
            model=model_specification,
            contents=contents,
            config=config,
        )
        return response
