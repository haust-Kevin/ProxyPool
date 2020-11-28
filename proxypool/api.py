from flask import Flask, g, request

__all__ = ['app']

from dao.mysql_dao import MysqlConn
from dao.redis_dao import RedisClient

app = Flask(__name__)


def get_redis_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


def get_mysql_conn():
    if not hasattr(g, 'mysql'):
        g.mysql = MysqlConn()
    return g.mysql


@app.route('/')
def index():
    return '''
            <h2>Welcome to Proxy Pool System!</h2>
           '''


@app.route('/get')
def get_proxy():
    data = request.args
    name = data.get('name')
    pwd = data.get('pwd')
    if get_mysql_conn().exist(name, pwd):
        return get_redis_conn().random()
    return '<h2>用户或口令错误, 有疑问请QQ咨询: {}</h2>'.format('878474339')


if __name__ == '__main__':
    app.run()
