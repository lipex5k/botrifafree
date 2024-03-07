import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from fake_useragent import UserAgent

# Função para enviar dados para o webhook do Discord
def send_to_discord(comprador, telefone, situacao, qtd_cotas, num_cotas):
    webhook_url = "https://discordapp.com/api/webhooks/1215033007820382279/IOaK6LiJYlscyfM-t44pT-CHWHW5Bv8AkkRtt9FLJ1gO1wyHbU8Ti-mc6LGtHzN29kmd"

    data = {
        "content": f"**Comprador:** {comprador}\n**Telefone:** {telefone}\n**Situação:** {situacao}\n**Quantidade de Cotas:** {qtd_cotas}\n**Número de Cotas:** {num_cotas}"
    }

    requests.post(webhook_url, json=data)

# Função principal
def main():
    # Pergunte ao usuário as informações necessárias
    telefone = input("Digite o número de telefone: ")
    quantidade_repeticoes = int(input("Digite a quantidade de vezes que deseja repetir o processo: "))

    # Configuração do Selenium
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1200,600')

    # Adicionar agente de usuário aleatório
    user_agent = UserAgent()
    chrome_options.add_argument(f"user-agent={user_agent.random}")

    # Loop para repetir o processo
    for _ in range(quantidade_repeticoes):
        # Inicializar o driver do Selenium
        driver = webdriver.Chrome(options=chrome_options)

        # Abrir o site
        url = 'https://sepremios.com/rifa/sorteio-gratuito-mais-de-20k-quem-adquirir-mais-de-uma-cota-nao-ira-concorrer-159'
        driver.get(url)

        # Clicar no botão
        rif_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[4]/div[7]/button"))
        )
        rif_button.click()

        # Preencher formulário
        input_field_tel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form[1]/div/div/div[2]/div[1]/div/input"))
        )
        input_field_tel.send_keys(telefone)

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/form[1]/div/div/div[2]/div[2]/button"))
        )
        submit_button.click()

        # Aguardar 20 segundos
        time.sleep(10)

        # Obter informações
        comprador = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/div/div[2]/div[2]").text
        telefone_info = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/div/div[3]/div[2]").text
        situacao = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/div/div[5]/div[2]").text
        qtd_cotas = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/div/div[6]/div[2]").text
        num_cotas = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/div/div[8]/div[2]").text

        # Enviar para o Discord
        send_to_discord(comprador, telefone_info, situacao, qtd_cotas, num_cotas)

        # Fechar a página
        driver.quit()

    # Imprimir "processo concluído" no final
    print("Processo concluído.")

# Executar o script
if __name__ == "__main__":
    main()
