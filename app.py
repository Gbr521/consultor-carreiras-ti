"""Consultor Inteligente de Carreiras em TI - Interface Streamlit.

Autor: Gabriel Medeiros de Souza Costa
Execute:  streamlit run app.py
"""
import streamlit as st

from base_conhecimento import (
    DESCRICOES_TRILHAS,
    PERGUNTAS,
    REGRAS_META,
    TRILHAS,
    diagnosticar,
)
from personas import PERSONAS

st.set_page_config(page_title="Consultor de Carreiras em TI", page_icon="🧭", layout="centered")

# ---------------------------------------------------------------------------
# Estado: permite carregar uma persona de teste nos campos da entrevista
# ---------------------------------------------------------------------------
for chave in PERGUNTAS:
    st.session_state.setdefault(f"resp_{chave}", None)


def carregar_persona():
    nome = st.session_state.get("persona_escolhida")
    if nome == "— nenhuma —":
        return
    persona = next(p for p in PERSONAS if p["nome"] == nome)
    for chave, valor in persona["respostas"].items():
        st.session_state[f"resp_{chave}"] = valor


with st.sidebar:
    st.header("🧪 Personas de teste")
    st.caption("Preenche a entrevista automaticamente para demonstrar o sistema.")
    st.selectbox(
        "Carregar persona",
        ["— nenhuma —"] + [p["nome"] for p in PERSONAS],
        key="persona_escolhida",
        on_change=carregar_persona,
    )
    st.divider()
    st.caption("Autor: Gabriel Medeiros de Souza Costa")
    st.caption("UNIPAC Barbacena · Inteligência Artificial")
    st.caption(f"Base de conhecimento: **{len(REGRAS_META)} regras** · **{len(TRILHAS)} trilhas**")

st.title("🧭 Consultor Inteligente de Carreiras em TI")
st.write(
    "Sistema especialista baseado em regras (Experta). Responda à entrevista e descubra "
    "qual das **10 trilhas** combina mais com você — com a justificativa das regras disparadas."
)

aba_entrevista, aba_matriz, aba_trilhas = st.tabs(
    ["📝 Entrevista", "📊 Matriz de decisão", "🗺️ As 10 trilhas"]
)

# ---------------------------------------------------------------------------
# Aba 1 - Entrevista + resultado
# ---------------------------------------------------------------------------
with aba_entrevista:
    respostas = {}
    for chave, (pergunta, opcoes) in PERGUNTAS.items():
        respostas[chave] = st.radio(
            pergunta,
            options=list(opcoes.keys()),
            format_func=lambda k, o=opcoes: o[k],
            index=None,
            key=f"resp_{chave}",
        )

    faltando = [c for c, v in respostas.items() if v is None]
    consultar = st.button("🔍 Descobrir minha trilha", type="primary", disabled=bool(faltando))
    if faltando:
        st.caption(f"Responda todas as perguntas para continuar ({len(faltando)} pendente(s)).")

    if consultar:
        res = diagnosticar(respostas)

        if res["pontuacao"][res["trilha"]] <= 0:
            st.warning(
                "Suas respostas não ativaram regras suficientes para uma recomendação "
                "segura. Revise as respostas (elas parecem apontar em direções diferentes) "
                "e tente novamente."
            )
        else:
            st.success(f"### Trilha recomendada: {res['nome']}")
            st.write(DESCRICOES_TRILHAS[res["trilha"]])
            c1, c2 = st.columns(2)
            c1.metric("Pontuação", res["pontuacao"][res["trilha"]])
            c2.metric("Concentração de evidências", f"{res['confianca']}%")

            st.subheader("Por que essa recomendação?")
            st.caption("Regras disparadas que levaram a essa conclusão:")
            for r in res["regras"]:
                sinal = "➕" if r["peso"] > 0 else "➖"
                st.markdown(f"{sinal} **{r['id']}** (peso {r['peso']:+d}) — {r['motivo']}")

            outras = [r for r in res["todas_regras"] if r["trilha"] != res["trilha"]]
            with st.expander("Ver regras disparadas para outras trilhas"):
                if outras:
                    for r in sorted(outras, key=lambda r: -r["peso"]):
                        st.markdown(
                            f"**{r['id']}** → {TRILHAS[r['trilha']]} "
                            f"(peso {r['peso']:+d}): {r['motivo']}"
                        )
                else:
                    st.write("Nenhuma outra trilha foi favorecida pelas suas respostas.")

            st.subheader("Ranking de trilhas")
            positivos = [(k, p) for k, p in res["ranking"] if p > 0]
            st.bar_chart({TRILHAS[k]: p for k, p in positivos}, horizontal=True)
            if len(positivos) > 1:
                segunda = positivos[1][0]
                st.info(
                    f"Segunda opção: **{TRILHAS[segunda]}** "
                    f"({res['pontuacao'][segunda]} pts)."
                )

# ---------------------------------------------------------------------------
# Aba 2 - Matriz de decisão (gerada a partir da própria base de conhecimento)
# ---------------------------------------------------------------------------
with aba_matriz:
    st.write(
        "Tabela de decisão: cada regra, a trilha que ela favorece (ou penaliza) e o seu peso. "
        "A trilha com maior soma de pesos vence."
    )
    filtro = st.selectbox("Filtrar por trilha", ["Todas"] + list(TRILHAS.values()))
    linhas = [
        {"Regra": rid, "Trilha": TRILHAS[t], "Peso": p, "Condição (em linguagem natural)": m}
        for rid, (t, p, m) in REGRAS_META.items()
        if filtro in ("Todas", TRILHAS[t])
    ]
    st.dataframe(linhas, width="stretch", hide_index=True)

# ---------------------------------------------------------------------------
# Aba 3 - Catálogo das trilhas
# ---------------------------------------------------------------------------
with aba_trilhas:
    for chave, nome in TRILHAS.items():
        st.markdown(f"**{nome}** — {DESCRICOES_TRILHAS[chave]}")
