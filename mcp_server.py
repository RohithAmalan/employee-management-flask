# mcp_server.py
print("✅ MCP Employee tools registered")

from mcp.server.fastmcp import FastMCP
from flask_app import load_employees, save_employees  # reuse your helpers

mcp = FastMCP("employee-management-mcp")


def _get_next_id(employees: list[dict]) -> int:
    """Helper: find next employee ID."""
    if not employees:
        return 1
    return max(e.get("id", 0) for e in employees) + 1


# ---------------- MCP TOOLS ---------------- #

@mcp.tool()
def create_employee(
    name: str,
    email: str,
    phone: str,
    role: str = "",
    department: str = "",
    salary: int | float | None = None,
    date_of_joining: str = "",
    status: str = "Active",
) -> dict:
    """
    Create a new employee and store it in employees.json.
    Returns the created employee record.
    """
    employees = load_employees()

    new_emp = {
        "id": _get_next_id(employees),
        "name": name,
        "email": email,
        "phone": phone,
        "role": role,
        "department": department,
        "salary": salary or 0,
        "date_of_joining": date_of_joining,
        "status": status or "Active",
    }

    employees.append(new_emp)
    save_employees(employees)
    return new_emp


@mcp.tool()
def list_employees() -> list[dict]:
    """
    Return the full list of employees from employees.json.
    """
    return load_employees()


@mcp.tool()
def delete_employee(employee_id: int) -> dict:
    """
    Delete an employee by ID.
    Returns a small status message.
    """
    employees = load_employees()
    remaining = [e for e in employees if e.get("id") != employee_id]

    if len(remaining) == len(employees):
        return {"success": False, "message": "Employee not found"}

    save_employees(remaining)
    return {"success": True, "message": f"Employee {employee_id} deleted"}


if __name__ == "__main__":
    # Run MCP server (typically over stdio or a socket; your MCP client will connect to this)
    mcp.run()
