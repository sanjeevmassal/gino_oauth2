import gino
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.authentication import AuthenticationMiddleware
from users.backends import BasicAuthBackend
from core import db
app = Starlette()
app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
app.debug = True
app.mount('/static', StaticFiles(directory="static"))
app.db_engine = None

@app.route('/')
def homepage(request):
    return PlainTextResponse('Hello, world!')

@app.route('/user/me')
def user_me(request):
    username = "John Doe"
    return PlainTextResponse('Hello, %s!' % username)

@app.route('/user/{username}')
def user(request):
    username = request.path_params['username']
    return PlainTextResponse('Hello, %s!' % username)

@app.on_event('startup')
def startup():
    print('Ready to go')

async def open_database_connection_pool():
    print('Database connection created')
    app.db_engine = await gino.create_engine('postgresql://postgres:root@localhost/gino_user')
    db.bind = app.db_engine

async def close_database_connection_pool():
    print('Database connection Connection close')
    await app.db_engine.close()

app.add_event_handler('startup', open_database_connection_pool)
app.add_event_handler('shutdown', close_database_connection_pool)