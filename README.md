# Desafio MBA Engenharia de Software com IA - Full Cycle

# 📑 Ingestão e Busca Semântica com LangChain e Postgres

Este projeto é uma implementação de um sistema de **RAG (Retrieval-Augmented Generation)**. Ele permite a ingestão de documentos PDF em um banco de dados vetorial PostgreSQL (utilizando a extensão `pgVector`) e a realização de perguntas via linha de comando (CLI) com respostas baseadas exclusivamente no conteúdo do documento.

## 🚀 Tecnologias Utilizadas

* **Linguagem:** Python 3.11+
* **Framework LLM:** [LangChain](https://www.langchain.com/)
* **Banco de Dados Vetorial:** PostgreSQL com a extensão [pgVector](https://github.com/pgvector/pgvector)
* **Modelos de IA (Google Gemini):**
    * Embeddings: `models/embedding-001`
    * LLM: `gemini-2.5-flash-lite`
* **Infraestrutura:** Docker & Docker Compose

## 📂 Estrutura do Projeto

```text
├── src/
│   ├── ingest.py         # Script para processar o PDF e salvar no banco
│   ├── search.py         # Lógica de busca vetorial e integração com LLM
│   ├── chat.py           # Interface de linha de comando (CLI)
├── document.pdf          # PDF que será processado
├── docker-compose.yml    # Configuração do banco de dados PostgreSQL
├── .env                  # Variáveis de ambiente (API Keys, DB URL)
├── requirements.txt      # Dependências do projeto
└── README.md             # Instruções de uso
```

## 🛠️ Configuração e Instalação
1. Clonar o Repositório

```
git clone <url-do-seu-repositorio>
cd <nome-da-pasta>
```

2. Ambiente Virtual e Dependências
Crie um ambiente virtual e instale as bibliotecas necessárias:

```
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto seguindo o modelo abaixo:

```
GOOGLE_API_KEY='sua_chave_aqui'
DATABASE_URL='postgresql+psycopg://postgres:postgres@localhost:5432/rag'
PG_VECTOR_COLLECTION='document_collection'
PDF_PATH='document.pdf'
EMBED_MODEL='models/embedding-001'
GEMINI_LLM_MODEL='gemini-2.5-flash-lite'
```

### 🏃 Como Executar
Siga a ordem abaixo para garantir que o sistema funcione corretamente:

1. Subir o Banco de Dados
Certifique-se de que o Docker está rodando e execute:

```
docker compose up -d
```

2. Ingestão do PDF
Este comando lerá o arquivo document.pdf, fará a quebra em pedaços (chunks) de 1000 caracteres e salvará os vetores no banco:

```
python src/ingest.py
```

3. Iniciar o Chat
Agora você pode interagir com o documento via CLI:

```
python src/chat.py
```


🧠 Regras de Resposta do Sistema
O sistema foi configurado para ser rigoroso conforme as diretrizes do desafio:

- Fidelidade ao Contexto: Ele só responde o que estiver no PDF.

- Sem Alucinações: Se a informação não for encontrada, a resposta padrão será: "Não tenho informações necessárias para responder sua pergunta."

- Sem Conhecimento Externo: O modelo ignora fatos externos se não estiverem no texto.


🛠️ Solução de Problemas
- Erro de conexão com o banco: Verifique se o container Docker está em execução (docker ps).

- Erro de API Key: Verifique se sua chave do Google AI Studio possui cotas disponíveis.