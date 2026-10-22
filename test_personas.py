"""Validação com personas (Fase 4).

Execute:  python test_personas.py      (ou: pytest test_personas.py)
"""
from base_conhecimento import REGRAS_META, TRILHAS, diagnosticar
from personas import PERSONAS


def test_personas_recebem_trilha_esperada():
    for persona in PERSONAS:
        resultado = diagnosticar(persona["respostas"])
        assert resultado["trilha"] == persona["esperada"], (
            f"{persona['nome']}: esperado {persona['esperada']}, "
            f"obtido {resultado['trilha']} | ranking: {resultado['ranking'][:3]}"
        )


def test_quantidade_minima_de_regras_e_personas():
    assert len(REGRAS_META) >= 25
    assert len(PERSONAS) >= 4
    assert {p["esperada"] for p in PERSONAS} == set(TRILHAS)  # todas as 10 trilhas


def test_ciencia_vs_engenharia_de_dados():
    """Mesma base de dados, perfis diferentes -> trilhas diferentes."""
    cientista = dict(matematica="alta", atuacao="dados_brutos", ferramenta="python",
                     entrega="insights", plataforma="indiferente",
                     estilo="investigar", interacao="media")
    engenheiro = dict(matematica="baixa", atuacao="pipelines", ferramenta="sql",
                      entrega="dados_prontos", plataforma="nuvem",
                      estilo="construir", interacao="baixa")
    assert diagnosticar(cientista)["trilha"] == "DATASCI"
    assert diagnosticar(engenheiro)["trilha"] == "DATAENG"


if __name__ == "__main__":
    acertos = 0
    for p in PERSONAS:
        r = diagnosticar(p["respostas"])
        ok = r["trilha"] == p["esperada"]
        acertos += ok
        print(f"[{'OK' if ok else 'ERRO'}] {p['nome']:<36} esperado={p['esperada']:<8} "
              f"obtido={r['trilha']:<8} pontos={r['pontuacao'][r['trilha']]:>3} "
              f"confiança={r['confianca']}%")
    print(f"\n{acertos}/{len(PERSONAS)} personas corretas")
