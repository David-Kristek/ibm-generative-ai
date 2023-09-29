import logging

try:
    from transformers import Agent
except ImportError:
    raise ImportError(
        "Could not import HuggingFace transformers: Please install ibm-generative-ai[huggingface] extension."
    )


from typing import List, Optional

from genai import Credentials, Model
from genai.schemas import GenerateParams
from genai.utils.extensions import enforce_stop_tokens

logger = logging.getLogger(__name__)


class GenaiAgent(Agent):
    """
    Class that extends the functionality of the Hugging Face Transformers' Agent class.
    It uses Genai models as agents that select appropriate tools and then generate code.
    """

    def __init__(
        self,
        credentials: Credentials = None,
        model: Optional[str] = None,
        params: Optional[GenerateParams] = None,
        chat_prompt_template: Optional[str] = None,
        run_prompt_template: Optional[str] = None,
        additional_tools: Optional[List[str]] = None,
    ):
        super().__init__(
            chat_prompt_template=chat_prompt_template,
            run_prompt_template=run_prompt_template,
            additional_tools=additional_tools,
        )
        self.credentials = credentials
        self.model = model
        self.params = params

    def generate_one(self, prompt, stop):
        return self._generate([prompt], stop)[0]

    def generate_many(self, prompts, stop):
        return self._generate(prompts, stop)

    def _generate(self, prompts: List[str], stop: Optional[List[str]] = None) -> List[str]:
        result: List[str] = []
        if len(prompts) == 0:
            return result

        params = self.params or GenerateParams()
        params.stop_sequences = stop or params.stop_sequences
        model = Model(model=self.model, params=params, credentials=self.credentials)
        for response in model.generate(prompts=prompts):
            if params.stop_sequences:
                response.generated_text = enforce_stop_tokens(response.generated_text, params.stop_sequences)

            generated_text = response.generated_text
            logger.info("Output of GENAI call: {}".format(generated_text))
            result.append(generated_text)

        return result
