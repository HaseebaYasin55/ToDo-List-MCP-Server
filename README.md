# Todo List MCP Server

A simple, beginner-friendly **Model Context Protocol (MCP) server** written in Python.
It lets any MCP-compatible AI client (like Claude Desktop) manage a to-do list on your
computer through five tools: add, view, get by ID, complete, and delete.

Built with the official **MCP Python SDK** (`mcp[cli]`) and its high-level `FastMCP` interface.
Data is stored locally in a plain JSON file — no database required.

---

## 1. What This Project Does

This MCP server exposes 5 tools to any connected AI client:

| Tool | What it does |
|---|---|
| `add_todo(title, description)` | Adds a new todo |
| `list_todos()` | Returns every todo currently saved |
| `get_todo(todo_id)` | Returns one todo by its ID |
| `complete_todo(todo_id)` | Marks a todo as completed |
| `delete_todo(todo_id)` | Removes a todo permanently |

All data lives in `todos.json`, created automatically the first time you add a todo.

---

## 2. Project Structure

```
todo-mcp-server/
├── server.py          # Main MCP server — defines the 5 tools
├── storage.py          # Handles reading/writing todos.json
├── todos.json           # Auto-created data file (not committed to git)
├── requirements.txt     # Python dependencies     
├── .gitignore            # Files Git should ignore
└── README.md             
```

---

## 3. Setup

### Prerequisites
- Python 3.10 or newer
- pip (comes with Python)

### Steps

```bash
# 1. Clone or download this project, then move into it
cd todo-mcp-server

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## 4. Running the Server

**Option A — MCP Inspector (recommended for testing):**
```bash
mcp dev server.py
```
This opens a browser-based UI where you can call each tool manually and see the JSON responses.

**Option B — Install into Claude Desktop:**
```bash
mcp install server.py --name "Todo List MCP Server"
```
This registers the server so Claude Desktop starts it automatically.

**Option C — Run directly:**
```bash
python server.py
```

---

## 5. Testing / Example Prompts (in Claude Desktop)

Once connected in Claude Desktop, try:

- "Add a todo: Buy groceries, with description Milk, eggs, and bread"
- "Show me all my todos"
- "Get the todo with ID 1"
- "Mark todo 1 as completed"
- "Delete todo 2"

---

## 6. Architecture

```
 MCP Client (Claude Desktop)
          │  (stdio / JSON-RPC)
          ▼
     server.py  (FastMCP tools)
          │
          ▼
     storage.py (reads/writes JSON)
          │
          ▼
     todos.json  (local data file)
```

The client never touches the JSON file directly — it only calls tools, and the server
decides how the data is stored. This separation is a core MCP design idea: the client
doesn't need to know *how* a tool works internally, only *what* it does.

---

## 7. Learning Outcomes

Through this project I learned:
- What the Model Context Protocol (MCP) is and how it standardizes tool access for LLMs
- The difference between an MCP server, client, and tools/resources/prompts
- How to use the official Python SDK's `FastMCP` interface to build tools quickly from
  plain Python functions and type hints
- How to store and manage data locally with a JSON file
- How to connect and test a custom MCP server inside Claude Desktop
- How to package, document, and publish a small Python project on GitHub
- The basics of publishing an MCP server to a marketplace like Smithery

---

## License

MIT — free to use, modify, and share.

---

## Author

**Haseeba Yasin**

If you found this project helpful, feel free to ⭐ the repository.
