from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

LOGIN_URL = "http://api-validacion.merrmsdev.work.gd/login"
PEDIMENTO_FAKE = "999999999999999"


def login(driver):
    driver.get(LOGIN_URL)
    time.sleep(1)
    driver.find_element(By.NAME, "usuario").send_keys("admin")
    driver.find_element(By.NAME, "contrasena").send_keys("admin123")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(2)


def test_pedimento_inexistente():
    print("\n🚀 CT-04: Pedimento inexistente\n")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    login(driver)

    ped_input = driver.find_element(By.NAME, "pedimento")
    ped_input.send_keys(PEDIMENTO_FAKE)

    # Botón REAL
    btn = driver.find_element(By.XPATH, "//button[text()='Validar']")
    btn.click()

    time.sleep(3)

    print("🌐 URL después del submit:", driver.current_url)
    print("📄 HTML snippet:", driver.page_source[:400])

    # 1️⃣ NO debe ir a panel
    assert "/panel" not in driver.current_url

    # 2️⃣ Debe quedarse en validar
    assert driver.current_url.endswith("/validar")

    print("✅ CT-04 aprobado: pedimento inexistente NO avanza al panel")

    driver.quit()
test_pedimento_inexistente()