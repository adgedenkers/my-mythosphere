# Executable Knowledge Graph – Intake Logging System

## Overview
This document describes the structure and behavior of the intake logging system built using the Executable Knowledge Graph (XKG) architecture. It outlines how user conversations are recorded, structured, and stored using a combination of FastAPI endpoints, GitHub-based logs, and Neo4j metadata relationships.

## Objectives
- Capture full user prompts and assistant responses
- Embed associated files (e.g., base64-encoded images)
- Persist the interaction history as versioned markdown logs
- Structure metadata in Neo4j for indexing, search, and graph querying

## Core Concepts
- **XKG (Executable Knowledge Graph):** A runtime model where executable logic and interactions are defined as graph nodes and relationships.
- **Conversation Logging:** Prompt and response exchanges stored as markdown documents, with additional tagging and metadata indexed in Neo4j.

## Key Components

### `/convolog` Endpoint
- Accepts:
  - `conversation_id`: unique identifier
  - `user_prompt`: text of the user message
  - `file_data`: optional list of base64-encoded file attachments
- Behavior:
  1. Checks if GitHub file for the conversation exists
  2. If not, creates it and adds metadata to Neo4j
  3. Formats the prompt + files into markdown
  4. Appends markdown to GitHub file
  5. (Planned) Triggers analysis and tagging

### `/convolog/response` Endpoint
- Accepts:
  - `conversation_id`: same as above
  - `assistant_response`: assistant's reply text
  - `response_files`: optional base64-encoded attachments
- Behavior:
  1. Formats the assistant response
  2. Appends it to the same GitHub file

### Utilities
- `normalize_datetime`: ensures uniform timestamp handling
- `format_prompt_entry` / `format_response_entry`: markdown formatting utilities
- `append_to_github`: API bridge to GitHub backend

## GitHub Structure
Markdown logs are stored under:
```
logs/{conversation_id}.md
```

Each log includes:
- ISO 8601 timestamped headers
- User prompt
- Assistant response
- Inline file previews (base64)

## Neo4j Metadata
When a conversation file is created, a `:Conversation` node is also created with:
- `title`, `author`, `created_at`, and more
- Relationship to a `:Person` (if authenticated)
- Relationships to extracted `:Tag` nodes (planned)

## Future Enhancements
- Tag extraction using keyword/topic analysis
- Support for file download from GitHub
- Linking to `:CodeChunk` nodes when a user submits executable code

## Status
This system is under live development. The core functionality is working and the logging structure is being extended to support tagging, chunk linkage, and deeper introspection.
