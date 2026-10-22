"""
Consultor Inteligente de Carreiras em TI - Base de Conhecimento
===============================================================
Autor: Gabriel Medeiros de Souza Costa
UNIPAC Barbacena - Ciência da Computação - Inteligência Artificial
Sistema Especialista baseado em regras (encadeamento para frente) usando Experta.

Funcionamento:
  1. As respostas da entrevista viram um fato `Perfil`.
  2. Cada regra @Rule casa um padrão do Perfil e "vota" em uma trilha (peso > 0)
     ou penaliza uma trilha (peso < 0, regras de desambiguação).
  3. Ao final, a trilha com maior pontuação é recomendada e as regras
     disparadas são devolvidas como justificativa.
"""
import collections
import collections.abc

# --- Compatibilidade: Experta 1.9.4 usa aliases removidos no Python 3.10+ ---
for _nome in ("Mapping", "MutableMapping", "Sequence"):
    if not hasattr(collections, _nome):
        setattr(collections, _nome, getattr(collections.abc, _nome))

from experta import Fact, KnowledgeEngine, L, Rule  # noqa: E402

# ---------------------------------------------------------------------------
# Trilhas
# ---------------------------------------------------------------------------
TRILHAS = {
    "BACKEND": "Desenvolvimento Back-end",
    "FRONTEND": "Desenvolvimento Front-end & UI/UX",
    "DATASCI": "Ciência de Dados e Machine Learning",
    "DATAENG": "Engenharia de Dados",
    "SEC": "Cibersegurança (Security / Pentesting)",
    "DEVOPS": "DevOps & SRE",
    "CLOUD": "Computação em Nuvem (Cloud Architecture)",
    "MOBILE": "Desenvolvimento Mobile",
    "QA": "Engenharia de Qualidade e Testes (QA)",
    "PM": "Gestão de Produtos (Product Management)",
}

DESCRICOES_TRILHAS = {
    "BACKEND": "Lógica de servidores, construção de APIs, regras de negócio e bancos de dados.",
    "FRONTEND": "Interfaces web responsivas, experiência do usuário e frameworks reativos.",
    "DATASCI": "Estatística, modelagem preditiva, análise de grandes massas de dados e IA.",
    "DATAENG": "Arquitetura de dados, pipelines (ETL/ELT) e infraestrutura para Data Lakes.",
    "SEC": "Defesa cibernética, análise de vulnerabilidades, criptografia e redes seguras.",
    "DEVOPS": "Automação de processos, integração e entrega contínua (CI/CD) e contêineres.",
    "CLOUD": "Planejamento, migração e gestão de infraestruturas escaláveis (AWS/Azure/GCP).",
    "MOBILE": "Ecossistema de dispositivos móveis (nativo ou Flutter/React Native).",
    "QA": "Testes automatizados, confiabilidade de software e processos de qualidade.",
    "PM": "Ponte entre negócio, design e desenvolvimento, metodologias ágeis e priorização.",
}

