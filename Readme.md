# Learning examples for connecting to tarantool db
(in docker)

used docker image: tarantool/tarantool:3

because it has type = 'uuid'

**reasons for the study project:**

--learn to connect to tarantool

--create two containers of docker, which works as multi-master replication for database

--create examples of sql-like queries to insert, select from tarantool by python


## **Installation**

--sudo docker-compose up (for tarantool in docker with auth)

(the line in docker-compose: `command: tarantool /usr/local/share/tarantool/app.init.lua` - isn't necessary. it creates some preparations for the example space. but in can be done manually)

--in app.init.lua theres a try to create trigger. can't say if it works.


--sudo docker exec -it my_container_name console (for creating spaces as preparation for connection in console, container_name in docker-compose)


--create virtual environment

--pip3 install tarantool (it is client, tarantool==1.1.2)(or pip install -r requirenments.txt)

--pip install asynctnt (asynctnt==2.1.0)


--run examples after preparations in console
(some examples in Jupyter Notebook and separately app_example.py)


## preparations in tarantool console in docker

`sudo docker exec -it my_container_name console`     # (replace with your container_name)

```
box.cfg {
        memtx_memory = 1 * 1000 * 1024 * 1024,
        listen = 3301,
        checkpoint_count  = 3,
        checkpoint_interval = 3600,
        read_only  = false 
}
```
```
box.schema.space.create('APP')

box.space.APP:format({
    { name = 'ID', type = 'uuid' },
    { name = 'BAND_NAME', type = 'string' },
    { name = 'YEAR', type = 'unsigned' }
})

box.space.APP:create_index("primary", {parts={{field = 1, type = 'uuid'}}})

box.space.APP:create_index('name', { unique = false, parts = { 'BAND_NAME' } })
box.space.APP:create_index('time', { unique = false, parts = { 'YEAR' } })
```
