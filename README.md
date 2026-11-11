# RAG Insurance Assistant

A multi-agent AI assistant that answers customer questions about two insurance savings products, **Fidelidade Savings** and **PPR Evoluir**, using retrieval-augmented generation (RAG). Every answer is grounded in the official product documents, so the assistant explains real rates, fees, tax rules and conditions instead of inventing them.

Built as a team business case for the Master's in Data Science and Advanced Analytics at **NOVA IMS** (Business Cases with Data Science, Case 4).

## How it works

```
Customer question
      │
      ▼
┌──────────────┐     ┌──────────────────────────┐
│ Savings Bot  │◄────│ Astra DB vector store    │  (Fidelidade Savings documents)
└──────┬───────┘     └──────────────────────────┘
       │
┌──────────────┐     ┌──────────────────────────┐
│   PPR Bot    │◄────│ Astra DB vector store    │  (PPR Evoluir documents)
└──────┬───────┘     └──────────────────────────┘
       ▼
┌──────────────────┐
│  Answer Manager  │  combines the specialist answers into one clear, neutral reply
└──────┬───────────┘
       ▼
 Streamlit chat app
```

1. **Document preparation:** the product PDFs were converted to text (`preprocessing/pdf_to_text.ipynb`), split into chunks and embedded with **Azure OpenAI** `text-embedding-3-small`.
2. **One vector store per product:** each product's documents live in a separate **Astra DB** collection, so each agent only retrieves from its own product.
3. **Specialist agents:** a Savings agent and a PPR agent (**GPT-4o-mini**) answer using only the retrieved passages, with instructions to give exact rates and practical examples in plain language (`prompts/agent_prompts.txt`).
4. **Answer Manager:** a final agent merges the answers into one neutral, easy-to-read reply, comparing products only when the customer asks.
5. **Interface:** a **Streamlit** app sends the question to the deployed **Langflow** flow and shows the answer.

## Tech stack

Langflow · Azure OpenAI (GPT-4o-mini, text-embedding-3-small) · Astra DB (vector database) · Streamlit · Python

## Repository structure

| Folder | Contents |
|---|---|
| `langflow/` | The exported Langflow flow (API keys removed) |
| `app/` | Streamlit chat interface |
| `prompts/` | The instructions given to each agent (in Portuguese) |
| `preprocessing/` | Notebook converting the product PDFs to text |

## Running it

1. Import `langflow/insurance_assistant_flow.json` into Langflow, add your own Azure OpenAI and Astra DB credentials, and upload the product documents.
2. In `app/`, copy `.env.example` to `.env` and fill in your Langflow token and flow URL.
3. Install and run:
   ```bash
   pip install -r app/requirements.txt
   streamlit run app/main.py
   ```

No credentials or source documents are included in this repository.

## Team

Group D: Chloé Deschanel, Diogo Carvalho, Ingrid Gil López and Rúben Marques.
