import asyncio
import asynctnt
import time
import uuid
from datetime import datetime


PORT1 = 3303
PORT2 = 3304

'''for tarantool in docker version 3
sudo docker exec -it t3 console
sudo docker exec -it t4 console
Команды в консоли тарантула (запущенного в докере)

box.cfg {
        memtx_memory = 1 * 1000 * 1024 * 1024,
        listen = 3301,
        checkpoint_count  = 3,
        checkpoint_interval = 3600,
        read_only  = false 
}


box.schema.space.create('APP')

box.space.APP:format({
    { name = 'ID', type = 'uuid' },
    { name = 'BAND_NAME', type = 'string' },
    { name = 'YEAR', type = 'unsigned' }
})

box.space.APP:create_index("primary", {parts={{field = 1, type = 'uuid'}}})

box.space.APP:create_index('name', { unique = false, parts = { 'BAND_NAME' } })
box.space.APP:create_index('time', { unique = false, parts = { 'YEAR' } })
'''

async def get_conn(port):
    conn = asynctnt.Connection(host="localhost", port=port, username='admin', password='pass')
    await conn.connect()
    return conn


async def insert(conn, val):
    await conn.execute('insert into APP (ID, BAND_NAME, YEAR) values (?, ?, ?);', (uuid.uuid4(), "", val))


async def print_select(conn):
    data = await conn.execute('select * from SEQSCAN  APP order by YEAR desc limit 5;')
    for row in data:
        print(row)
    print()


async def main():
    try:
        conn = await get_conn(PORT1)
        print(PORT1)
    except Exception:
        conn = await get_conn(PORT2)
        print(PORT2)
    

    for i in range(1000):
        time_val = int(datetime.now().timestamp())
        await insert(conn, time_val)

        if i % 10 == 1:
            await print_select(conn)
        time.sleep(2)

    await conn.disconnect()



asyncio.run(main())

