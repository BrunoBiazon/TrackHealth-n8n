# 📊 TrackHealth

## 🎯 Sobre o Projeto
O **TrackHealth-n8n** é uma arquitetura de automação operando no **n8n**, projetada para o monitoramento rigoroso de performance esportiva e métricas de saúde. O sistema atua capturando dados desestruturados via Telegram e extraindo informações precisas de hardwares esportivos (Garmin). Utilizando IA, os dados são convertidos, estruturados e armazenados em uma planilha Google Sheets para consultas e análises.

## 🏗️ Arquitetura do Sistema
O sistema agora é dividido em **três Workflows independentes**, garantindo maior escalabilidade, isolamento de falhas, organização,menos gastos de tokens e integridade dos dados.

### ⚙️ Workflow 1: Ingestão de Dados e Roteamento
#### Atua como o "recepcionista" do sistema. É responsável por processar a mensagem do usuário no bot do telegram, estruturar os dados e decidir qual caminho a automação deve seguir.
<img width="1229" height="632" alt="image" src="https://github.com/user-attachments/assets/746ffa63-4ad7-4b2c-9618-703a05ecdead" />

* **Gatilho (Trigger):** Recepção de mensagens de texto via Telegram Bot API.
* **Processamento (Groq):** Serve como ETL, interpretando a entrada em linguagem natural e a converte em um *payload* JSON estrito, classificando a intenção do usuário entre as chaves: `TREINO`, `SONO`, `HIDRATACAO`, `MEDICAMENTO`, `PESO` ou `FEEDBACK`.
* **Tratamento de Dados (Code):** Nós em JavaScript formatam e normalizam o JSON gerado.
* **Roteamento (Switch):** Lê a categoria estruturada.
  * **Se Inserção:** Preenche a aba correspondente no Google Sheets e retorna uma confirmação de cadastro via Telegram.
  * **Se Feedback:** Interrompe o fluxo local e **aciona o Workflow 3**, repassando parâmetros essenciais via *Execute Workflow* (como o `ChatID` do usuário e o `PeriodoDias` requisitado).

### 🏃‍♂️ Workflow 2: Integração Automática (Garmin Connect)
#### Um fluxo assíncrono que extrai os dados dos cardios passivamente a partir do salvamento de atividades no relógio Garmin, eliminando a dependência de APIs restritas oficiais.
<img width="1229" height="613" alt="image" src="https://github.com/user-attachments/assets/a4ad7bc2-dc30-45ef-b970-9a242e76a909" />

* **Extração (GitHub Actions):** Um script autônomo em Python, agendado via *cron job*, simula autenticação no Garmin Connect e coleta os 5 últimos registros contendo: `Data do Cardio`, `Nome do Exercício`, `Distância (m)`, `BPM Máximo`, `BPM Médio`, `Calorias` e `ID do Treino`.
* **Tratamento de Dados (n8n):** O *payload* é recebido pelo n8n, onde um nó JavaScript faz tratamento do JSON e converte unidades brutas (ex: metros para quilômetros).
* **Armazenamento Seguro (Upsert):** Salva as métricas na página "Cardio" do Google Sheets. A operação utiliza a lógica de *Update or Append* usando o `id_treino` como chave primária, garantindo a idempotência e evitando duplicação.

### 🧠 Workflow 3: Motor de Análise e Feedback (IA)
#### Fluxo dedicado exclusivamente à extração e análise analítica de dados consolidados. É acionado sob demanda de forma isolada para não sobrecarregar o fluxo de ingestão.
<img width="1229" height="632" alt="image" src="https://github.com/user-attachments/assets/83511db1-3db3-4479-9116-64ab9d11c12f" />

