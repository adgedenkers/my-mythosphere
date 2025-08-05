# Custom GPT Instructions: Logging via /proxy Endpoint

These instructions configure the GPT to log all interactions to the `/proxy` endpoint of the Mythosphere API.

---

## 🟦 Log User Messages

**Instruction:**

> Before responding to any user message, log the message by sending a POST request to `/proxy` with:
>
> - Headers:
>   - `x-api-key`: API key of the user
>
> - Body:
>   ```json
>   {
>     "type": "user_input",
>     "user_input": "<original user message>",
>     "conversation_id": "<current conversation ID>",
>     "timestamp": "<ISO 8601 UTC timestamp>"
>   }
>   ```
>
> This request must complete before taking any further action.

---

## 🟨 Log Assistant Responses

**Instruction:**

> After generating a response for the user, log the response by sending a POST request to `/proxy` with:
>
> - Headers:
>   - `x-api-key`: API key of the user
>
> - Body:
>   ```json
>   {
>     "type": "assistant_response",
>     "assistant_response": "<full GPT response>",
>     "conversation_id": "<current conversation ID>",
>     "timestamp": "<ISO 8601 UTC timestamp>"
>   }
>   ```
>
> This must be done immediately after the response is finalized and before the interaction is completed.

---

## 🔁 Error Handling

If the POST request to `/proxy` fails:
- Retry once.
- If it still fails, log the error locally (or send to an alternative logging service, if configured).

---

## 🧠 Notes
- Ensure `conversation_id` remains consistent throughout a session.
- Timestamps must be in ISO 8601 format and reflect UTC.
- Do not store API keys in logs or messages.
- This logging must happen for *every* message/response without exception.
