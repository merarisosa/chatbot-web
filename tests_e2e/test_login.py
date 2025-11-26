import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "http://api-validacion.merrmsdev.work.gd/login"


def test_login_valido():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(BASE_URL)
    print("🚀 Chrome se abrió correctamente en /login")

    time.sleep(3)

    # Llenar formulario
    driver.find_element(By.NAME, "usuario").send_keys("admin")
    driver.find_element(By.NAME, "contrasena").send_keys("admin123")

    # Click login
    driver.find_element(By.TAG_NAME, "button").click()
    print("➡️ Se hizo clic en login")
    time.sleep(10)

    # Validar redirección
    assert "/validar" in driver.current_url

    print("✅ Login válido redirige a /validar correctamente")
    driver.quit()


test_login_valido()