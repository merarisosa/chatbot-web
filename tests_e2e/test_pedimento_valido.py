import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "http://api-validacion.merrmsdev.work.gd/login"
PEDIMENTO = "255130655005970"


def build_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def test_pedimento_valido():
    driver = build_driver()
    wait = WebDriverWait(driver, 15)

    print("\n🚀 CT-03: Validación de pedimento EXISTENTE\n")

    # 1) LOGIN
    driver.get(LOGIN_URL)
    print("➡️ Login page:", driver.current_url)

    wait.until(EC.presence_of_element_located((By.NAME, "usuario"))).send_keys("admin")
    driver.find_element(By.NAME, "contrasena").send_keys("admin123")
    driver.find_element(By.TAG_NAME, "button").click()

    print("🔐 Credenciales enviadas…")
    time.sleep(2)

    print("🌐 URL tras login:", driver.current_url)
    assert "/validar" in driver.current_url

    # 2) VALIDAR PEDIMENTO
    print("\n🧾 Ingresando pedimento:", PEDIMENTO)

    ped_input = wait.until(EC.presence_of_element_located((By.NAME, "pedimento")))
    ped_input.send_keys(PEDIMENTO)

    # 🔥 AQUÍ EL FIX: seleccionar el botón REAL
    btn = driver.find_element(By.XPATH, "//button[text()='Validar']")
    btn.click()

    print("📩 Pedimento enviado…")
    time.sleep(3)

    print("🌐 URL tras validar:", driver.current_url)
    assert "/panel" in driver.current_url

    html = driver.page_source
    assert PEDIMENTO in html, "❌ El pedimento no está en el panel"
    print("✅ CT-03 COMPLETADO\n")

    driver.quit()

test_pedimento_valido()