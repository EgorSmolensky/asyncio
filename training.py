from aiohttp import ClientSession
import asyncio
from more_itertools import chunked
from db import engine, Session, People, Base

MAX_SIZE = 10


async def get_person(people_id: int, client: ClientSession):
    url = f'https://swapi.dev/api/people/{people_id}'
    async with await client.get(url) as response:
        json_data = await response.json()
    json_data['homeworld'] = await get_info([json_data['homeworld']], client)
    json_data['films'] = await get_info(json_data['films'], client, 'title')
    json_data['species'] = await get_info(json_data['species'], client)
    json_data['starships'] = await get_info(json_data['starships'], client)
    json_data['vehicles'] = await get_info(json_data['vehicles'], client)
    return json_data


async def get_info(info_list, client, desc='name'):
    info = []
    for url in info_list:
        async with await client.get(url) as response:
            json_data = await response.json()
            info.append(json_data[desc])
    return ', '.join(info)


async def paste_to_db(people_list):
    async with Session() as session:
        people_list = [People(
            birth_year=item['birth_year'],
            eye_color=item['eye_color'],
            films=item['films'],
            gender=item['gender'],
            hair_color=item['hair_color'],
            height=item['height'],
            homeworld=item['homeworld'],
            mass=item['mass'],
            name=item['name'],
            skin_color=item['skin_color'],
            species=item['species'],
            starships=item['starships'],
            vehicles=item['vehicles'],
        ) for item in people_list]
        session.add_all(people_list)
        await session.commit()


async def main():
    tasks = list()
    async with ClientSession() as session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        for id_chunk in chunked(range(1, 83), MAX_SIZE):
            coros = [get_person(people_id=id, client=session) for id in id_chunk if id != 17]
            people_list = await asyncio.gather(*coros)
            db_coro = paste_to_db(people_list)
            paste_to_db_task = asyncio.create_task(db_coro)
            tasks.append(paste_to_db_task)
    tasks = asyncio.all_tasks() - {asyncio.current_task()}
    for task in tasks:
        await task


asyncio.run(main())
