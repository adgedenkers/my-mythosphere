# POST /proxy

This endpoint logs every user message in a conversation.

### Request Headers:
- `x-api-key`: string (required) — The API key of the user sending the message.

### Request Body:
- `user_input`: string (required) — The plain text of the user's message.
- `conversation_id`: string (required) — A unique identifier for the current chat conversation.

### Example:
```json
POST /proxy

Headers:
{
  "x-api-key": "galactic-architect-online"
}

Body:
{
  "user_input": "I want to query the data about Atlantis.",
  "conversation_id": "conv-12345"
}
```

### Response:
- `200 OK` if the message was successfully logged.
- `400 Bad Request` if required fields are missing.
- `403 Forbidden` if the API key is invalid.
- `500 Internal Server Error` for any other issues.