# ---------------------------------------------------------------------------
# Perguntas da entrevista (chave -> pergunta, {valor_interno: rótulo})
# ---------------------------------------------------------------------------
PERGUNTAS = {
    "matematica": (
        "Qual é a sua afinidade com matemática e estatística?",
        {"baixa": "Baixa", "media": "Média", "alta": "Alta"},
    ),
    "atuacao": (
        "O que você mais gostaria de fazer no seu dia a dia de trabalho?",
        {
            "algoritmos": "Escrever algoritmos lógicos e regras de negócio",
            "layouts": "Criar layouts e interfaces visuais",
            "servidores": "Lidar com servidores e ambientes de execução",
            "dados_brutos": "Analisar dados brutos em busca de padrões",
            "pipelines": "Coletar, limpar e movimentar grandes volumes de dados",
            "seguranca": "Garantir a segurança e procurar falhas",
            "automacao": "Automatizar processos de build, testes e publicação",
            "testes": "Testar sistemas e encontrar bugs",
            "negocio": "Conversar com usuários e decidir o que será construído",
        },
    ),
    "ferramenta": (
        "Qual linguagem/ferramenta você domina melhor hoje?",
        {
            "python": "Python",
            "javascript": "JavaScript",
            "sql": "SQL / Bancos de dados",
            "linux_redes": "Linux / Redes",
            "mobile_lang": "Dart / Kotlin / Swift / React Native",
            "nenhuma": "Nenhuma / Sou iniciante",
        },
    ),
    "entrega": (
        "Que tipo de entrega de valor mais te motiva?",
        {
            "produto_usuario": "O produto final que o usuário usa",
            "infraestrutura": "A infraestrutura que sustenta o sistema",
            "seguranca": "A segurança contra invasões",
            "insights": "Insights e previsões extraídos de dados",
            "dados_prontos": "Dados confiáveis e disponíveis para outras equipes",
            "qualidade": "Qualidade e confiabilidade do software",
            "valor_negocio": "Resultado e valor para o negócio",
        },
    ),
    "plataforma": (
        "Onde você prefere que o seu trabalho 'viva'?",
        {
            "web": "No navegador (web)",
            "mobile": "No celular (apps)",
            "nuvem": "Na nuvem / data centers",
            "indiferente": "Tanto faz",
        },
    ),
    "estilo": (
        "Qual é o seu estilo de trabalho predominante?",
        {
            "construir": "Programar e implementar funcionalidades",
            "desenhar": "Planejar e desenhar arquiteturas / soluções",
            "operar": "Automatizar e manter sistemas funcionando",
            "investigar": "Investigar, analisar e descobrir problemas",
            "coordenar": "Coordenar pessoas, prioridades e prazos",
        },
    ),
    "interacao": (
        "Quanto você gosta de interagir com pessoas e decisões de negócio?",
        {"baixa": "Pouco", "media": "Moderadamente", "alta": "Muito"},
    ),
}

