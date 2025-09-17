create_employee = """
INSERT INTO employees (
    organization_id,
    invited_from_account_id,
    account_id,
    name,
    role,
    required_moderation,
    autoposting_permission,
    add_employee_permission,
    edit_employee_perm_permission,
    top_up_balance_permission,
    sign_up_social_net_permission
)
VALUES (
    :organization_id,
    :invited_from_account_id,
    :account_id,
    :name,
    :role,
    :required_moderation,
    :autoposting_permission,
    :add_employee_permission,
    :edit_employee_perm_permission,
    :top_up_balance_permission,
    :sign_up_social_net_permission
)
RETURNING id;
"""

get_employee_by_id = """
SELECT * FROM employees
WHERE account_id = :account_id;
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
WHERE account_id = :account_id;
"""

delete_employee = """
DELETE FROM employees
WHERE account_id = :account_id;
"""