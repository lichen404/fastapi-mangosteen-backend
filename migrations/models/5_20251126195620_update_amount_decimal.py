from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "item" ALTER COLUMN "amount" TYPE DECIMAL(10,2) USING "amount"::DECIMAL(10,2);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "item" ALTER COLUMN "amount" TYPE DOUBLE PRECISION USING "amount"::DOUBLE PRECISION;"""
