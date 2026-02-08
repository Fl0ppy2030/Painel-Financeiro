# 📊 Painel Financeiro — Projeto de Estudo

Este projeto foi desenvolvido com o objetivo de **estudar e praticar conceitos financeiros**, ao mesmo tempo em que aprofunda conhecimentos em **lógica de programação, Python e desenvolvimento de aplicações interativas**.

O painel reúne informações financeiras reais e simuladores, apresentados de forma simples e intuitiva, utilizando o framework **Streamlit**.

---

## 🎯 Objetivos do Projeto

- Compreender conceitos financeiros do dia a dia, como:
  - Cotação do dólar
  - Taxa Selic e CDI
  - Juros compostos
  - Imposto de renda sobre investimentos
- Praticar:
  - Lógica de programação
  - Estruturação de código em Python
  - Consumo de APIs públicas
- Aprender novas ferramentas e conceitos, como:
  - Desenvolvimento de dashboards interativos
  - Uso do Streamlit
  - Visualização de dados
  - Deploy de aplicações web

---

## 🧩 Funcionalidades

- 💵 **Cotação do Dólar**
  - Valor atual
  - Variação diária
  - Gráfico histórico

- 📈 **Taxa Selic e CDI**
  - Exibição da taxa Selic atual
  - Estimativa do CDI com base na Selic

- 💰 **Simulador de Empréstimo**
  - Cálculo de parcela mensal
  - Total pago
  - Juros totais

- 💸 **Simulador de Investimentos (CDB / CDI)**
  - Simulação equivalente a um CDB atrelado ao CDI (ex: Caixinha Nubank)
  - Juros compostos
  - Aportes mensais
  - Cálculo de imposto de renda regressivo
  - Comparação com a poupança
  - Gráfico de evolução do investimento

---

## 🛠️ Tecnologias Utilizadas

- **Python**
- **Streamlit**
- **Requests**
- **Pandas**
- **Plotly**

---

## 🌐 Fontes de Dados

- Cotação do dólar:  
  - API AwesomeAPI
- Taxa Selic:  
  - API do Banco Central do Brasil

---

## 🚀 Execução do Projeto

Para rodar o projeto localmente:

```bash
pip install -r requirements.txt
streamlit run app.py
