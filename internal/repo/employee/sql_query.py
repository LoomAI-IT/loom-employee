create_employee = """
INSERT INTO employees (
    organization_id,
    invited_from_employee_id,
    account_id,
    name,
    role
)
VALUES (
    :organization_id,
    :invited_from_employee_id,
    :account_id,
    :name,
    :role
)
RETURNING id;
"""

get_employee_by_id = """
SELECT * FROM employees
WHERE id = :employee_id;
"""

get_employee_by_account_id = """
SELECT * FROM employees
WHERE account_id = :account_id;
"""

get_employees_by_organization = """
SELECT * FROM employees
WHERE organization_id = :organization_id
ORDER BY created_at DESC;
"""

update_employee_role = """
UPDATE employees 
SET role = :role
WHERE id = :employee_id;
"""

delete_employee = """
DELETE FROM employees
WHERE id = :employee_id;
"""