* **Gatilho Interno:** Acionado pelo Workflow 1 via nó *When Executed by Another Workflow*, recebendo de forma global o `ChatID` e o `PeriodoDias`.
* **Busca de Dados:** Lê o banco de dados do Google Sheets, filtrando as métricas exatamente pelo intervalo de dias solicitado.
* **Análise Fisiológica (Groq):** Injeta o histórico de dados em um novo *prompt* complexo. A IA atua como analista de performance, cruzando dados de carga, descanso e métricas cardiovasculares para gerar *insights*.
* **Retorno (Telegram):** Resgata o `ChatID` recebido no gatilho inicial para enviar o relatório de performance diretamente para o celular do usuário em uma mensagem única.
  
## Google Sheets 📝
#### Estruturado a partir das categorias, separando por páginas. Com isso, permite a melhor escalabilidade, manutenção e diminuição de latência / consumo de tokens dos agentes.
<img width="1427" height="810" alt="image" src="https://github.com/user-attachments/assets/a9190075-1451-461c-9f80-958850629222" />


## ☁️ Infraestrutura e Deploy

O deploy deste projeto foi realizado com custo zero, utilizando a plataforma **Render** para a hospedagem do sistema e do banco de dados. Abaixo estão os recursos e configurações utilizados na infraestrutura:

* **Plataforma de Hospedagem:** Render (Plano Free).
* **Banco de Dados Relacional:** PostgreSQL 18, operando como um serviço de banco de dados interno no Render.
* **Motor da Automação (Web Service):** Imagem Docker oficial do n8n (`docker.n8n.io/n8nio/n8n`), rodando em uma instância de Web Service com 512MB de RAM e CPU compartilhada.
* **Variáveis de Ambiente (Environment Variables):** Utilizadas no Web Service para garantir a comunicação segura com o banco de dados interno e o funcionamento correto dos gatilhos:
  * Variáveis de conexão com o banco: `DB_TYPE` (como `postgresdb`), `DB_POSTGRESDB_HOST`, `DB_POSTGRESDB_PORT`, `DB_POSTGRESDB_DATABASE`, `DB_POSTGRESDB_USER` e `DB_POSTGRESDB_PASSWORD`.
  * Variáveis de sistema do n8n: `N8N_ENCRYPTION_KEY` e `WEBHOOK_URL` (URL pública do serviço, essencial para a comunicação com o Telegram Bot API).
* **Gestão de Disponibilidade:** Integração com o **UptimeRobot**, responsável por realizar requisições HTTP a cada 14 minutos na URL do Web Service. Isso impede que a instância gratuita do Render entre em modo de suspensão, mantendo a automação 100% responsiva.
---

## 🛠️ Stack Tecnológica
* **Orquestração de Fluxos:** n8n
* **Infraestrutura e Deploy (n8n):** Render (Web Service Free)
* **Banco de Dados Interno (n8n):** Render (PostgreSQL 18 Free)
* **Automação e Scripts:** GitHub Actions: Secrets para credênciais e Cron Job para automatizar o script,
* **Interfaces e APIs:** Telegram Bot API, Google Sheets API
* **Inteligência Artificial:** Groq (Modelo: `llama-3.3-70b-versatile`) - versão free
* **Linguagens:** JavaScript (nós n8n) e Python (Script)
  

---

## 🚀 Como Usar na Prática
* **Registro de Rotina:** Envie mensagens orgânicas no seu bot do Telegram, como *"Dormi 6 horas e meia hoje"* ou *"Treino de peito: supino top set 100kg pra 6 reps, 2 séries válidas"*. O Workflow 1 entenderá o contexto e fará a estruturação no banco automaticamente.
* **Análise de Desempenho (Feedback):** Peça um balanço enviando *"Quero um feedback dos últimos 30 dias"*. O Workflow 1 delegará a tarefa para o Workflow 3, que fará a *query* na base de dados, processará com a IA e retornará um relatório avançado via Telegram.
* **Telemetria de Cardio:** Apenas inicie e conclua suas atividades físicas no relógio Garmin. O *Cron Job* em background fará a extração periodicamente (a cada duas horas) e o Workflow 2 manterá sua planilha sincronizada sem nenhuma intervenção manual.
