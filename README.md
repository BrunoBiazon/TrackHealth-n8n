# TrackHealt-n8n

## Sobre
Este projeto consiste em uma arquitetura de automação em 3 camadas operando no **n8n**. O sistema atua como um diário de telemetria esportiva e fisiológica, capturando dados desestruturados via Telegram e Strava, estruturando-os no Google Sheets e gerando análises de alta precisão com IA (Google Gemini).

---

## Arquitetura 
O sistema é dividido em três Workflows independentes, garantindo escalabilidade, isolamento de falhas e respostas rápidas.

### ⚙️ Workflow 1: Ingestão de Dados (ETL via Telegram)
Atua como a porta de entrada principal de dados manuais.
* **Gatilho:** Recebe mensagens de texto via Telegram Bot.
* **Processamento (Gemini):** A IA atua como um middleware (ETL), lendo a mensagem em linguagem natural e convertendo-a em um payload JSON estrito (classificando a intenção entre `TREINO`, `SONO`, `HIDRATACAO`, `MEDICAMENTO`, `PESO` ou `FEEDBACK`).
* **Roteamento (Switch):** Lê a categoria do JSON e direciona os dados para a aba correspondente no Google Sheets, inserindo a data/hora exata.
* **Desvio:** Se a intenção for `FEEDBACK`, os dados não vão para as planilhas. O fluxo aciona o Workflow 3, passando o período desejado (ex: 7 ou 30 dias).

### 🏃‍♂️ Workflow 2: Automação Strava (Background)
Opera de forma silenciosa e 100% automatizada para capturar o gasto energético e a resposta cardiovascular.
* **Gatilho:** Webhook da API do Strava ouvindo eventos de *Activity Created*.
* **Tratamento de Dados:** Um nó de código extrai e converte os dados brutos (tempo decorrido para minutos, batimentos médios/máximos e calorias gastas).
* **Armazenamento:** Salva a métrica limpa na aba "Cardio" do Google Sheets.

### 🧠 Workflow 3: O Cérebro Analítico (Feedback Inteligente)
O núcleo de inteligência do projeto. Gera relatórios cruzando todas as variáveis do seu estilo de vida e treinamento.
* **Gatilho:** Acionado exclusivamente pelo Workflow 1 quando o usuário pede uma análise (ex: `"/feedback semanal"`).
* **Busca Paralela:** Executa leituras simultâneas nas 6 abas do Google Sheets (Treino, Cardio, Peso, Sono, Água, Medicamento), filtrando apenas os registros do período solicitado.
* **Consolidação e Análise:** Junta todos os dados em um único bloco de contexto e os envia para um modelo LLM avançado (como o Gemini 1.5 Pro).
* **Entrega:** A IA analisa a correlação entre peso, performance no treino, gasto de cardio e recuperação (sono/hidratação), retornando um relatório formatado em Markdown diretamente no Telegram com apontamentos de falhas e diretrizes para o próximo ciclo.

---

## 🛠️ Stack Tecnológica
* **Orquestração:** n8n
* **Bancos de Dados:** Google Sheets API
* **Interfaces de Entrada:** Telegram Bot API, Strava Webhook API
* **Processamento e IA:** Google Gemini API (ETL de normalização e Análise de Dados)

---

## 🚀 Como Usar na Prática
* **Registro de Rotina:** Envie mensagens casuais no Telegram como *"Dormi 6 horas e meia hoje"* ou *"Treino de peito: supino top set 100kg pra 6 reps"*. O Workflow 1 entenderá, estruturará e salvará.
* **Cardio:** Apenas inicie e finalize sua atividade no Strava. O Workflow 2 cuida do resto em background.
* **Análise:** Quando quiser ajustar a rota, mande *"Gere meu feedback semanal"* no Telegram. O Workflow 3 varrerá seus dados e entregará o relatório completo com os próximos passos.