# ---------------------------------------------------------------------------
# Metadados das regras: id -> (trilha, peso, explicação mostrada ao usuário)
# peso > 0 = evidência a favor | peso < 0 = penalidade (desambiguação)
# ---------------------------------------------------------------------------
REGRAS_META = {
    # Back-end
    "R01": ("BACKEND", 5, "Gosta de escrever algoritmos/regras de negócio, programa e domina Python ou SQL."),
    "R02": ("BACKEND", 4, "Quer lidar com servidores programando (Python, SQL ou JavaScript)."),
    "R03": ("BACKEND", 3, "Domina SQL e prefere trabalhar com lógica de negócio."),
    # Front-end
    "R04": ("FRONTEND", 5, "Gosta de criar layouts e quer entregar o produto final ao usuário na web."),
    "R05": ("FRONTEND", 4, "Domina JavaScript e gosta de criar interfaces visuais."),
    "R06": ("FRONTEND", 3, "Domina JavaScript, constrói e quer entregar o produto ao usuário na web."),
    # Mobile
    "R07": ("MOBILE", 5, "Quer entregar o produto ao usuário e prefere que ele viva no celular."),
    "R08": ("MOBILE", 5, "Domina uma linguagem/framework mobile (Dart, Kotlin, Swift, React Native)."),
    "R09": ("MOBILE", 3, "Prefere o celular como plataforma e gosta de layouts ou algoritmos."),
    "R10": ("FRONTEND", -2, "Prefere o celular em vez da web (penaliza Front-end a favor de Mobile)."),
    # Ciência de Dados
    "R11": ("DATASCI", 6, "Alta afinidade com matemática, analisa dados brutos e usa Python."),
    "R12": ("DATASCI", 4, "Valoriza insights/previsões e tem afinidade média ou alta com matemática."),
    "R13": ("DATASCI", 3, "Alta afinidade matemática, estilo investigativo e foco em insights."),
    "R14": ("DATASCI", -4, "Baixa afinidade com matemática/estatística (essencial para Ciência de Dados)."),
    "R15": ("DATASCI", -3, "Foco em mover/organizar dados (pipelines) aponta para Engenharia, não Ciência de Dados."),
    # Engenharia de Dados
    "R16": ("DATAENG", 6, "Gosta de construir pipelines de dados e domina Python ou SQL."),
    "R17": ("DATAENG", 4, "Quer entregar dados confiáveis e disponíveis para outras equipes."),
    "R18": ("DATAENG", 3, "Quer entregar dados prontos sem exigir alta afinidade matemática."),
    "R19": ("DATAENG", 3, "Analisa dados com SQL e afinidade matemática baixa/média (perfil de engenharia)."),
    # Cibersegurança
    "R20": ("SEC", 6, "Quer garantir segurança no dia a dia e entregar proteção contra invasões."),
    "R21": ("SEC", 4, "Domina Linux/Redes e gosta de procurar falhas de segurança."),
    "R22": ("SEC", 3, "Estilo investigativo com foco em segurança contra invasões."),
    "R23": ("SEC", 1, "Alta afinidade matemática combinada com segurança (criptografia)."),
    # DevOps
    "R24": ("DEVOPS", 6, "Gosta de automatizar processos e tem estilo de operar/manter sistemas."),
    "R25": ("DEVOPS", 4, "Domina Linux/Redes e gosta de automatizar build, testes e publicação."),
    "R26": ("DEVOPS", 3, "Foco em infraestrutura com estilo de operar e automatizar."),
    # Cloud
    "R27": ("CLOUD", 6, "Prefere a nuvem e gosta de planejar/desenhar arquiteturas."),
    "R28": ("CLOUD", 5, "Valoriza a infraestrutura que sustenta o sistema e gosta de desenhar soluções."),
    "R29": ("CLOUD", 3, "Lida com servidores e prefere o ambiente de nuvem."),
    # QA
    "R30": ("QA", 6, "Gosta de testar sistemas e valoriza qualidade e confiabilidade."),
    "R31": ("QA", 4, "Gosta de testar com estilo investigativo (caça bugs)."),
    "R32": ("QA", 3, "Valoriza qualidade, programa e usa Python ou JavaScript (testes automatizados)."),
    "R33": ("QA", 2, "Iniciante que gosta de testar sistemas (porta de entrada comum para QA)."),
    # Product Management
    "R34": ("PM", 6, "Quer decidir o que será construído e valoriza resultado para o negócio."),
    "R35": ("PM", 5, "Gosta muito de interagir com pessoas e tem estilo de coordenação."),
    "R36": ("PM", 3, "Gosta de negócio e de pessoas, mesmo sem domínio técnico de ferramentas."),
    "R37": ("PM", 3, "Valoriza o valor para o negócio e gosta de interagir com pessoas."),
    # Sinais fracos (uma atividade diária isolada já aponta uma direção)
    "R38": ("BACKEND", 2, "Sinal fraco: a atividade preferida (algoritmos/regras de negócio) é típica de Back-end."),
    "R39": ("FRONTEND", 2, "Sinal fraco: a atividade preferida (layouts visuais) é típica de Front-end."),
    "R40": ("DATASCI", 2, "Sinal fraco: a atividade preferida (analisar dados brutos) é típica de Ciência de Dados."),
    "R41": ("DATAENG", 2, "Sinal fraco: a atividade preferida (movimentar grandes volumes de dados) é típica de Eng. de Dados."),
    "R42": ("SEC", 2, "Sinal fraco: a atividade preferida (segurança) é típica de Cibersegurança."),
    "R43": ("DEVOPS", 2, "Sinal fraco: a atividade preferida (automação de processos) é típica de DevOps."),
    "R44": ("QA", 2, "Sinal fraco: a atividade preferida (testar sistemas) é típica de QA."),
    "R45": ("PM", 2, "Sinal fraco: a atividade preferida (decidir o que construir) é típica de Product Management."),
}


class Perfil(Fact):
    """Fato com as respostas da entrevista (uma chave por pergunta)."""


