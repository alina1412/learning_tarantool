#!/usr/bin/env tarantool


local log = require('log')
local uuid = require('uuid')

local function init()
    -- box.schema.user.create('operator', {
    --     password = '123123', 
    --     if_not_exists = true
    -- })

    box.schema.user.grant('admin', 'read,write,execute', 
    'universe', nil, {
        if_not_exists = true
    })

    local APP_space = box.schema.space.create('APP', {
        if_not_exists = true
    })

    APP_space:format({
        { name = 'ID', type = 'uuid' },
        { name = 'BAND_NAME', type = 'string' },
        { name = 'YEAR', type = 'unsigned' }
    })
   
    box.space.APP:create_index("primary", {parts={{field = 1, type = 'uuid'}}, if_not_exists = true})
    box.space.APP:create_index('name', { unique = false, parts = { 'BAND_NAME' }, if_not_exists = true })
    box.space.APP:create_index('time', { unique = false, parts = { 'YEAR' }, if_not_exists = true })
    
    -- APP_space:create_index('ID', {
    --     if_not_exists = true,
    --     parts={{field = 1, type = 'uuid'}}
    -- })
   
    -- APP_space:create_index('NAME', {
    --     if_not_exists = true,
    --     type = 'TREE',
    --     unique = false,
    --     parts = { 'BAND_NAME' }
    -- })

    -- APP_space:create_index('year', { unique = false, parts = { 'YEAR' } })


end


-- unnecessary tries for triggers
local my_trigger = function(old, new, _, op)
    if new == nil or old == nil then
        return new
    end
    if op == 'INSERT' then
        if new[2] > old[2] then
            return box.tuple.new(new)
        end
    elseif new[2] > old[2] then
        return new
    end
    return old
end

-- код для добавления триггера unnecessary
-- позволит обрабатывать все записи, 
-- начиная с момента восстановления из snapshot'а
box.ctl.on_schema_init(function()
    box.space._space:on_replace(function(_, sp)
        if sp.name == 'APP' then
            box.on_commit(function() 
                -- I don't see the result of a print, but it seems that trigger works in case of replacing on the same id
                print('on_replace in,,,,,,,,,,,,')               
                box.space.APP:before_replace(my_trigger)
            end)
        end
    end)
end)
-- end of  unnecessary tries for triggers


box.cfg
{
    pid_file = nil,
    background = false,
    log_level = 5,
    read_only  = false
}

box.once('init', init)


