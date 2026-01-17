import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_postgres import PGVector

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("EMBED_MODEL"))

store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True,
)

llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_LLM_MODEL", "gemini-2.5-flash-lite"),
    temperature=0.0
)

def search_prompt(question: str) -> str:
    # Busca os 10 resultados mais relevantes conforme requisito
    docs_with_scores = store.similarity_search_with_score(question, k=10)

    if not docs_with_scores:
        return "Não tenho informações necessárias para responder sua pergunta."

    # Concatena apenas o conteúdo dos documentos
    contexto_str = "\n\n".join(doc.page_content for doc, score in docs_with_scores)

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | llm

    # Passa as variáveis separadamente para o template
    response = chain.invoke({
        "contexto": contexto_str,
        "pergunta": question
    })

    return response.content