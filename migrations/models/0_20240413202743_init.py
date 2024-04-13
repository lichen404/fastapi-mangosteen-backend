from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "email" VARCHAR(128) NOT NULL UNIQUE /* 账号 */
);
CREATE TABLE IF NOT EXISTS "item" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "amount" INT NOT NULL  /* 金额 */,
    "kind" VARCHAR(10)   /* 类型 */,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 创建时间 */,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 更新时间 */,
    "happen_at" TIMESTAMP   /* 发生时间 */,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "tag" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(50) NOT NULL  /* 名称 */,
    "sign" VARCHAR(10) NOT NULL  /* 标志 */,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 创建时间 */,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 更新时间 */,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "item_tag" (
    "item_id" INT NOT NULL REFERENCES "item" ("id") ON DELETE CASCADE,
    "tag_id" INT NOT NULL REFERENCES "tag" ("id") ON DELETE CASCADE
) /* 标签 */;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
