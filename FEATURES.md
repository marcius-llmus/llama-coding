
---

## Core Features
- **Conversational Code Generation:** Accepts user messages and generates code patches based on them.
- **Live Diff Streaming:** Streams code changes as `diff` patches in the main window.
- **Context Management UI:** Features a popup with a project file tree that respects `.gitignore` rules, allowing users to add or remove files from the context.
- **.gitignore Integration:** A `.gitignore` file is required for accurate project file filtering.
- **Internal Ignore List:** Includes an internal ignore list for application-specific files.
---

## AI & Context Intelligence
- **Automatic Context Gathering:** When enabled, the application analyzes the Abstract Syntax Tree (AST) to intelligently determine which files should be added to the context.
- **RAG Integration:** Can utilize Retrieval-Augmented Generation (RAG) to add relevant code chunks or entire files to the context.
- **AST-Powered Context:** Always sends the AST in requests, with configurable parameters to limit its size for efficiency.
- **Model Selection:** Allows users to select different language models for various tasks.
- **Temperature Configuration:** Provides the ability to configure the model's temperature for controlling creativity.

---

## Project & Environment Management
- **Docker-Based Setup:** Configuration is managed via `docker-compose.yml` and an environment file. A volume is mounted to provide the application access to user projects, allowing them to continue using their preferred IDE.
- **Project State Persistence:** Users can select a configured project, which will load its previous state, including loaded files and conversation history.
---

## Configuration & Customization
- **Single-Page Application (SPA):** The application operates as an SPA where all configurations are managed through modals.
- **Token Limit Configuration:** Users can configure the maximum number of tokens for the AST analysis to manage context size.
- **Operational Modes:** Users can switch between different modes, such as 'plan', 'read', and 'write'.
- **Message History Control:** Users can set the length of the message history to be included in the context.
- **Chat Management:** Users can clear the chat history.