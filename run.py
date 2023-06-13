from propiedades.pagina import linkedin
import time

with linkedin() as bot:
    bot.entrar('*****@gmail.com','Contraseña')
    bot.buscar('companies')
    bot.una_a_una()
    time.sleep(10000)


