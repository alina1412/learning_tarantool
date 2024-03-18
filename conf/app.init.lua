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
   
    box.space.APP:create_index("primary", {parts={{field = 1, type = 'uuid'}}})
    box.space.APP:create_index('name', { unique = false, parts = { 'BAND_NAME' } })
    box.space.APP:create_index('time', { unique = false, parts = { 'YEAR' } })
    
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


box.cfg
{
    pid_file = nil,
    background = false,
    log_level = 5,
    read_only  = false
}

box.once('init', init)