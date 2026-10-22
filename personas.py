"""Personas de teste (Fase 4). Cada persona traz as respostas e a trilha esperada."""

PERSONAS = [
    # ---- As 4 personas exigidas no enunciado -------------------------------
    {
        "nome": "Ana - Perfil analítico",
        "descricao": "Adora estatística, trabalha com Python e quer extrair previsões de dados.",
        "esperada": "DATASCI",
        "respostas": {
            "matematica": "alta", "atuacao": "dados_brutos", "ferramenta": "python",
            "entrega": "insights", "plataforma": "indiferente",
            "estilo": "investigar", "interacao": "media",
        },
    },
    {
        "nome": "Bruno - Perfil infra/segurança",
        "descricao": "Vive no terminal Linux, gosta de redes e de caçar vulnerabilidades.",
        "esperada": "SEC",
        "respostas": {
            "matematica": "media", "atuacao": "seguranca", "ferramenta": "linux_redes",
            "entrega": "seguranca", "plataforma": "indiferente",
            "estilo": "investigar", "interacao": "baixa",
        },
    },
    {
        "nome": "Carla - Perfil visual/front-end",
        "descricao": "Ama criar interfaces bonitas em JavaScript para o navegador.",
        "esperada": "FRONTEND",
        "respostas": {
            "matematica": "baixa", "atuacao": "layouts", "ferramenta": "javascript",
            "entrega": "produto_usuario", "plataforma": "web",
            "estilo": "construir", "interacao": "media",
        },
    },
    {
        "nome": "Diego - Perfil negócios/produto",
        "descricao": "Iniciante em programação, adora conversar com usuários e priorizar entregas.",
        "esperada": "PM",
        "respostas": {
            "matematica": "media", "atuacao": "negocio", "ferramenta": "nenhuma",
            "entrega": "valor_negocio", "plataforma": "indiferente",
            "estilo": "coordenar", "interacao": "alta",
        },
    },
    # ---- Personas adicionais: cobrem as demais trilhas ---------------------
    {
        "nome": "Elisa - Perfil back-end",
        "descricao": "Gosta de modelar regras de negócio e APIs em Python com bancos de dados.",
        "esperada": "BACKEND",
        "respostas": {
            "matematica": "media", "atuacao": "algoritmos", "ferramenta": "python",
            "entrega": "produto_usuario", "plataforma": "web",
            "estilo": "construir", "interacao": "baixa",
        },
    },
    {
        "nome": "Fábio - Perfil engenharia de dados",
        "descricao": "Monta pipelines ETL em Python/SQL e quer dados confiáveis para todos.",
        "esperada": "DATAENG",
        "respostas": {
            "matematica": "media", "atuacao": "pipelines", "ferramenta": "sql",
            "entrega": "dados_prontos", "plataforma": "nuvem",
            "estilo": "construir", "interacao": "baixa",
        },
    },
    {
        "nome": "Gabi - Perfil DevOps",
        "descricao": "Automatiza deploys, domina Linux e gosta de manter tudo no ar.",
        "esperada": "DEVOPS",
        "respostas": {
            "matematica": "baixa", "atuacao": "automacao", "ferramenta": "linux_redes",
            "entrega": "infraestrutura", "plataforma": "indiferente",
            "estilo": "operar", "interacao": "baixa",
        },
    },
    {
        "nome": "Hugo - Perfil cloud",
        "descricao": "Gosta de desenhar arquiteturas escaláveis e migrar sistemas para a nuvem.",
        "esperada": "CLOUD",
        "respostas": {
            "matematica": "media", "atuacao": "servidores", "ferramenta": "linux_redes",
            "entrega": "infraestrutura", "plataforma": "nuvem",
            "estilo": "desenhar", "interacao": "media",
        },
    },
    {
        "nome": "Iara - Perfil mobile",
        "descricao": "Desenvolve apps em Flutter/Kotlin e quer que o produto viva no celular.",
        "esperada": "MOBILE",
        "respostas": {
            "matematica": "media", "atuacao": "layouts", "ferramenta": "mobile_lang",
            "entrega": "produto_usuario", "plataforma": "mobile",
            "estilo": "construir", "interacao": "media",
        },
    },
    {
        "nome": "João - Perfil QA",
        "descricao": "Metódico, adora encontrar bugs e garantir a qualidade do software.",
        "esperada": "QA",
        "respostas": {
            "matematica": "media", "atuacao": "testes", "ferramenta": "python",
            "entrega": "qualidade", "plataforma": "indiferente",
            "estilo": "investigar", "interacao": "media",
        },
    },
]
