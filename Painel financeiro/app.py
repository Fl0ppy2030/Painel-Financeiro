import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# ================= CONFIG =================
st.set_page_config(
    page_title="Painel Financeiro",
    layout="wide",
)

st.title("📊 Painel Financeiro")
st.write("Acompanhe suas finanças de forma simples e intuitiva.")

# ================= FUNÇÕES =================
def obter_dolar():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    return requests.get(url).json()["USDBRL"]

def historico_dolar(dias=30):
    url = f"https://economia.awesomeapi.com.br/json/daily/USD-BRL/{dias}"
    return requests.get(url).json()

def obter_selic():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4189/dados?formato=json"
    return float(requests.get(url).json()[-1]["valor"])

# ================= ABAS =================
aba_dolar, aba_selic, aba_emprestimo, aba_invest = st.tabs(
    ["💵 Dólar", "📈 Selic & CDI", "💰 Empréstimo", "💸 Investimentos"]
)

# ================= ABA DÓLAR =================
with aba_dolar:
    st.subheader("Cotação do Dólar hoje")

    dolar = obter_dolar()
    valor = float(dolar["bid"])
    variacao = float(dolar["varBid"])
    percentual = float(dolar["pctChange"])

    c1, c2, c3 = st.columns(3)
    c1.metric("Valor", f"R$ {valor:.2f}")
    c2.metric("Variação", f"{variacao:+.2f}", delta=f"{variacao:+.2f}")
    c3.metric("Percentual", f"{percentual:+.2f}%", delta=f"{percentual:+.2f}%")

    if st.button("📉 Ver gráfico do dólar"):
        dados = historico_dolar(30)
        df = pd.DataFrame({
            "Data": [datetime.fromtimestamp(int(i["timestamp"])) for i in dados],
            "Valor": [float(i["bid"]) for i in dados]
        })
        fig = px.line(df, x="Data", y="Valor", title="Variação do Dólar (30 dias)")
        st.plotly_chart(fig, use_container_width=True)

# ================= ABA SELIC =================
with aba_selic:
    st.subheader("Taxas de Juros")

    selic = obter_selic()
    cdi = selic - 0.10

    st.metric("Selic atual", f"{selic:.2f}% ao ano")
    st.metric("CDI (estimado)", f"{cdi:.2f}% ao ano")

    st.caption("CDI estimado com base na taxa Selic atual")

# ================= ABA EMPRÉSTIMO =================
with aba_emprestimo:
    st.subheader("💰 Simulador de Empréstimo")

    valor_emp = st.number_input("Valor do empréstimo (R$)", 0.0, step=100.0, value=10000.0)
    taxa = st.number_input("Taxa de juros mensal (%)", 0.0, step=0.1, value=5.0)
    prazo = st.number_input("Prazo (meses)", 1, step=1, value=12)

    if st.button("Simular Empréstimo"):
        i = taxa / 100
        n = prazo

        parcela = valor_emp * (i / (1 - (1 + i) ** -n))
        total = parcela * n
        juros = total - valor_emp

        st.metric("Parcela mensal", f"R$ {parcela:,.2f}")
        st.metric("Total pago", f"R$ {total:,.2f}")
        st.metric("Juros totais", f"R$ {juros:,.2f}")

# ================= ABA INVESTIMENTOS =================
with aba_invest:
    st.subheader("💸 Simulador de Investimento (CDB / CDI)")

    investimento = st.number_input("Valor inicial (R$)", 0.0, step=100.0, value=1000.0)
    prazo_dias = st.number_input("Prazo (dias)", 1, step=1, value=365)
    percentual_cdi = st.number_input("% do CDI", 0.0, step=5.0, value=100.0)
    aporte_mensal = st.number_input("Aporte mensal (R$)", 0.0, step=50.0, value=0.0)

    if st.button("Simular investimento"):
        taxa_cdi_anual = cdi / 100
        taxa_real = taxa_cdi_anual * (percentual_cdi / 100)
        taxa_diaria = (1 + taxa_real) ** (1 / 252) - 1

        saldo = investimento
        valores = []

        for dia in range(1, prazo_dias + 1):
            saldo *= (1 + taxa_diaria)
            if dia % 30 == 0:
                saldo += aporte_mensal
            valores.append(saldo)

        total_aportes = investimento + (aporte_mensal * (prazo_dias // 30))
        rendimento_bruto = saldo - total_aportes

        if prazo_dias <= 180:
            ir = 0.225
        elif prazo_dias <= 360:
            ir = 0.20
        elif prazo_dias <= 720:
            ir = 0.175
        else:
            ir = 0.15

        imposto = rendimento_bruto * ir
        rendimento_liquido = rendimento_bruto - imposto
        valor_final = total_aportes + rendimento_liquido

        poupanca = investimento * ((1 + 0.005) ** (prazo_dias / 30))

        st.metric("Rendimento bruto", f"R$ {rendimento_bruto:,.2f}")
        st.metric("Imposto de renda", f"R$ {imposto:,.2f}")
        st.metric("Rendimento líquido", f"R$ {rendimento_liquido:,.2f}")
        st.metric("💰 Valor final (CDI)", f"R$ {valor_final:,.2f}")
        st.metric(
            "🏦 Valor na poupança",
            f"R$ {poupanca:,.2f}",
            delta=f"R$ {(valor_final - poupanca):,.2f}"
        )

        df = pd.DataFrame({
            "Dia": range(1, prazo_dias + 1),
            "Saldo": valores
        })

        st.subheader("📈 Evolução do investimento")
        st.line_chart(df.set_index("Dia"))

        st.caption("🟣 Simulação equivalente a um CDB 100% do CDI (Caixinha Nubank)")
