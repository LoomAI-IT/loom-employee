from internal import interface, model
from internal.migration.base import Migration, MigrationInfo


class InitialSchemaMigration(Migration):

    def get_info(self) -> MigrationInfo:
        return MigrationInfo(
            version="v0_0_1",
            name="initial_schema",
        )

    async def up(self, db: interface.IDB):
        queries = [
            create_employees_table
        ]

        await db.multi_query(queries)

    async def down(self, db: interface.IDB):
        queries = [
            drop_employees_table
        ]

        await db.multi_query(queries)

create_employees_table = """
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER NOT NULL,
    
    invited_from_account_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    
    required_moderation BOOLEAN DEFAULT FALSE,
    autoposting_permission BOOLEAN DEFAULT FALSE,
    add_employee_permission BOOLEAN DEFAULT FALSE,
    edit_employee_perm_permission BOOLEAN DEFAULT FALSE,
    top_up_balance_permission BOOLEAN DEFAULT FALSE,
    sign_up_social_net_permission BOOLEAN DEFAULT FALSE,
    
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

drop_employees_table = """
DROP TABLE IF EXISTS employees CASCADE;
"""