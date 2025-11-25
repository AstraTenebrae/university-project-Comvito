from api_settings import app
import routes, db_tables                           # Необходимо, чтобы эти модули прогрузились ДО запуска сервера

if __name__ == '__main__':
    app.run()