class ConsultorCarreiras(KnowledgeEngine):
    """Motor de inferência com forward chaining (Experta)."""

    def __init__(self):
        super().__init__()
        self.pontuacao = {k: 0 for k in TRILHAS}
        self.disparadas = []  # lista de dicts: id, trilha, peso, motivo

    # -- utilitário chamado pelo lado direito (RHS) de cada regra --------------
    def _votar(self, regra_id: str):
        trilha, peso, motivo = REGRAS_META[regra_id]
        self.pontuacao[trilha] += peso
        self.disparadas.append(
            {"id": regra_id, "trilha": trilha, "peso": peso, "motivo": motivo}
        )

    # =========================== BACK-END ===================================
    @Rule(Perfil(atuacao="algoritmos", estilo="construir", ferramenta=L("python") | L("sql")))
    def r01(self):
        self._votar("R01")

    @Rule(Perfil(atuacao="servidores", estilo="construir",
                 ferramenta=L("python") | L("sql") | L("javascript")))
    def r02(self):
        self._votar("R02")

    @Rule(Perfil(ferramenta="sql", atuacao="algoritmos"))
    def r03(self):
        self._votar("R03")

    # =========================== FRONT-END ==================================
    @Rule(Perfil(atuacao="layouts", entrega="produto_usuario",
                 plataforma=L("web") | L("indiferente")))
    def r04(self):
        self._votar("R04")

    @Rule(Perfil(ferramenta="javascript", atuacao="layouts"))
    def r05(self):
        self._votar("R05")

    @Rule(Perfil(ferramenta="javascript", entrega="produto_usuario",
                 estilo="construir", plataforma="web"))
    def r06(self):
        self._votar("R06")

    # =========================== MOBILE =====================================
    @Rule(Perfil(plataforma="mobile", entrega="produto_usuario"))
    def r07(self):
        self._votar("R07")

    @Rule(Perfil(ferramenta="mobile_lang"))
    def r08(self):
        self._votar("R08")

    @Rule(Perfil(plataforma="mobile", atuacao=L("layouts") | L("algoritmos")))
    def r09(self):
        self._votar("R09")

    @Rule(Perfil(plataforma="mobile", atuacao="layouts"))
    def r10(self):
        self._votar("R10")

    # =========================== CIÊNCIA DE DADOS ===========================
    @Rule(Perfil(matematica="alta", atuacao="dados_brutos", ferramenta="python"))
    def r11(self):
        self._votar("R11")

    @Rule(Perfil(entrega="insights", matematica=L("media") | L("alta")))
    def r12(self):
        self._votar("R12")

    @Rule(Perfil(matematica="alta", estilo="investigar", entrega="insights"))
    def r13(self):
        self._votar("R13")

    @Rule(Perfil(matematica="baixa", atuacao=L("dados_brutos") | L("pipelines"),
                 entrega=L("insights") | L("dados_prontos")))
    def r14(self):
        self._votar("R14")

    @Rule(Perfil(atuacao="pipelines"))
    def r15(self):
        self._votar("R15")

    # =========================== ENGENHARIA DE DADOS ========================
    @Rule(Perfil(atuacao="pipelines", ferramenta=L("python") | L("sql")))
    def r16(self):
        self._votar("R16")

    @Rule(Perfil(entrega="dados_prontos"))
    def r17(self):
        self._votar("R17")

    @Rule(Perfil(entrega="dados_prontos", matematica=L("baixa") | L("media")))
    def r18(self):
        self._votar("R18")

    @Rule(Perfil(atuacao="dados_brutos", ferramenta="sql",
                 matematica=L("baixa") | L("media")))
    def r19(self):
        self._votar("R19")

    # =========================== CIBERSEGURANÇA =============================
    @Rule(Perfil(atuacao="seguranca", entrega="seguranca"))
    def r20(self):
        self._votar("R20")

    @Rule(Perfil(ferramenta="linux_redes", atuacao="seguranca"))
    def r21(self):
        self._votar("R21")

    @Rule(Perfil(estilo="investigar", entrega="seguranca"))
    def r22(self):
        self._votar("R22")

    @Rule(Perfil(matematica="alta", atuacao="seguranca"))
    def r23(self):
        self._votar("R23")

    # =========================== DEVOPS & SRE ===============================
    @Rule(Perfil(atuacao="automacao", estilo="operar"))
    def r24(self):
        self._votar("R24")

    @Rule(Perfil(ferramenta="linux_redes", atuacao="automacao"))
    def r25(self):
        self._votar("R25")

    @Rule(Perfil(entrega="infraestrutura", estilo="operar"))
    def r26(self):
        self._votar("R26")

    # =========================== CLOUD ======================================
    @Rule(Perfil(plataforma="nuvem", estilo="desenhar"))
    def r27(self):
        self._votar("R27")

    @Rule(Perfil(entrega="infraestrutura", estilo="desenhar"))
    def r28(self):
        self._votar("R28")

    @Rule(Perfil(atuacao="servidores", plataforma="nuvem"))
    def r29(self):
        self._votar("R29")

    # =========================== QA =========================================
    @Rule(Perfil(atuacao="testes", entrega="qualidade"))
    def r30(self):
        self._votar("R30")

    @Rule(Perfil(atuacao="testes", estilo="investigar"))
    def r31(self):
        self._votar("R31")

    @Rule(Perfil(entrega="qualidade", estilo="construir",
                 ferramenta=L("python") | L("javascript")))
    def r32(self):
        self._votar("R32")

    @Rule(Perfil(atuacao="testes", ferramenta="nenhuma"))
    def r33(self):
        self._votar("R33")

    # =========================== PRODUCT MANAGEMENT =========================
    @Rule(Perfil(atuacao="negocio", entrega="valor_negocio"))
    def r34(self):
        self._votar("R34")

    @Rule(Perfil(interacao="alta", estilo="coordenar"))
    def r35(self):
        self._votar("R35")

    @Rule(Perfil(interacao="alta", ferramenta="nenhuma", atuacao="negocio"))
    def r36(self):
        self._votar("R36")

    @Rule(Perfil(entrega="valor_negocio", interacao=L("media") | L("alta")))
    def r37(self):
        self._votar("R37")


    # =========================== SINAIS FRACOS ==============================
    @Rule(Perfil(atuacao="algoritmos"))
    def r38(self):
        self._votar("R38")

    @Rule(Perfil(atuacao="layouts"))
    def r39(self):
        self._votar("R39")

    @Rule(Perfil(atuacao="dados_brutos"))
    def r40(self):
        self._votar("R40")

    @Rule(Perfil(atuacao="pipelines"))
    def r41(self):
        self._votar("R41")

    @Rule(Perfil(atuacao="seguranca"))
    def r42(self):
        self._votar("R42")

    @Rule(Perfil(atuacao="automacao"))
    def r43(self):
        self._votar("R43")

    @Rule(Perfil(atuacao="testes"))
    def r44(self):
        self._votar("R44")

    @Rule(Perfil(atuacao="negocio"))
    def r45(self):
        self._votar("R45")


