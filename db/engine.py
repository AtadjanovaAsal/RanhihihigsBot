__all__ = [
    "async_create_table",
    "async_sessionmaker",
]

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import select, insert, update, delete
from .models import User, Base, Ref, Folder


engine = create_async_engine(url="sqlite+aiosqlite:///instance/sqlite.db", echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def async_create_table() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
async def user_exists(user_id) -> bool:
    async with async_session() as session:  
        query = select(User).where(user_id == User.user_id)
        user_exists = await session.execute(query)
        if user_exists.scalars().all():
            return True
        else:
            return False
        
async def add_user(user_id, username, status) -> bool: 
    async with async_session() as session:    
        if await user_exists(user_id):
            return False
        else:
            new_user = {
                        'user_id': user_id,
                        'username': username,
                        'status': status,
                    }
            insert_query = insert(User).values(**new_user)
            await session.execute(insert_query)
            await session.commit()
            return True

async def add_ref(user_id, refferer_id) -> bool: 
    async with async_session() as session:    
        if await user_exists(user_id):
            return False
        else:
            new_user = {
                        'user_id': user_id,
                        'refferer_id': refferer_id,
                    }
            insert_query = insert(Ref).values(**new_user)
            await session.execute(insert_query)
            await session.commit()
            return True
  
async def add_path(user_id, path) -> bool:
    async with async_session() as session:    
        if await user_exists(user_id):
            new_path = {
                'user_id': user_id,
                'folder_path': path,
            }
            try:
                insert_query = insert(Folder).values(**new_path)
                await session.execute(insert_query)
                await session.commit()
                return True
            except:
                return False
        else:
            return False

async def get_status(user_id):
    async with async_session() as session:    
        if await user_exists(user_id):
            query = select(User).where(user_id == User.user_id)
            result = await session.execute(query)
            user = result.scalar()
            query = select(Ref).where(user.user_id == Ref.user_id)
            result = await session.execute(query)
            ref = result.scalar()
            info = (f"<b>UserId</b>: <i>{user.user_id}</i>\n"
                    f"<b>UserName</b>: <i>{user.username}</i>\n"
                    f"<b>UserRole</b>: <i>{user.status}</i>\n"
                    f"<b>Registration Date</b>: <i>{user.reg_date}</i>\n"
                    f"<b>ReffererId</b>: <i>{ref.refferer_id}</i>")
            return info
        else:
            return None
     
async def get_role(user_id): 
    async with async_session() as session:    
        if await user_exists(user_id):
            query = select(User).where(user_id == User.user_id)
            result = await session.execute(query)
            user = result.scalar()
            return str(user.status)
        else:
            return None  
            
async def get_token(user_id):
    async with async_session() as session:    
        if await user_exists(user_id):
            query = select(User).where(user_id == User.user_id)
            result = await session.execute(query)
            user = result.scalar()
            return str(user.yatoken)
        else:
            return None 

async def get_folders():
    async with async_session() as session:    
        query = select(Folder).where(True)
        result = await session.execute(query)
        return result

async def get_refs(refferer_id):
    async with async_session() as session:    
        query = select(Ref).where(token.refferer_id == Ref.referer_id)
        result = await session.execute(query)
        return result
    
            
async def set_token(user_id, token): 
    async with async_session() as session:    
        if await user_exists(user_id):
            query = update(User).where(user_id == User.user_id).values(yatoken=token)
            await session.execute(query)
            await session.commit()
            return True
        else:
            return False
            
async def set_date(folder_id, date):
    async with async_session() as session:  
        query = update(Folder).where(int(folder_id) == Folder.id).values(check_date = date)
        await session.execute(query)
        await session.commit()
            
                        
async def rem_path(user_id, path) -> bool:
    async with async_session() as session:    
        if await user_exists(user_id):
            try:
                delete_query = delete(Folder).where(user_id == Folder.user_id).where(path == Folder.folder_path)
                await session.execute(delete_query)
                await session.commit()
                return True
            except:
                return False
        else:
            return False
            
          