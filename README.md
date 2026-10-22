# ☀️ BREVE. — Resumo Matinal Diário

Briefing matinal executivo e minimalista, lido diretamente no smartphone com curadoria editorial anti-fake news (2 a 3 notícias por tema) gerada via **Google Gemini**.

## 🚀 Tecnologias

- **Backend:** FastAPI, Uvicorn, SQLModel (SQLite)
- **Frontend:** Jinja2 Templates, Tailwind CSS (Mobile-first, Dark Mode editorial)
- **IA:** Google Gemini 1.5 Flash via `google-genai`
- **Agendador:** APScheduler (disparo diário às 06:30 BRT)
- **E-mail:** Resend API
- **Hospedagem:** Render.com (Web Service com CI/CD direto via GitHub)

---

## 🛠️ Como rodar localmente

1. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   source .venv/bin/activate # Linux/Mac
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o arquivo `.env` a partir de `.env.example`:
   ```env
   GEMINI_API_KEY=sua_chave_gemini
   RESEND_API_KEY=sua_chave_resend
   NOTIFICATION_EMAIL=antoniosouza1997@gmail.com
   APP_BASE_URL=http://localhost:8000
   TIMEZONE=America/Sao_Paulo
   ```

4. Inicie o servidor:
   ```bash
   uvicorn app.main:app --reload
   ```
   Acesse: `http://localhost:8000`

---

## ☁️ Deploy no Render (render.com)

1. Conecte sua conta do GitHub ao Render.
2. Crie um novo **Web Service** selecionando o repositório `breve-news`.
3. Configure os campos:
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Em **Environment Variables**, adicione:
   - `GEMINI_API_KEY`: sua chave de API
   - `RESEND_API_KEY`: sua chave de API do Resend
   - `NOTIFICATION_EMAIL`: `antoniosouza1997@gmail.com`
   - `APP_BASE_URL`: URL gerada pelo Render (ex: `https://breve-news.onrender.com`)
   - `TIMEZONE`: `America/Sao_Paulo`
   - `DATABASE_URL`: `sqlite:///./briefing.db`
