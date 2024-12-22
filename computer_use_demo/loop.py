"""
Agentic sampling loop that calls the Gemini API and local implementation of computer use tools.
"""

import platform
from collections.abc import Callable
from datetime import datetime
from enum import StrEnum
from typing import Any, cast, List
import google.generativeai as genai
import httpx
from google.generativeai.types import  Content, Part, ToolCall, FunctionDeclaration
from google.api_core import exceptions
from .tools import BashTool, ComputerTool, EditTool, ToolCollection, ToolResult


COMPUTER_USE_BETA_FLAG = "computer-use-2024-10-22"
PROMPT_CACHING_BETA_FLAG = "prompt-caching-2024-07-31"


class APIProvider(StrEnum):
    GEMINI = "gemini"


PROVIDER_TO_DEFAULT_MODEL_NAME: dict[APIProvider, str] = {
    APIProvider.GEMINI: "gemini-1.5-pro-latest",
}


# This system prompt is optimized for the environment in this repository and
# specific tool combinations enabled.
# We encourage modifying this system prompt to ensure the model has context for the
# environment it is running in, and to provide any additional information that may be
# helpful for the task at hand.
SYSTEM_PROMPT = f"""<SYSTEM_CAPABILITY>
* You are utilising an Ubuntu virtual machine using {platform.machine()} architecture with internet access.
* You can feel free to install Ubuntu applications with your bash tool. Use curl instead of wget.
* To open firefox, please just click on the firefox icon.  Note, firefox-esr is what is installed on your system.
* Using bash tool you can start GUI applications, but you need to set export DISPLAY=:1 and use a subshell. For example "(DISPLAY=:1 xterm &)". GUI apps run with bash tool will appear within your desktop environment, but they may take some time to appear. Take a screenshot to confirm it did.
* When using your bash tool with commands that are expected to output very large quantities of text, redirect into a tmp file and use str_replace_editor or `grep -n -B <lines before> -A <lines after> <query> <filename>` to confirm output.
* When viewing a page it can be helpful to zoom out so that you can see everything on the page.  Either that, or make sure you scroll down to see everything before deciding something isn't available.
* When using your computer function calls, they take a while to run and send back to you.  Where possible/feasible, try to chain multiple of these calls all into one function calls request.
* The current date is {datetime.today().strftime('%A, %B %-d, %Y')}.
</SYSTEM_CAPABILITY>

<IMPORTANT>
* When using Firefox, if a startup wizard appears, IGNORE IT.  Do not even click "skip this step".  Instead, click on the address bar where it says "Search or enter address", and enter the appropriate search term or URL there.
* If the item you are looking at is a pdf, if after taking a single screenshot of the pdf it seems that you want to read the entire document instead of trying to continue to read the pdf from your screenshots + navigation, determine the URL, use curl to download the pdf, install and use pdftotext to convert it to a text file, and then read that text file directly with your StrReplaceEditTool.
</IMPORTANT>"""


async def sampling_loop(
    *,
    model: str,
    provider: APIProvider,
    system_prompt_suffix: str,
    messages: list[dict],
    output_callback: Callable[[dict], None],
    tool_output_callback: Callable[[ToolResult, str], None],
    api_response_callback: Callable[
        [httpx.Request, httpx.Response | object | None, Exception | None], None
    ],
    api_key: str,
    only_n_most_recent_images: int | None = None,
    max_tokens: int = 4096,
):
    """
    Agentic sampling loop for the assistant/tool interaction of computer use with Gemini API.
    """
    tool_collection = ToolCollection(
        ComputerTool(),
        BashTool(),
        EditTool(),
    )
    system_prompt = f"{SYSTEM_PROMPT}{' ' + system_prompt_suffix if system_prompt_suffix else ''}"
    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel(model)
    
    chat = gemini_model.start_chat(history=[])
    
    def _convert_to_gemini_content(messages: list[dict]) -> list[Content]:
        gemini_contents = []
        for message in messages:
            parts: List[Part] = []
            if isinstance(message['content'], str):
                 parts.append(Part.from_text(message['content']))
            elif isinstance(message['content'], list):
                 for block in message['content']:
                    if isinstance(block, dict):
                         if block.get('type') == 'text':
                            parts.append(Part.from_text(block['text']))
                         if block.get('type') == 'image':
                              try:
                                  parts.append(Part.from_image(data=base64.b64decode(block['source']['data']), mime_type='image/png'))
                              except Exception as e:
                                  print(e)
                                  pass
                    else:
                         parts.append(Part.from_text(str(block)))
            gemini_contents.append(Content(parts=parts, role=message['role']))
        return gemini_contents
    
    
    while True:
        gemini_messages = _convert_to_gemini_content(messages)
        chat.history = gemini_messages
        
        tools = tool_collection.to_params()
        function_declarations = [FunctionDeclaration(**tool) for tool in tools]
        
        try:
            response = chat.send_message(
                system_prompt,
                tools=function_declarations,
            )

            api_response_callback(
                response.raw_response.request, response.raw_response.response, None
            )
            
        except exceptions.GoogleAPIError as e:
             api_response_callback(e.request, e.response, e)
             return messages
         
        
        if response.candidates[0].content.parts and  len(response.candidates[0].content.parts) > 0:
            response_params = []
            for part in response.candidates[0].content.parts:
                 if isinstance(part, str):
                      response_params.append({"type":"text", "text": part})
                 elif isinstance(part, ToolCall):
                       response_params.append(part.function_call)
            
            messages.append(
                {
                    "role": "assistant",
                    "content": response_params,
                }
            )
        
            tool_result_content = []
            for content_block in response_params:
                 if content_block.get('name'):
                    output_callback(content_block)
                    result = await tool_collection.run(
                         name=content_block["name"],
                         tool_input=cast(dict[str, Any], content_block["arguments"]),
                    )
                    tool_result_content.append(
                         _make_api_tool_result(result, content_block.get('name'))
                    )
                    tool_output_callback(result, content_block.get('name'))

            if not tool_result_content:
                return messages

            messages.append({"content": tool_result_content, "role": "user"})
        else:
            return messages


def _make_api_tool_result(
    result: ToolResult, tool_use_id: str
) -> dict:
    """Convert an agent ToolResult to an API ToolResultBlockParam."""
    tool_result_content: list[dict] | str = []
    is_error = False
    if result.error:
        is_error = True
        tool_result_content = _maybe_prepend_system_tool_result(result, result.error)
    else:
        if result.output:
             tool_result_content.append(
                 {
                     "type": "text",
                     "text": _maybe_prepend_system_tool_result(result, result.output),
                 }
             )
        if result.base64_image:
             tool_result_content.append(
                {
                     "type": "image",
                     "source": {
                         "type": "base64",
                         "media_type": "image/png",
                         "data": result.base64_image,
                     },
                }
             )
    return {
        "type": "tool_result",
        "content": tool_result_content,
        "tool_use_id": tool_use_id,
        "is_error": is_error,
    }


def _maybe_prepend_system_tool_result(result: ToolResult, result_text: str):
    if result.system:
        result_text = f"<system>{result.system}</system>\n{result_text}"
    return result_text