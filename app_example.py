'''
app which connects to tarantool and inserts data
'''
import asyncio
import asynctnt
import time
import uuid
from datetime import datetime


PORT1 = 3303
PORT2 = 3304

'''for tarantool in docker version 3
sudo docker exec -it t3 console     # t3 - container_name (replace with your container_name)
sudo docker exec -it t4 console
Команды в консоли тарантула (запущенного в докере)  # following are commands for tarantool in docker

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
class Db:
    conn = None

    async def get_conn(self):
        if self.conn:
            return self.conn
        return await self.db_reconnect()

    async def db_reconnect(self):
        '''reconnect_timeout=None'''
        ports = (PORT1, PORT2)
        print("trying to connect...")
        for port in ports:
            try:
                self.conn = asynctnt.Connection(host="localhost", port=port, username='admin', password='pass', reconnect_timeout=None)
                await self.conn.connect()
            except ConnectionRefusedError:
                print("ConnectionRefusedError")
            except Exception as exc:
                print(exc)

            if self.conn:
                print(port)
                break
        return self.conn
    
    async def db_disconnect(self):
        if self.conn:
            await self.conn.disconnect()
            self.conn = None

    async def execute(self, sql, args=tuple()):
        conn = await self.get_conn()
        res = None
        if conn:
            try:
                res = await conn.execute(sql, args)
            except Exception as exc:
                print(exc)
                raise exc
        return res

    async def select(self, sql, args=tuple()):
        conn = await self.get_conn()
        res = None
        if conn:
            if not args:
                data = await conn.execute(sql)
            else:
                data = await conn.execute(sql, args)
            return data



async def print_select(db):
    sql = 'select * from SEQSCAN APP order by YEAR desc limit 5;'
    data = await db.select(sql)
    for row in data:
        print(row)
    print()



async def process_with_db(db, start=0, stop=1000):
    try:
        for i in range(start, stop):
            time_val = int(datetime.now().timestamp())
           
            sql = 'insert into APP (ID, BAND_NAME, YEAR) values (?, ?, ?);'
            args = (uuid.uuid4(), "", time_val)
            await db.execute(sql, args)

            if i % 10 == 1:
                await print_select(db)
            time.sleep(2)
            i += 1
    except Exception as exc:
        print(f"{i}--------Not finished {exc}")
    return i
    


async def main():
    db = Db()
    stop = 30
    i = await process_with_db(db, 0, stop)
    await db.db_disconnect()
    if i == stop:
        print('finished successfully')



asyncio.run(main())

