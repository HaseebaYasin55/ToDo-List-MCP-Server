"""
server.py
---------
This is the main MCP server file.

It uses FastMCP, the high-level, beginner-friendly interface that ships
inside the official MCP Python SDK ("mcp" package on PyPI).

FastMCP lets you turn a normal Python function into an MCP "tool" just by
adding the @mcp.tool() decorator above it. The SDK automatically:
  - reads your function's type hints to build the tool's input schema
  - reads your docstring to build the tool's description
  - handles all the low-level MCP protocol / JSON-RPC details for you

Run this server with:
    uv run mcp dev server.py      (opens the MCP Inspector for testing)
or:
    uv run mcp install server.py  (installs it into Claude Desktop)
or directly:
    python server.py
"""

from mcp.server.fastmcp import FastMCP

import storage

# Create the MCP server instance.
# The name "Todo List MCP Server" is what shows up in MCP clients like
# Claude Desktop when they list connected servers.
mcp = FastMCP("Todo List MCP Server")


@mcp.tool()
def add_todo(title: str, description: str = "") -> dict:
    """
    Add a new todo item to the list.

    Args:
        title: A short title describing the task (required).
        description: Optional extra details about the task.

    Returns:
        The newly created todo, including its auto-generated ID.
    """
    if not title or not title.strip():
        return {"error": "Title cannot be empty."}

    new_todo = storage.add_todo(title.strip(), description.strip())
    return {"message": "Todo added successfully.", "todo": new_todo}


@mcp.tool()
def list_todos() -> dict:
    """
    View all todo items currently saved, both completed and not completed.

    Returns:
        A list of every todo, plus a count.
    """
    todos = storage.get_all_todos()
    return {"count": len(todos), "todos": todos}


@mcp.tool()
def get_todo(todo_id: int) -> dict:
    """
    Get a single todo item by its ID.

    Args:
        todo_id: The numeric ID of the todo you want to look up.

    Returns:
        The matching todo, or an error message if no todo has that ID.
    """
    todo = storage.get_todo_by_id(todo_id)
    if todo is None:
        return {"error": f"No todo found with id {todo_id}."}
    return {"todo": todo}


@mcp.tool()
def complete_todo(todo_id: int) -> dict:
    """
    Mark a todo item as completed.

    Args:
        todo_id: The numeric ID of the todo to mark as done.

    Returns:
        The updated todo, or an error message if no todo has that ID.
    """
    todo = storage.mark_todo_completed(todo_id)
    if todo is None:
        return {"error": f"No todo found with id {todo_id}."}
    return {"message": "Todo marked as completed.", "todo": todo}


@mcp.tool()
def delete_todo(todo_id: int) -> dict:
    """
    Delete a todo item permanently.

    Args:
        todo_id: The numeric ID of the todo to delete.

    Returns:
        A confirmation message, or an error message if no todo has that ID.
    """
    was_deleted = storage.delete_todo(todo_id)
    if not was_deleted:
        return {"error": f"No todo found with id {todo_id}."}
    return {"message": f"Todo {todo_id} deleted successfully."}


# This block only runs when you execute "python server.py" directly.
# It is not used by "uv run mcp dev" or "uv run mcp install", which
# import the `mcp` object above instead.
if __name__ == "__main__":
    mcp.run()