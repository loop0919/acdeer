from typing import Optional
import aiomysql
import settings

logger = settings.logging.getLogger("bot")

async def create_server_connection() -> Optional[aiomysql.connection.Connection]:
    connection = None
    try:
        connection = await aiomysql.connect(
            host=settings.MYSQL_HOST,
            user=settings.MYSQL_USER,
            db='acdeer',
            password=settings.MYSQL_PASSWORD
        )
        logger.info("MySQL Database connection successful")
    except aiomysql.Error as err:
        logger.error(err)
        raise err

    return connection


async def set_user(conn: aiomysql.connection.Connection, atcoder_id: str, discord_id: int, rating: int) -> None:
    try:
        async with await conn.cursor() as cur:
            stmt = """\
                INSERT INTO users(atcoder_id, discord_id, rating)
                VALUES (%(atcoder_id)s, %(discord_id)s, %(rating)s);
            """
            
            
            await cur.execute(stmt, {
                "atcoder_id": atcoder_id,
                "discord_id": discord_id,
                "rating": rating
            })
            
            await conn.commit()
        
        logger.info(f"User registerd in MySQL Database! ({discord_id}, {atcoder_id}, {rating})")
    
    except aiomysql.Error as err:
        logger.error(err)
        raise err


async def fetch_user(conn: aiomysql.connection.Connection, discord_id: int):
    try:
        async with await conn.cursor() as cur:
            stmt = """\
                SELECT atcoder_id, rating FROM users
                WHERE discord_id = %s;
            """
            
            await cur.execute(stmt, (discord_id, ))
            fetched = await cur.fetchone()
            atcoder_id = fetched[0] if fetched else None
            rating = fetched[1] if fetched else None
            
            logger.info(f"{atcoder_id}, {rating}")
            
            return atcoder_id, rating
        
    except aiomysql.Error as err:
        logger.error(err)
        raise err


async def fetch_user(conn: aiomysql.connection.Connection, discord_id: int):
    try:
        async with await conn.cursor() as cur:
            stmt = """\
                SELECT atcoder_id, rating FROM users
                WHERE discord_id = %s;
            """
            
            await cur.execute(stmt, (discord_id, ))
            fetched = await cur.fetchone()
            atcoder_id = fetched[0] if fetched else None
            rating = fetched[1] if fetched else None
            
            logger.info(f"{atcoder_id}, {rating}")
            
            return atcoder_id, rating
        
    except aiomysql.Error as err:
        logger.error(err)
        raise err
