from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE INDEX IF NOT EXISTS "idx_item_happen_at" ON "item" ("happen_at");
        CREATE INDEX IF NOT EXISTS "idx_item_kind" ON "item" ("kind");
        CREATE INDEX IF NOT EXISTS "idx_tag_kind" ON "tag" ("kind");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "idx_item_happen_at";
        DROP INDEX IF EXISTS "idx_item_kind";
        DROP INDEX IF EXISTS "idx_tag_kind";"""
