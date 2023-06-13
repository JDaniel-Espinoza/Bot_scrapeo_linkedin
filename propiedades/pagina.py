import time
import propiedades.Constante as const
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd




class linkedin(webdriver.Chrome):
    # Constructor de la clase "linkedin"
    # Se inicializan las variables y se configura el controlador de Selenium

    def __init__(self, driver_path=r"D:/xd/e/chromedriver.exe",
                 teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(linkedin, self).__init__()
        self.implicitly_wait(30)
        self.maximize_window()




    def entrar(self, NAME, PASS):
        # Método para iniciar sesión en LinkedIn
        self.get(const.BASE_URL)
        time.sleep(14)
        # Se encuentra el campo de nombre de usuario y se ingresa el nombre
        name = self.find_element(By.XPATH, const.NOMBRE_DE_USUARIO)
        name.clear()
        time.sleep(5)
        name.send_keys(NAME)
        time.sleep(8)
        # Se encuentra el campo de contraseña y se ingresa la contraseña
        clave = self.find_element(By.XPATH, const.CONTRASEÑA_DE_USUARIO)
        clave.clear()
        time.sleep(3)
        clave.send_keys(PASS)
        time.sleep(8)
        # Se encuentra y se hace clic en el botón de inicio de sesión
        iniciar = self.find_element(By.XPATH, const.BOTON_INICIAR_SESION)
        iniciar.click()

    def buscar(self, busqueda):
        # Método para buscar en LinkedIn
        time.sleep(8)

        # Se encuentra y se hace clic en el botón para ocultar el chat
        esconder_chat = self.find_element(By.XPATH, const.OCULTAR_CHAT)
        esconder_chat.click()
        time.sleep(6)

        # Se encuentra el campo de búsqueda y se ingresa la palabra clave de búsqueda
        name = self.find_element(By.XPATH, const.CAMPO_DE_BUSQUEDA)
        name.clear()
        time.sleep(9)
        name.send_keys(busqueda, Keys.ENTER)
        time.sleep(8)

        # Se encuentra y se hace clic en el botón para mostrar solo empresas en los resultados
        solo_empresas = self.find_element(By.XPATH, const.SOLO_EMPRESAS)
        solo_empresas.click()
        time.sleep(5)

    def dar_click(self, xpath1):
        # Método para realizar clic en ACERCA DE y extraer información de la página

        # Variables para almacenar los datos extraídos
        Telefono = "NULL"
        sector = "NULL"
        empleados = "NULL"
        sede = "NULL"
        texto = ""
        link = ""
        fundacion = "NULL"
        especialidades = "NULL"
        nombre = "NULL"

        # Verifica si se encontró el elemento xpath1
        try:
            opcion1 = self.find_element(By.XPATH, xpath1)
        except NoSuchElementException:
            opcion1 = None

        if opcion1 is not None:
            n = 5
        if opcion1 is None:
            n = 4

        # Se encuentra y se hace clic en la sección ACERCA DE para obtener información adicional
        opcion = self.find_element(By.XPATH, '/html/body/div[' + str(n) + ']/div[3]/div/div[2]/div/div[2]/main/div[1]/section/div/div[2]/div[2]/nav/ul/li[2]/a')
        opcion.click()

        # Se encuentra y se extrae el nombre de la empresa
        nombre_xpath = self.find_element(By.XPATH, '/html/body/div[' + str(n) + ']/div[3]/div/div[2]/div/div[2]/main/div[1]/section/div/div[2]/div[1]/div[1]/div[2]/div/h1/span')
        nombre = nombre_xpath.text.replace(",", " ")

        # Se encuentra y se extrae el enlace de la empresa
        link1 = self.find_element(By.XPATH, '/html/body/div[' + str(n) + ']/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dd[1]/a/span')
        link = link1.text

        # Se iteran varios elementos para extraer diferentes datos
        for i in range(7):
            try:
                texto_comparar = self.find_element(By.XPATH,
                                                   '/html/body/div[' + str(n) + ']/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dt[' + str(i) + ']')
            except NoSuchElementException:
                texto_comparar = None
            if texto_comparar is not None:
                texto = texto_comparar.text

                texto_fuente = self.find_element(By.XPATH,
                                                 '/html/body/div[' + str(n) + ']/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dd[' + str(i) + ']')

                texto_fuente2 = self.find_element(By.XPATH,
                                                  '/html/body/div[' + str(n) + ']/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dd[' + str(i + 1) + ']')

                if texto == "Teléfono":
                    texto_fuente3 = self.find_element(By.XPATH,
                                                      '/html/body/div[' + str(n) + ']/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dd[' + str(i) + ']/a/span[1]')
                    Telefono = texto_fuente3.text
                if texto == "Sector":
                    sector = texto_fuente.text
                if texto == "Tamaño de la empresa":
                    empleados = texto_fuente.text
                if texto == "Sede":
                    sede = texto_fuente2.text
                if texto == "Fundación":
                    fundacion = texto_fuente2.text
                if texto == "Especialidades":
                    especialidades = texto_fuente2.text

        return nombre, link, Telefono, sector, empleados, sede, fundacion, especialidades


    def una_a_una(self):
        # Método para realizar acciones en cada empresa en una lista de URLs
        datos = []

        # Encontrar los enlaces de empleo

        empresas = self.find_elements(By.XPATH, '//a[@class="app-aware-link "]')

        # Lista para almacenar las URLs de los empleos
        empresas_urls1 = []


        for empresa in empresas:

            empresas_urls1.append(empresa.get_attribute('href'))

        empresas_urls = empresas_urls1[1:]

        for i in range(len(empresas_urls)):
            empresas_urls[i] = empresas_urls[i].replace("'", "\\'")

        print('longitud', len(empresas_urls))

        print(empresas_urls)


        for url in (empresas_urls):

            time.sleep(5)
            # Abrir una nueva pestaña
            self.execute_script("window.open('" + url + "');")
            # Cambiar el controlador a la nueva pestaña
            self.switch_to.window(self.window_handles[1])

            time.sleep(5)  # Esperar a que se cargue la página del empleo

            datos.append(self.dar_click(const.PATH1_ACERCA_DE))

            time.sleep(3)



            self.close()
            # Cambiar el controlador de vuelta a la primera pestaña
            self.switch_to.window(self.window_handles[0])

        print(datos)
        df = pd.DataFrame(datos, columns=['Empresa', 'URL', 'Teléfono', 'Sector', 'Empleados', 'Ubicación', 'Año de fundación', 'Especialidades'])

        df.to_csv('prueba.csv', index=False, encoding='utf-8-sig')
