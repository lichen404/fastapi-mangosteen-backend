from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(128) NOT NULL UNIQUE
);
COMMENT ON COLUMN "user"."email" IS '账号';
CREATE TABLE IF NOT EXISTS "item" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "amount" DOUBLE PRECISION NOT NULL,
    "kind" VARCHAR(10),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "happen_at" TIMESTAMPTZ,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "item"."amount" IS '金额';
COMMENT ON COLUMN "item"."kind" IS '类型';
COMMENT ON COLUMN "item"."created_at" IS '创建时间';
COMMENT ON COLUMN "item"."updated_at" IS '更新时间';
COMMENT ON COLUMN "item"."happen_at" IS '发生时间';
CREATE TABLE IF NOT EXISTS "tag" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "sign" VARCHAR(10) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "kind" VARCHAR(10),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "tag"."name" IS '名称';
COMMENT ON COLUMN "tag"."sign" IS '标志';
COMMENT ON COLUMN "tag"."created_at" IS '创建时间';
COMMENT ON COLUMN "tag"."kind" IS '类型';
COMMENT ON COLUMN "tag"."updated_at" IS '更新时间';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "item_tag" (
    "item_id" INT NOT NULL REFERENCES "item" ("id") ON DELETE CASCADE,
    "tag_id" INT NOT NULL REFERENCES "tag" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "item_tag" IS '标签';
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_item_tag_item_id_aa205c" ON "item_tag" ("item_id", "tag_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
