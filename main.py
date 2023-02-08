import uvicorn
from fastapi import FastAPI, status, UploadFile, File
from starlette.responses import RedirectResponse, Response

from config import HOST, PORT
from pools import FilePool, dump_factories_file, get_factories_file, Factories

app = FastAPI()
factories = Factories()


@app.get('/')
async def get_root():
    return RedirectResponse('/proxies')


@app.get('/proxies')
async def get_factories(method: str = 'info'):
    match method:
        case 'info':
            return {key: item.info() for key, item in factories.items()}
        case 'reload':
            factories.reload_pools()
            return RedirectResponse('/proxies')


@app.patch('/proxies')
async def put_factories(model: dict):
    factories_file: dict = get_factories_file()
    factories_file.update(model)
    dump_factories_file(factories_file)
    factories.reload_pools()
    return RedirectResponse(url='/proxies', status_code=status.HTTP_302_FOUND)


@app.post('/proxies')
async def post_factories(model: dict):
    dump_factories_file(model)
    factories.reload_pools()
    return RedirectResponse(url='/proxies', status_code=status.HTTP_302_FOUND)


@app.get('/proxies/{pool}')
async def get_factory_pool(pool: str, method: str = 'info'):
    proxy_pool: FilePool = factories.get(pool)
    match method:
        case 'info':
            info = proxy_pool.info()
            return info
        case 'pool':
            pool = proxy_pool.get_pool()
            return Response(content='\n'.join(pool))
        case 'pop':
            value = proxy_pool.pop()
            return Response(content=value)
        case 'clear':
            proxy_pool.clear()
            return RedirectResponse(f'/proxies/{pool}')
        case 'reload':
            proxy_pool.reload()
            return RedirectResponse(f'/proxies/{pool}')


@app.post('/proxies/{pool}')
async def post_factory_pool(pool, file: UploadFile = File(...)):
    if pool not in factories.keys():
        print(file)
        return RedirectResponse('/proxies', status_code=status.HTTP_302_FOUND)


if __name__ == '__main__':
    uvicorn.run('main:app', host=HOST, port=int(PORT))