# ---------------------------------------------------------------------------
# API de alto nível usada pela interface e pelos testes
# ---------------------------------------------------------------------------
# Ordem de desempate (primeiro = prioridade maior) quando a pontuação empata.
_ORDEM_DESEMPATE = list(TRILHAS.keys())


def diagnosticar(respostas: dict) -> dict:
    """Executa o motor de inferência e devolve o diagnóstico.

    Retorna:
        {
          "trilha": chave da trilha recomendada,
          "nome": nome da trilha,
          "pontuacao": {chave: pontos},
          "ranking": [(chave, pontos), ...] em ordem decrescente,
          "regras": [regras disparadas que favorecem a trilha vencedora],
          "todas_regras": [todas as regras disparadas],
          "confianca": % dos pontos positivos concentrados na trilha vencedora,
        }
    """
    engine = ConsultorCarreiras()
    engine.reset()
    engine.declare(Perfil(**respostas))
    engine.run()

    def chave_ordem(k):
        n_regras = sum(1 for r in engine.disparadas if r["trilha"] == k and r["peso"] > 0)
        return (-engine.pontuacao[k], -n_regras, _ORDEM_DESEMPATE.index(k))

    ranking = sorted(TRILHAS.keys(), key=chave_ordem)
    vencedora = ranking[0]

    p1 = engine.pontuacao[vencedora]
    soma_positivos = sum(v for v in engine.pontuacao.values() if v > 0)
    # Fatia dos pontos positivos concentrada na trilha vencedora (0-100)
    confianca = 0 if p1 <= 0 else round(100 * p1 / soma_positivos)

    regras_vencedora = sorted(
        (r for r in engine.disparadas if r["trilha"] == vencedora),
        key=lambda r: -r["peso"],
    )
    return {
        "trilha": vencedora,
        "nome": TRILHAS[vencedora],
        "pontuacao": dict(engine.pontuacao),
        "ranking": [(k, engine.pontuacao[k]) for k in ranking],
        "regras": regras_vencedora,
        "todas_regras": list(engine.disparadas),
        "confianca": confianca,
    }
