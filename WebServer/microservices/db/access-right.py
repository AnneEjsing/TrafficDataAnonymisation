@routes.get('/access/get')
async def right_get(request):
    data = await request.json()
    f = fieldCheck(['camera_id', 'user_id'], data)
    if f != None: return f
    
    camera_id = data['camera_id']
    user_id = data['user_id']
    query = """
    SELECT *
    FROM access_rights
    WHERE camera_id = %s AND user_id = %s;
    """

    result, error = execute_query(query, camera_id, user_id)
    if error: return web.Response(text=str(error),status=500)
    return web.Response(text=json.dumps(result, default=str), status=200)


@routes.delete('/access/delete')
async def right_delete(request):
    data = await request.json()
    f = fieldCheck(['camera_id', 'user_id'], data)
    if f != None: return f

    camera_id = data['camera_id']
    user_id = data['user_id']
    query = """
    DELETE FROM access_rights
    WHERE camera_id = %s AND user_id = %s
    RETURNING *;
    """
    result, error = execute_query(query, camera_id, user_id)
    if error: return web.Response(text=str(error),status=500)
    
    return hasOneResult(result, "There are no access for that user and camera.", 404)

@routes.post('/access/create')
async def right_create(request):
    data = await request.json()
    f = fieldCheck(['camera_id', 'user_id'], data)
    if f != None: return f
    
    camera_id = data['camera_id']    
    user_id = data['user_id']
    query = """
    INSERT INTO access_rights (camera_id,user_id)
    VALUES (
        %s, %s
    )
    RETURNING *;
    """
    result, error = execute_query(query,camera_id,user_id)
    if error: return web.Response(text=str(error),status=409)
    return web.Response(text=json.dumps(result, default=str), status=200)

@routes.get('/access/list')
def right_list(request):
    query = "SELECT * FROM access_rights;"
    result, error = execute_query(query)
    if error: return web.Response(text=str(error),status=500)
    return web.Response(text=json.dumps(result, default=str), status=200)