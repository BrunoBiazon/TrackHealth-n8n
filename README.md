# TrackHealth-n8n

## Sobre
Este projeto consiste em uma arquitetura de automação operando no **n8n**, projetada para o monitoramento rigoroso de indivíduos altamente treinados. O sistema atua como um diário de telemetria esportiva e fisiológica, capturando dados desestruturados via Telegram e extraindo métricas precisas de hardwares esportivos, estruturando tudo em um banco de dados relacional no Google Sheets com o auxílio de IA.



## Arquitetura 
O sistema é dividido em dois Workflows independentes, garantindo escalabilidade, isolamento de falhas e integridade dos dados.

### ⚙️ Workflow 1: Inserção e Feedback de Dados
Insere dados sobre **Treino, Sono, Medicação, Hidratção** e permite um **Feedback** dos dados gerados por IA a partir do **período de dias** requisitado.
<img width="1494" height="599" alt="image" src="https://github.com/user-attachments/assets/4ebbedd2-6f95-4764-a205-94ac514d87f1" />

* **Gatilho:** Recebe mensagens de texto via Telegram Bot API.
* **Processamento (Groq):** A IA atua como um middleware de ETL, interpretando a mensagem em linguagem natural e convertendo-a em um payload JSON estrito (classificando a intenção entre `TREINO`, `SONO`, `HIDRATACAO`, `MEDICAMENTO` , `PESO` ou `FEEDBACK`).
* **Tratamento de Dados(Code)**: Formata para JSON para o formato correto utilizando JavaScript.
* **Condicional (If):** Lê a categoria do JSON e direciona os dados, se for categoria `FEEDBACK` vai para o fluxo de Feedback dos dados, se não vai para a inserção na planilha.
* **Inserção:** Preenche o Sheets com as informações dada pelo usuário, e posteriormente retorna um feeback no telegramBot sobre o cadastro bem sucedido.

* **Feedback:** Lê a planilha com os dados no Sheets, filtrando pelo período de DIAS requisitados pelo usuário. Com isso, a automação utiliza novamenta uma IA para análisar os dados, para posteriormente retornar ao usuário.

### 🏃‍♂️ Workflow 2: Automação Garmin Connect ("Ponte")
**Insere informações do cardio a partir da salvamento do exercício no relogio garmin**, sem a necessidade da API do Garmin ou até mesmo Strava, utilizando um **Script agendado no GitHub Action**.
* **Gatilho e Extração:** Um script em Python, agendado via cron job no GitHub Actions:
* ** Script Python:** Simula o login no garmin, extrai os últimos 5 treinos com o `Data Cardio`,`Nome Cardio`, `Distância (metros)`,`BPM máximo`,`BPM médio`,`Calorias`, `ID treino`
* **Tratamento de Dados:** Um nó JavaScript no n8n processa e converte os dados brutos (achatando o JSON ) para a inserção no Sheets, e converte distância em metros -> KM.
* **Armazenamento Seguro (Upsert):** Salva as métricas limpas na aba "Cardio" do Google Sheets. Utiliza a lógica de *Update or Append* baseada na chave primária (`id_treino`) para garantir que os dados não sejam duplicados a cada execução do script.

---

## 🛠️ Stack Tecnológica
* **Orquestração de Fluxos:** n8n
* **Infraestrutura e Deploy (n8n):** Render (Web Service Free)
* **Banco de Dados Interno (n8n):** Render (PostgreSQL 18 Free)
* **Automação de Scripts:** GitHub Actions (Secrets & Cron Jobs)
* **Interfaces e APIs:** Telegram Bot API, Google Sheets API
* **Agente IA:** Groq (Modelo: `llama-3.3-70b-versatile`)

---

## 🚀 Como Usar na Prática
* **Registro de Rotina:** Envie mensagem no seu bot do Telegram, como *"Dormi 6 horas e meia hoje"* ou *"Treino de peito: supino top set 100kg pra 6 reps, 2 series válidas"*. O Workflow 1 entenderá o contexto, estruturará os dados e os salvará na aba correta.
* **Feedback:** Envie mensagem no Bot, como "Quero um Feedback dos últimos 30 dias". O Worflow 1 entenderá o contexto, gerara uma análise com IA e retornará esse feedback no telegram.
* **Métricas de Cardio e Performance:** Apenas inicie e finalize suas atividades normalmente no seu relógio Garmin. O fluxo em Python no GitHub Actions fará a extração periodicamente ( A cada duas horas ) e o Workflow 2 atualizará sua planilha em background sem nenhuma intervenção manual.
