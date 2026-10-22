Consultor Inteligente de Carreiras em TI

Sistema Especialista baseado em regras (encadeamento para frente) que entrevista o usuário e recomenda
**uma entre 10 trilhas de carreira em TI**, justificando a decisão com as regras disparadas.

**Autor:** Gabriel Medeiros de Souza Costa  
> UNIPAC Barbacena · Ciência da Computação · Inteligência Artificial · Prof. Felipe Roncalli de Paula Carneiro

## Tecnologias

- Python 3.10+
- [Experta](https://github.com/nilp0inter/experta) — motor de regras (`Fact`, `@Rule`, `KnowledgeEngine`)
- [Streamlit](https://streamlit.io) — interface web
- GitHub — controle de versão

## Instalação e execução

```bash
# 1. clonar o repositório
git clone https://github.com/Gbr521/consultor-carreiras-ti
cd consultor-carreiras-ti

# 2. (opcional) criar ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. instalar dependências
pip install -r requirements.txt

# 4. executar a aplicação web
streamlit run app.py

# 5. (opcional) validar com as personas de teste
python test_personas.py        # ou: pytest -v
```

A aplicação abre em `http://localhost:8501`.

> **Nota sobre o Experta e Python 3.10+:** a versão 1.9.4 do Experta usa `collections.Mapping`,
> removido no Python 3.10. O módulo `base_conhecimento.py` aplica um pequeno *patch* de
> compatibilidade antes de importar a biblioteca, então nenhuma ação extra é necessária.

## Estrutura do projeto

```
consultor_carreiras/
├── app.py                  # Fase 3 - interface Streamlit
├── base_conhecimento.py    # Fases 1 e 2 - fatos, regras (@Rule) e motor de inferência
├── personas.py             # Fase 4 - personas de teste
├── test_personas.py      # Fase 4 - validação automatizada
├── requirements.txt
└── README.md
```

## Como funciona

1. **Entrevista** — 7 perguntas objetivas viram um único fato `Perfil(...)` no Experta.
2. **Inferência** — as 45 regras `@Rule` casam padrões do `Perfil`. Cada regra disparada
   adiciona **pontos** (evidência a favor) ou **subtrai pontos** (regras de desambiguação) de uma trilha.
3. **Decisão** — vence a trilha com maior pontuação (desempate: nº de regras favoráveis e ordem fixa).
4. **Justificativa** — a interface mostra a trilha, a pontuação, o ranking e **as regras que levaram à conclusão**.

### Fase 1 — Perguntas da entrevista

| Chave | Pergunta | Opções |
|---|---|---|
| `matematica` | Qual é a sua afinidade com matemática e estatística? | Baixa; Média; Alta |
| `atuacao` | O que você mais gostaria de fazer no seu dia a dia de trabalho? | Escrever algoritmos lógicos e regras de negócio; Criar layouts e interfaces visuais; Lidar com servidores e ambientes de execução; Analisar dados brutos em busca de padrões; Coletar, limpar e movimentar grandes volumes de dados; Garantir a segurança e procurar falhas; Automatizar processos de build, testes e publicação; Testar sistemas e encontrar bugs; Conversar com usuários e decidir o que será construído |
| `ferramenta` | Qual linguagem/ferramenta você domina melhor hoje? | Python; JavaScript; SQL / Bancos de dados; Linux / Redes; Dart / Kotlin / Swift / React Native; Nenhuma / Sou iniciante |
| `entrega` | Que tipo de entrega de valor mais te motiva? | O produto final que o usuário usa; A infraestrutura que sustenta o sistema; A segurança contra invasões; Insights e previsões extraídos de dados; Dados confiáveis e disponíveis para outras equipes; Qualidade e confiabilidade do software; Resultado e valor para o negócio |
| `plataforma` | Onde você prefere que o seu trabalho 'viva'? | No navegador (web); No celular (apps); Na nuvem / data centers; Tanto faz |
| `estilo` | Qual é o seu estilo de trabalho predominante? | Programar e implementar funcionalidades; Planejar e desenhar arquiteturas / soluções; Automatizar e manter sistemas funcionando; Investigar, analisar e descobrir problemas; Coordenar pessoas, prioridades e prazos |
| `interacao` | Quanto você gosta de interagir com pessoas e decisões de negócio? | Pouco; Moderadamente; Muito |

### Fase 1 — Matriz de decisão

Cada linha é uma regra `SE <condição> ENTÃO <trilha> += peso`. Pesos negativos são **regras de
desambiguação**: por exemplo, *R14/R15* impedem que um perfil de pipelines ou de baixa afinidade
matemática seja classificado como **Cientista de Dados**, e *R19/R18* empurram esse perfil para
**Engenharia de Dados**.

#### Desenvolvimento Back-end

| Regra | Peso | Condição |
|---|:---:|---|
| R01 | +5 | Gosta de escrever algoritmos/regras de negócio, programa e domina Python ou SQL. |
| R02 | +4 | Quer lidar com servidores programando (Python, SQL ou JavaScript). |
| R03 | +3 | Domina SQL e prefere trabalhar com lógica de negócio. |
| R38 | +2 | Sinal fraco: a atividade preferida (algoritmos/regras de negócio) é típica de Back-end. |

#### Desenvolvimento Front-end & UI/UX

| Regra | Peso | Condição |
|---|:---:|---|
| R04 | +5 | Gosta de criar layouts e quer entregar o produto final ao usuário na web. |
| R05 | +4 | Domina JavaScript e gosta de criar interfaces visuais. |
| R06 | +3 | Domina JavaScript, constrói e quer entregar o produto ao usuário na web. |
| R10 | -2 | Prefere o celular em vez da web (penaliza Front-end a favor de Mobile). |
| R39 | +2 | Sinal fraco: a atividade preferida (layouts visuais) é típica de Front-end. |

#### Ciência de Dados e Machine Learning

| Regra | Peso | Condição |
|---|:---:|---|
| R11 | +6 | Alta afinidade com matemática, analisa dados brutos e usa Python. |
| R12 | +4 | Valoriza insights/previsões e tem afinidade média ou alta com matemática. |
| R13 | +3 | Alta afinidade matemática, estilo investigativo e foco em insights. |
| R14 | -4 | Baixa afinidade com matemática/estatística (essencial para Ciência de Dados). |
| R15 | -3 | Foco em mover/organizar dados (pipelines) aponta para Engenharia, não Ciência de Dados. |
| R40 | +2 | Sinal fraco: a atividade preferida (analisar dados brutos) é típica de Ciência de Dados. |

#### Engenharia de Dados

| Regra | Peso | Condição |
|---|:---:|---|
| R16 | +6 | Gosta de construir pipelines de dados e domina Python ou SQL. |
| R17 | +4 | Quer entregar dados confiáveis e disponíveis para outras equipes. |
| R18 | +3 | Quer entregar dados prontos sem exigir alta afinidade matemática. |
| R19 | +3 | Analisa dados com SQL e afinidade matemática baixa/média (perfil de engenharia). |
| R41 | +2 | Sinal fraco: a atividade preferida (movimentar grandes volumes de dados) é típica de Eng. de Dados. |

#### Cibersegurança (Security / Pentesting)

| Regra | Peso | Condição |
|---|:---:|---|
| R20 | +6 | Quer garantir segurança no dia a dia e entregar proteção contra invasões. |
| R21 | +4 | Domina Linux/Redes e gosta de procurar falhas de segurança. |
| R22 | +3 | Estilo investigativo com foco em segurança contra invasões. |
| R23 | +1 | Alta afinidade matemática combinada com segurança (criptografia). |
| R42 | +2 | Sinal fraco: a atividade preferida (segurança) é típica de Cibersegurança. |

#### DevOps & SRE

| Regra | Peso | Condição |
|---|:---:|---|
| R24 | +6 | Gosta de automatizar processos e tem estilo de operar/manter sistemas. |
| R25 | +4 | Domina Linux/Redes e gosta de automatizar build, testes e publicação. |
| R26 | +3 | Foco em infraestrutura com estilo de operar e automatizar. |
| R43 | +2 | Sinal fraco: a atividade preferida (automação de processos) é típica de DevOps. |

#### Computação em Nuvem (Cloud Architecture)

| Regra | Peso | Condição |
|---|:---:|---|
| R27 | +6 | Prefere a nuvem e gosta de planejar/desenhar arquiteturas. |
| R28 | +5 | Valoriza a infraestrutura que sustenta o sistema e gosta de desenhar soluções. |
| R29 | +3 | Lida com servidores e prefere o ambiente de nuvem. |

#### Desenvolvimento Mobile

| Regra | Peso | Condição |
|---|:---:|---|
| R07 | +5 | Quer entregar o produto ao usuário e prefere que ele viva no celular. |
| R08 | +5 | Domina uma linguagem/framework mobile (Dart, Kotlin, Swift, React Native). |
| R09 | +3 | Prefere o celular como plataforma e gosta de layouts ou algoritmos. |

#### Engenharia de Qualidade e Testes (QA)

| Regra | Peso | Condição |
|---|:---:|---|
| R30 | +6 | Gosta de testar sistemas e valoriza qualidade e confiabilidade. |
| R31 | +4 | Gosta de testar com estilo investigativo (caça bugs). |
| R32 | +3 | Valoriza qualidade, programa e usa Python ou JavaScript (testes automatizados). |
| R33 | +2 | Iniciante que gosta de testar sistemas (porta de entrada comum para QA). |
| R44 | +2 | Sinal fraco: a atividade preferida (testar sistemas) é típica de QA. |

#### Gestão de Produtos (Product Management)

| Regra | Peso | Condição |
|---|:---:|---|
| R34 | +6 | Quer decidir o que será construído e valoriza resultado para o negócio. |
| R35 | +5 | Gosta muito de interagir com pessoas e tem estilo de coordenação. |
| R36 | +3 | Gosta de negócio e de pessoas, mesmo sem domínio técnico de ferramentas. |
| R37 | +3 | Valoriza o valor para o negócio e gosta de interagir com pessoas. |
| R45 | +2 | Sinal fraco: a atividade preferida (decidir o que construir) é típica de Product Management. |

### Diferenciando Ciência de Dados × Engenharia de Dados

| Sinal | Ciência de Dados | Engenharia de Dados |
|---|---|---|
| Matemática/estatística | Alta (R11, R12, R13); baixa **penaliza** (R14) | Baixa/Média tolerada (R18, R19) |
| Atividade | Analisar dados brutos (R11, R40) | Movimentar grandes volumes / pipelines (R16, R41); **penaliza** DS (R15) |
| Entrega de valor | Insights e previsões (R12, R13) | Dados confiáveis para outras equipes (R17, R18) |
| Estilo | Investigar | Construir |

## Validação com personas (Fase 4)

| Persona | Esperada | Obtida | Pontos | |
|---|---|---|:---:|:---:|
| Ana - Perfil analítico | Ciência de Dados e Machine Learning | Ciência de Dados e Machine Learning | 15 | ✅ |
| Bruno - Perfil infra/segurança | Cibersegurança (Security / Pentesting) | Cibersegurança (Security / Pentesting) | 15 | ✅ |
| Carla - Perfil visual/front-end | Desenvolvimento Front-end & UI/UX | Desenvolvimento Front-end & UI/UX | 14 | ✅ |
| Diego - Perfil negócios/produto | Gestão de Produtos (Product Management) | Gestão de Produtos (Product Management) | 19 | ✅ |
| Elisa - Perfil back-end | Desenvolvimento Back-end | Desenvolvimento Back-end | 7 | ✅ |
| Fábio - Perfil engenharia de dados | Engenharia de Dados | Engenharia de Dados | 15 | ✅ |
| Gabi - Perfil DevOps | DevOps & SRE | DevOps & SRE | 15 | ✅ |
| Hugo - Perfil cloud | Computação em Nuvem (Cloud Architecture) | Computação em Nuvem (Cloud Architecture) | 14 | ✅ |
| Iara - Perfil mobile | Desenvolvimento Mobile | Desenvolvimento Mobile | 13 | ✅ |
| João - Perfil QA | Engenharia de Qualidade e Testes (QA) | Engenharia de Qualidade e Testes (QA) | 12 | ✅ |

Execute `python test_personas.py` para reproduzir a tabela acima.

## Possíveis melhorias

- Permitir respostas múltiplas (ex.: duas ferramentas favoritas).
- Calibrar os pesos com dados reais de profissionais da área.
- Exportar o resultado da consulta em PDF.
