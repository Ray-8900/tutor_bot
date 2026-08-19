import asyncio

from database.queries import get_all_students, create_invitation_code, create_user
from database.queries import make_teacher

async def main():
    user = await make_teacher(1403307753)

    if user:
        print(user.name, user.role)
    else:
        print("Пользователь не найден")

if __name__ == "__main__":
    asyncio.run(main())