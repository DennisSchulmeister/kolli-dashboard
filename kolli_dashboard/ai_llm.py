# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

import http.client, json, os 

def ai_conversation_available():
    try:
        return True if os.environ["LLM_OPENAI_API_KEY"] else False
    except KeyError:
        return False

def ai_message(text, messages=None):
    if not messages:
        messages = [
            {
                "role": "system",
                "content": "Wir haben verschiedene Umfragen unter Lehrenden und Studierenden gemacht, "
                           "weil wir Studierende partizipativ in die Umsetzung von Lehr-Lern-Innovationen "
                           "einbeziehen wollen. Wir nennen dies Kooperative Lehr-Lern-Innovationen. "
                           "Bitte hilf uns bei der Beantwortung folgender Fragen zur Auswertung der Ergebnisse."
            },
        ]
    
    messages.append({
        "role":  "user",
        "content": text,
    })

    return messages

def ai_conversation(messages):
    connection = http.client.HTTPSConnection(os.environ["LLM_OPENAI_HOST"])

    connection.request(
        method  = "POST",
        url     = os.environ["LLM_OPENAI_PATH"],
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['LLM_OPENAI_API_KEY']}",
        },
        body = json.dumps({
            "model": os.environ["LLM_OPENAI_MODEL"],
            "messages": messages,
        }),
    )

    response = connection.getresponse()
    data = response.read()
    connection.close()

    try:
        answer = json.loads(data)["choices"][0]["message"]["content"]
    except KeyError:
        answer = f"Fehler beim Aufruf der OpenAI API. Die Antwort war: {data}"

    return answer