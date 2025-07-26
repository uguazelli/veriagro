from app.models.company import CompanyCreate, CompanyOut, CompanyMembership
import asyncpg
import uuid


async def create_company(conn: asyncpg.Connection, company: CompanyCreate) -> CompanyOut:
    """
    Create a new company in the database.
    """
    query = """
    INSERT INTO companies (id, name, created_at)
    VALUES ($1, $2, NOW())
    RETURNING id, name, created_at;
    """
    company_id = uuid.uuid4()
    row = await conn.fetchrow(query, company_id, company.name)
    return CompanyOut(id=row['id'], name=row['name'], created_at=row['created_at'])


async def get_company(conn: asyncpg.Connection, company_id: int) -> CompanyOut:
    """
    Retrieve a company by its ID.
    """
    query = "SELECT id, name, created_at FROM companies WHERE id = $1;"
    row = await conn.fetchrow(query, company_id)
    if row:
        return CompanyOut(id=row['id'], name=row['name'], created_at=row['created_at'])
    return None

async def delete_company(conn: asyncpg.Connection, company_id: int) -> bool:
    """
    Delete a company by its ID.
    """
    query = "DELETE FROM companies WHERE id = $1;"
    result = await conn.execute(query, company_id)
    return result == "DELETE 1"

async def create_membership(conn, membership):
    membership_id = uuid.uuid4()

    query = """
        INSERT INTO company_memberships (id, user_id, company_id, role, created_at)
        VALUES ($1, $2, $3, $4, now())
        RETURNING id, user_id, company_id, role, created_at
    """

    row = await conn.fetchrow(
        query,
        membership_id,
        membership.user_id,
        membership.company_id,
        membership.role
    )

    return dict(row)


async def get_user_companies(conn: asyncpg.Connection, user_id: str) -> list[CompanyOut]:
    """
    Get all companies a user is a member of.
    """
    query = """
    SELECT c.id, c.name, c.created_at
    FROM companies c
    JOIN company_memberships cm ON c.id = cm.company_id
    WHERE cm.user_id = $1;
    """
    rows = await conn.fetch(query, user_id)
    return [CompanyOut(id=row['id'], name=row['name'], created_at=row['created_at']) for row in rows]

async def delete_membership(conn: asyncpg.Connection, user_id: str, company_id: str) -> bool:
    """
    Delete a membership for a user in a company.
    """
    query = "DELETE FROM company_memberships WHERE user_id = $1 AND company_id = $2;"
    result = await conn.execute(query, user_id, company_id)
    return result == "DELETE 1"
