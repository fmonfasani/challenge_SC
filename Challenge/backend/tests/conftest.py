# importamos el módulo real donde está la función
import app.interfaces.middlewares.middlewares as _mw

# alias para que setup_middleware apunte al setup original
_mw.setup_middleware = _mw.setup