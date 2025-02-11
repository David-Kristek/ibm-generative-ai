from typing import Literal, Optional, Union
from warnings import warn

from pydantic import BaseModel, ConfigDict, Field

from genai.schemas import Descriptions as tx

# API Reference : https://workbench.res.ibm.com/docs


class LengthPenalty(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid", protected_namespaces=())

    decay_factor: Optional[float] = Field(None, description=tx.DECAY_FACTOR, gt=1.00)
    start_index: Optional[int] = Field(None, description=tx.START_INDEX)


class ReturnOptions(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=False, extra="forbid", protected_namespaces=())

    input_text: Optional[bool] = Field(None, description=tx.INPUT_TEXT)
    generated_tokens: Optional[bool] = Field(None, description=tx.GENERATED_TOKEN)
    input_tokens: Optional[bool] = Field(None, description=tx.INPUT_TOKEN)
    token_logprobs: Optional[bool] = Field(None, description=tx.TOKEN_LOGPROBS)
    token_ranks: Optional[bool] = Field(None, description=tx.TOKEN_RANKS)
    top_n_tokens: Optional[int] = Field(None, description=tx.TOP_N_TOKENS)


class Return(ReturnOptions):
    def __init__(self, *args, **kwargs):
        warn(DeprecationWarning(f"{self.__class__.__name__} is deprecated, please use ReturnOptions instead."))
        super().__init__(*args, **kwargs)


# NOTE - The "return" parameter is deprecated, please use return_options now.
# Context   : The GENAI Service endpoint has an optional parameter named "return".
# Issue     : "return" is a reserved keyword, so we can't directly use it as an
#             attribute of Generate.
# Fix       : We created a "returns" attribute which gets mapped to the "return"
#             dictionary key in the sanitize method of ServiceInterface.
# Link to doc : https://workbench.res.ibm.com/docs/api-reference#generate


class ModerationTypeOptions(BaseModel):
    input: bool = Field(description=tx.MODERATION_TYPE_INPUT, default=True)
    output: bool = Field(description=tx.MODERATION_TYPE_OUTPUT, default=True)
    threshold: float = Field(description=tx.MODERATION_TYPE_THRESHOLD, ge=0, le=1, multiple_of=0.01, default=0.75)


class HAPOptions(ModerationTypeOptions):
    pass


class StigmaOptions(ModerationTypeOptions):
    pass


class ImplicitHateOptions(ModerationTypeOptions):
    pass


class ModerationsOptions(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    hap: Union[bool, HAPOptions] = Field(description=tx.MODERATION_HAP, default=False)
    stigma: Union[bool, StigmaOptions] = Field(description=tx.MODERATION_STIGMA, default=False)
    implicit_hate: Union[bool, ImplicitHateOptions] = Field(description=tx.MODERATION_IMPLICIT_HATE, default=False)


class GenerateParams(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=False, extra="allow", populate_by_name=True, protected_namespaces=())

    decoding_method: Optional[Literal["greedy", "sample"]] = Field(None, description=tx.DECODING_METHOD)
    length_penalty: Optional[LengthPenalty] = Field(None, description=tx.LENGTH_PENALTY)
    max_new_tokens: Optional[int] = Field(None, description=tx.MAX_NEW_TOKEN, ge=1)
    min_new_tokens: Optional[int] = Field(None, description=tx.MIN_NEW_TOKEN, ge=0)
    random_seed: Optional[int] = Field(None, description=tx.RANDOM_SEED, ge=1)
    stop_sequences: Optional[list[str]] = Field(None, description=tx.STOP_SEQUENCES, min_length=1)
    stream: Optional[bool] = Field(None, description=tx.STREAM)
    temperature: Optional[float] = Field(None, description=tx.TEMPERATURE, ge=0.05, le=2.00)
    time_limit: Optional[int] = Field(None, description=tx.TIME_LIMIT)
    top_k: Optional[int] = Field(None, description=tx.TOP_K, ge=1)
    top_p: Optional[float] = Field(None, description=tx.TOP_P, ge=0.00, le=1.00)
    typical_p: Optional[float] = Field(None, description=tx.TYPICAL_P, gt=0.00, le=1.00)
    repetition_penalty: Optional[float] = Field(
        None, description=tx.REPETITION_PENALTY, multiple_of=0.01, ge=1.00, le=2.00
    )
    truncate_input_tokens: Optional[int] = Field(None, description=tx.TRUNCATE_INPUT_TOKENS, ge=0)
    beam_width: Optional[int] = Field(None, description=tx.BEAM_WIDTH, ge=0)
    return_options: Optional[ReturnOptions] = Field(None, description=tx.RETURN)
    returns: Optional[Return] = Field(
        None, description=tx.RETURN, alias="return", json_schema_extra={"deprecated": True}
    )
    moderations: Optional[ModerationsOptions] = Field(None, description=tx.MODERATIONS)
    include_stop_sequence: Optional[bool] = Field(None, description=tx.INCLUDE_STOP_SEQUENCE)


class ChatOptions(BaseModel):
    conversation_id: Optional[str] = None
    parent_id: Optional[str] = None
    prompt_id: Optional[str] = None
    template_id: Optional[str] = None
    use_conversation_parameters: Optional[bool] = False
