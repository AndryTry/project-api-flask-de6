from module import test, users, users_orm, login
from connection import open_config, app 


app.add_url_rule('/', view_func=test.say_hello)
app.add_url_rule('/users', view_func=users.users, methods=["GET", "POST"])
app.add_url_rule('/users_orm', view_func=users_orm.users_orm, methods=["GET", "POST"])
app.add_url_rule('/users_orm/<user_id>', view_func=users_orm.handle_user, methods=['GET', 'PUT', 'DELETE'])
app.add_url_rule('/login', view_func=login.login, methods=["POST"])

config = open_config()
if __name__ == "__main__":
    app.run(debug=True, port=config['port_api'], ssl_context=('cert.pem', 'key.pem'))