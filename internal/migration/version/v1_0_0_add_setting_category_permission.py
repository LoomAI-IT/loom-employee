from internal import interface
from internal.migration.base import Migration, MigrationInfo


class AddSettingPermissionMigration(Migration):

    def get_info(self) -> MigrationInfo:
        return MigrationInfo(
            version="v1_0_0",
            name="add_setting_permissions",
            depends_on="v0_0_1"
        )

    async def up(self, db: interface.IDB):
        queries = [
            add_setting_category_permission_column,
            add_setting_organization_permission_column
        ]

        await db.multi_query(queries)

    async def down(self, db: interface.IDB):
        queries = [
            drop_setting_organization_permission_column,
            drop_setting_category_permission_column
        ]

        await db.multi_query(queries)

add_setting_category_permission_column = """
ALTER TABLE employees
ADD COLUMN setting_category_permission BOOLEAN DEFAULT FALSE;
"""

add_setting_organization_permission_column = """
ALTER TABLE employees
ADD COLUMN setting_organization_permission BOOLEAN DEFAULT FALSE;
"""

drop_setting_category_permission_column = """
ALTER TABLE employees
DROP COLUMN IF EXISTS setting_category_permission;
"""

drop_setting_organization_permission_column = """
ALTER TABLE employees
DROP COLUMN IF EXISTS setting_organization_permission;
"""
