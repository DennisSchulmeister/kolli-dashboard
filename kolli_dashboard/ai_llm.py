# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

import asyncio
import os

from collections.abc import AsyncIterator
from typing import cast

from openai import AsyncOpenAI, OpenAI
from openai.types.chat import ChatCompletionMessageParam

from shiny import reactive

def ai_conversation_available():
    try:
        return True if os.environ["LLM_OPENAI_API_KEY"] else False
    except KeyError:
        return False

def ai_message(
    text: str,
    messages: list[ChatCompletionMessageParam] | None = None,
) -> list[ChatCompletionMessageParam]:
    if messages is None:
        messages = [
            cast(ChatCompletionMessageParam, {
                "role": "system",
                "content": "Wir haben verschiedene Umfragen unter den Studierenden gemacht, "
                           "weil wir die Studierenden partizipativ in die Umsetzung von Lehr-Lern-Innovationen "
                           "einbeziehen wollen. Wir nennen dies Kooperative Lehr-Lern-Innovationen. "
                           "Bitte hilf uns bei der Beantwortung folgender Fragen zur Auswertung der Ergebnisse.",
            })
        ]

    messages.append(cast(ChatCompletionMessageParam, {
        "role": "user",
        "content": text,
    }))

    return messages

def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise KeyError(name)
    return value

def _openai_base_url() -> str:
    base_url = os.environ.get("LLM_OPENAI_BASE_URL")
    if base_url:
        return base_url.rstrip("/")

    host = _require_env("LLM_OPENAI_HOST")
    path = os.environ.get("LLM_OPENAI_PATH", "")

    # LLM_OPENAI_PATH historically points to the full endpoint (e.g. /v1/chat/completions).
    # The OpenAI SDK expects a base URL that ends with /v1.
    if "/v1" in path:
        prefix = path.split("/v1", 1)[0] + "/v1"
    else:
        prefix = "/v1"

    return f"https://{host}{prefix}"

def ai_conversation(messages: list[ChatCompletionMessageParam]) -> str:
    client = OpenAI(
        api_key=_require_env("LLM_OPENAI_API_KEY"),
        base_url=_openai_base_url(),
    )

    try:
        response = client.chat.completions.create(
            model=_require_env("LLM_OPENAI_MODEL"),
            messages=messages,
        )
        return response.choices[0].message.content or ""
    except Exception as error:
        return f"Fehler beim Aufruf der OpenAI API. Die Antwort war: {error}"


async def ai_conversation_stream(messages: list[ChatCompletionMessageParam]) -> AsyncIterator[str]:
    client = AsyncOpenAI(
        api_key=_require_env("LLM_OPENAI_API_KEY"),
        base_url=_openai_base_url(),
    )

    accumulated = ""

    try:
        stream = await client.chat.completions.create(
            model=_require_env("LLM_OPENAI_MODEL"),
            messages=messages,
            stream=True,
        )

        async for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            if not delta:
                continue
            accumulated += delta
            yield accumulated
    except Exception as error:
        yield f"Fehler beim Aufruf der OpenAI API. Die Antwort war: {error}"

ai_stream_tasks: dict[str, asyncio.Task] = {}


def cancel_ai_stream(task_name: str) -> None:
    task = ai_stream_tasks.get(task_name)
    if task is None:
        return

    task.cancel()
    # Remove immediately so a new task can be started right away.
    if ai_stream_tasks.get(task_name) is task:
        del ai_stream_tasks[task_name]

def start_ai_stream(*, question: str, target_md: reactive.Value, task_name: str) -> None:
    current_task = ai_stream_tasks.get(task_name)

    if current_task is not None:
        current_task.cancel()

    async def _run_stream():
        try:
            target_md.set("(Antwort wird generiert …)")
            async for partial in ai_conversation_stream(ai_message(question)):
                target_md.set(partial)
                await reactive.flush()
                await asyncio.sleep(0)
        except asyncio.CancelledError:
            raise

    task = asyncio.create_task(_run_stream())

    ai_stream_tasks[task_name] = task

    def _on_done(done_task: asyncio.Task):
        if ai_stream_tasks.get(task_name) is done_task:
            del ai_stream_tasks[task_name]

    task.add_done_callback(_on_done)