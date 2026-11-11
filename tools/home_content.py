# -*- coding: utf-8 -*-
"""
I testi della home, nelle due lingue, uno accanto all'altro.

Perche' esiste: fino all'11/11/2026 la home era due file HTML scritti a mano
(index.html e it/index.html), e ogni modifica di testo andava ripetuta in entrambi.
Qui ogni frase si scrive una volta sola come T(italiano, inglese): se una delle due
manca, si vede subito. La struttura della pagina sta in build_home.py.

Regole di scrittura, da website-context nella vault:
- niente em dash, niente corporate speak
- TIG Factory si nomina, i suoi clienti no
- su ToroPulse nessun dettaglio di stack o architettura

Dopo ogni modifica: python tools/build_home.py --write
"""


def T(it, en):
    """Una frase nelle due lingue."""
    return {"it": it, "en": en}


LINKS = {
    "toropulse": "https://toropulse.app",
    "spotify": "https://open.spotify.com/show/033j5ueQUdbVL57XTdu9TF",
    "apple": "https://podcasts.apple.com/us/podcast/fincast-ai/id6807076540",
    "youtube": "https://youtube.com/playlist?list=PL62zLK--DCehR0PF5Pl2Ok9Ay8Voc3Zw4",
    "fincast": "https://fincast.holtibitri.com/",
    "meeting_repo": "https://github.com/holtibitri-arch/AI-Meeting-Assistant",
    "linkedin": "https://linkedin.com/in/holtibitri",
    "github": "https://github.com/holtibitri-arch",
    "email": "info@holtibitri.com",
    "post_if": "https://www.linkedin.com/feed/update/urn:li:activity:7452989725663084544/",
}

# Pagine interne che cambiano indirizzo con la lingua.
GUIDE_LLM = T(
    "/it/articoli/llm-wiki-obsidian-secondo-cervello-ai/",
    "/articles/llm-wiki-obsidian-second-brain-ai/",
)
GUIDE_MEETING = T(
    "/it/articoli/trascrivere-riunioni-in-locale-senza-cloud/",
    "/articles/transcribe-meetings-locally-without-cloud/",
)

CONTENT = {
    # ------------------------------------------------------------------ meta
    "meta": {
        "title": T(
            "Holti Bitri | CTO: agenti AI e persone, una squadra sola",
            "Holti Bitri | CTO: AI agents and people, one team",
        ),
        # Fra 70 e 160 caratteri, altrimenti la build si ferma: Bing Webmaster Tools
        # segnala come errore una description piu' lunga, e i motori la tagliano.
        # L'11/11/2026 la prima versione era di 197 caratteri ed e' stata segnalata.
        "description": T(
            "Holti Bitri, CTO di TIG Factory. Progetto flussi in cui agenti AI e persone "
            "costruiscono software insieme. In produzione: ToroPulse e AI FinCast.",
            "Holti Bitri, CTO at TIG Factory. I design workflows where AI agents and people "
            "build software together. In production: ToroPulse and AI FinCast.",
        ),
        "og_title": T(
            "Agenti AI e persone, una squadra sola. La progetto io.",
            "AI agents and people, one team. I design it.",
        ),
        "og_description": T(
            "Holti Bitri, CTO. Progetto e guido flussi in cui agenti AI e persone "
            "costruiscono software insieme: regole scritte, un controllo a ogni "
            "passaggio, decisioni umane.",
            "Holti Bitri, CTO. I design and lead workflows where AI agents and people "
            "build software together: written rules, a check at every step, human decisions.",
        ),
        "job_title": "CTO & AI Innovator",
        # Data dell'ultima modifica vera ai testi. Si cambia a mano: finisce nei dati
        # strutturati, in og:updated_time e, tramite build_sitemap.py, nel lastmod
        # della sitemap. E' il segnale con cui i motori capiscono di dover ripassare.
        "updated": "2026-11-11",
        # Temi su cui i motori e i sistemi AI possono associare la persona.
        "knows_about": T(
            [
                "Agenti AI nello sviluppo software",
                "Flussi di lavoro agentici",
                "Sviluppo software con agenti AI e persone",
                "Claude Code",
                "Architettura software",
                "Microsoft Azure",
                ".NET",
                "Integrazione di sistemi",
                "Direzione tecnica",
            ],
            [
                "AI agents in software engineering",
                "Agentic workflows",
                "Software delivery with AI agents and people",
                "Claude Code",
                "Software architecture",
                "Microsoft Azure",
                ".NET",
                "Systems integration",
                "Technical leadership",
            ],
        ),
        # Apertura di llms.txt: in terza persona, perche' e' la frase che un sistema
        # AI puo' citare cosi' com'e' per dire chi e' Holti.
        "llms_summary": (
            "Holti Bitri is CTO at TIG Factory in Milan, Italy. He designs and leads "
            "workflows where AI agents and people build software together: agents get "
            "written rules and a check at every step, people keep the architecture and "
            "the decisions. Eighteen years of enterprise software, from .NET developer to CTO."
        ),
    },
    # ------------------------------------------------------------------- nav
    "nav": [
        {"href": "#about", "label": T("Chi sono", "About")},
        {"href": "#method", "label": T("Come lavoro", "How I work")},
        {"href": "#projects", "label": T("Progetti", "Projects")},
        {"href": "#experience", "label": T("Esperienza", "Experience")},
        {"href": "#writing", "label": T("Articoli", "Writing")},
        {"href": "#contact", "label": T("Contatti", "Contact")},
    ],
    "menu_label": T("Menu", "Menu"),
    # ------------------------------------------------------------------ hero
    "hero": {
        "eyebrow": T("Holti Bitri · CTO · Milano", "Holti Bitri · CTO · Milan"),
        "claim": T(
            ["Agenti AI e persone,", "una squadra sola."],
            ["AI agents and people,", "one team."],
        ),
        "claim_accent": T("La progetto io.", "I design it."),
        "sub": T(
            "Progetto e guido flussi in cui agenti AI e persone costruiscono software "
            "insieme. Agli agenti regole scritte e un controllo a ogni passaggio. "
            "Alle persone l'architettura e le decisioni.",
            "I design and lead workflows where AI agents and people build software "
            "together. Agents get written rules and a check at every step. "
            "People keep the architecture and the decisions.",
        ),
        "cta_primary": T("Come lavoro", "How I work"),
        "cta_secondary": T("Scrivimi", "Get in touch"),
    },
    # ----------------------------------------------------------------- about
    "about": {
        "label": T("Chi sono", "About"),
        "paragraphs": [
            T(
                "Scrivo software dal 2008: sviluppatore .NET e Oracle in Monte dei Paschi "
                "di Siena, poi integrazione di sistemi, architettura, la guida di un'area "
                "di innovazione. Oggi sono CTO di TIG Factory.",
                "I have been writing software since 2008: .NET and Oracle developer at "
                "Monte dei Paschi di Siena, then systems integration, architecture, and "
                "leading an innovation unit. Today I am CTO at TIG Factory.",
            ),
            T(
                "Il mio lavoro ha cambiato forma. Il codice lo scrivono in gran parte gli "
                "agenti AI. Io decido l'architettura, scrivo le regole con cui lavorano, "
                "metto i controlli e rispondo di quello che va in produzione.",
                "My job has changed shape. Most of the code is now written by AI agents. "
                "I decide the architecture, write the rules they work by, set the checks, "
                "and answer for what goes to production.",
            ),
            T(
                "Non è un esperimento. È il modo in cui costruisco una piattaforma di "
                "trading, un podcast che esce ogni mattina senza di me e gli strumenti "
                "che i colleghi in TIG usano tutti i giorni.",
                "This is not an experiment. It is how I build a trading platform, a "
                "podcast that ships every morning without me, and the tools my "
                "colleagues at TIG use every day.",
            ),
            T(
                "Prima di arrivarci ho lavorato dentro PwC, Medtronic Italia, Reply (per "
                "Eurizon) e Magneti Marelli, quattro anni in Nexive, otto in Cloudia "
                "Research da architetto a Innovation Director. Lì ho imparato cosa serve "
                "a un software per reggere in azienda, ed è quello che oggi chiedo agli agenti.",
                "Before that I worked inside PwC, Medtronic Italia, Reply (for Eurizon) "
                "and Magneti Marelli, spent four years at Nexive and eight at Cloudia "
                "Research, from architect to Innovation Director. That is where I learned "
                "what software needs to hold up in a company, and it is what I now ask of the agents.",
            ),
            T(
                "Certificato Microsoft dal 2011 (MCSD, MCTS) e Anthropic dal 2026 "
                "(Claude Code, Claude Cowork).",
                "Microsoft certified since 2011 (MCSD, MCTS), Anthropic certified since "
                "2026 (Claude Code, Claude Cowork).",
            ),
        ],
        "avatar_alt": T(
            "Holti Bitri, CTO di TIG Factory",
            "Holti Bitri, CTO at TIG Factory",
        ),
        "stats": [
            {
                "number": "18",
                "label": T("Anni di software in produzione", "Years of software in production"),
            },
            {
                "number": "100+",
                "label": T(
                    "Episodi di AI FinCast usciti senza intervento umano",
                    "AI FinCast episodes shipped with no human intervention",
                ),
            },
        ],
        "clients_label": T("Ho lavorato con", "Worked with"),
        "clients": [
            "PwC",
            "Medtronic Italia",
            "Reply / Eurizon",
            "Magneti Marelli",
            "Monte dei Paschi di Siena",
            "Nexive",
        ],
    },
    # ---------------------------------------------------------------- method
    "method": {
        "label": T("Come lavoro", "How I work"),
        "title": T(
            ["Cinque regole,", "nate da cose che girano."],
            ["Five rules,", "learned from things that run."],
        ),
        "rules": [
            {
                "title": T("Prima si decide se l'AI serve", "First, decide whether AI is needed"),
                "text": T(
                    "Un cliente mi ha chiesto l'AI. Dopo trenta minuti era chiaro che gli "
                    "serviva un if. Saperlo dire fa parte del lavoro.",
                    "A client asked me for AI. Thirty minutes in, it was clear he needed "
                    "an if statement. Being able to say so is part of the job.",
                ),
                "link": {
                    "href": LINKS["post_if"],
                    "label": T("Leggi il post", "Read the post"),
                    "external": True,
                },
            },
            {
                "title": T(
                    "All'agente si dà un contratto, non un prompt",
                    "Agents get a contract, not a prompt",
                ),
                "text": T(
                    "Ruolo, regole, fonti, cosa non deve mai fare. Scritto, versionato, "
                    "corretto a ogni errore. In TIG Factory la conoscenza aziendale è "
                    "tenuta da un agente con una regola in cima: non inventare mai nulla.",
                    "Role, rules, sources, what it must never do. Written down, versioned, "
                    "corrected after every mistake. At TIG Factory the company knowledge "
                    "base is kept by an agent with one rule at the top: never make anything up.",
                ),
                "link": {
                    "href": GUIDE_LLM,
                    "label": T("Leggi la guida", "Read the guide"),
                    "external": False,
                },
            },
            {
                "title": T(
                    "I dati sensibili non arrivano al modello",
                    "Sensitive data never reaches the model",
                ),
                "text": T(
                    "In TIG una verifica sul database di produzione richiedeva mezz'ora a "
                    "mano. Oggi richiede pochi secondi: i dati personali vengono "
                    "mascherati sul PC e al modello arriva solo il riepilogo.",
                    "At TIG, a check on the production database used to take half an hour "
                    "by hand. Now it takes seconds: personal data is masked on the PC and "
                    "the model only gets the summary.",
                ),
                "link": {
                    "href": GUIDE_MEETING,
                    "label": T(
                        "Un altro caso: riunioni trascritte in locale",
                        "Another case: meetings transcribed locally",
                    ),
                    "external": False,
                },
            },
            {
                "title": T("Ogni passaggio ha un controllo", "Every step has a check"),
                "text": T(
                    "Un agente che scrive senza verifica produce codice veloce e problemi "
                    "lenti. Test, revisione e collaudo stanno dentro il flusso, non dopo.",
                    "An agent that writes without verification produces fast code and "
                    "slow problems. Tests, review and acceptance live inside the workflow, "
                    "not after it.",
                ),
            },
            {
                "title": T("Le decisioni restano alle persone", "Decisions stay with people"),
                "text": T(
                    "Gli agenti propongono, scrivono, verificano. Cosa costruire, con "
                    "quale architettura e quando va in produzione lo decide chi ne risponde.",
                    "Agents propose, write and verify. What to build, on which "
                    "architecture and when it ships is decided by whoever answers for it.",
                ),
            },
        ],
    },
    # -------------------------------------------------------------- projects
    "projects": {
        "label": T("Progetti", "Projects"),
        "title": T(
            ["Il metodo,", "messo alla prova."],
            ["The method,", "put to the test."],
        ),
        "toropulse": {
            "title": "ToroPulse",
            "role": T("Lead Architect · dal 2026", "Lead Architect · since 2026"),
            "cta": T("Lista d'attesa", "Join the waitlist"),
            "text": T(
                "Il tuo account eToro, potenziato. ToroPulse è un progetto di ricerca "
                "indipendente che porta alert tecnici composti (RSI, EMA, Volume), "
                "analytics avanzate sul copier e automazione social ai trader retail e "
                "Popular Investors.",
                "Your eToro account, supercharged. ToroPulse is an independent research "
                "project bringing smart compound alerts (RSI, EMA, Volume), deep copier "
                "analytics, and social automation to retail traders and Popular Investors.",
            ),
            "proof": T(
                "Sviluppata in gran parte con agenti AI: io faccio l'architetto e l'orchestratore.",
                "Built largely with AI agents: I act as architect and orchestrator.",
            ),
            "tags": ["Agentic Workflows", "Fintech SaaS", "Trading APIs"],
        },
        "fincast": {
            "title": "AI FinCast",
            "role": T("Creator · dal 2026", "Creator · since 2026"),
            "site": T("Sito", "Website"),
            "text": T(
                "Podcast finanziario quotidiano in italiano, interamente generato dall'AI. "
                "Una pipeline Python autonoma legge le fonti finanziarie durante la notte, "
                "sceglie le notizie che contano, scrive uno script adattivo in 5-7 sezioni, "
                "lo revisiona, sintetizza la voce e pubblica prima dell'apertura dei mercati "
                "europei su Spotify, Apple Podcasts e YouTube.",
                "AI-generated daily financial podcast in Italian. An autonomous Python "
                "pipeline reads the financial sources overnight, selects the news that "
                "matters, writes an adaptive 5-7 section script, edits it, synthesizes the "
                "voice and publishes before European markets open on Spotify, Apple "
                "Podcasts and YouTube.",
            ),
            "proof": T(
                "Oltre 100 episodi, dal lunedì al venerdì, più il riepilogo settimanale del sabato.",
                "100+ episodes, Monday to Friday, plus the Saturday weekly recap.",
            ),
            "tags": ["Python", "Claude API", "Multi-Agent AI", "TTS", "RSS"],
        },
        "tig": {
            "title": T("Strumenti AI in TIG Factory", "AI tooling at TIG Factory"),
            "role": T("CTO · dal 2026", "CTO · since 2026"),
            "text": T(
                "Gli stessi principi dentro un'azienda vera, con colleghi e dati sensibili.",
                "The same principles inside a real company, with colleagues and sensitive data.",
            ),
            "items": [
                {
                    "title": T("Secondo cervello aziendale", "Company second brain"),
                    "text": T(
                        "La conoscenza dell'azienda tenuta da un agente. Ogni fatto ha una "
                        "fonte, un controllo automatico blocca le note fuori standard.",
                        "Company knowledge kept by an agent. Every fact has a source, and "
                        "an automatic check blocks notes that break the standard.",
                    ),
                },
                {
                    "title": T(
                        "Conoscenza di progetto per ogni collega",
                        "Project knowledge for every colleague",
                    ),
                    "text": T(
                        "Ognuno la interroga dal proprio Claude: sola lettura, accesso "
                        "personale, niente esposto su Internet.",
                        "Everyone queries it from their own Claude: read-only, personal "
                        "access, nothing exposed to the Internet.",
                    ),
                },
                {
                    "title": T("Verifiche sul database in secondi", "Database checks in seconds"),
                    "text": T(
                        "Da mezz'ora a mano a pochi secondi, con i dati personali "
                        "mascherati prima che arrivino al modello.",
                        "From half an hour by hand to a few seconds, with personal data "
                        "masked before it reaches the model.",
                    ),
                },
            ],
            "tags": ["Claude Code", "MCP", "Agent Skills", "Quality Gate"],
        },
        "others_label": T("Altri progetti", "Other projects"),
        "others": [
            {
                "type": T("Open Source · Personale", "Open Source · Personal"),
                "title": "AI Meeting Assistant",
                "text": T(
                    "Pipeline AI completamente locale per trascrivere riunioni, identificare "
                    "gli speaker e generare report esecutivi. Funziona su qualsiasi "
                    "piattaforma: Teams, Zoom, Webex. Nessun cloud, nessun abbonamento, "
                    "i dati non escono dalla macchina.",
                    "Fully local AI pipeline for transcribing meetings, identifying speakers, "
                    "and generating executive summaries. Works with any platform: Teams, "
                    "Zoom, Webex. No cloud, no subscriptions, no data leaving your machine.",
                ),
                "tags": ["Python", "FastAPI", "Docker", "Whisper", "Ollama"],
                "link": {
                    "href": LINKS["meeting_repo"],
                    "label": T("Vedi su GitHub", "View on GitHub"),
                },
            },
            {
                "type": T("Prodotto · Cloudia Research", "Product · Cloudia Research"),
                "title": "AI4Teams",
                "text": T(
                    "Un hub basato su AI progettato per migliorare la collaborazione, "
                    "l'allineamento e la produttività dei team nell'ecosistema Microsoft 365.",
                    "An AI-powered hub designed to enhance team collaboration, alignment, "
                    "and productivity within the Microsoft 365 ecosystem.",
                ),
                "tags": ["Microsoft 365", "Azure AI", "Power Platform"],
            },
            {
                "type": T("Prodotto · Cloudia Research", "Product · Cloudia Research"),
                "title": "AI4Orchestration",
                "text": T(
                    "Piattaforma di orchestrazione intelligente su stack Microsoft per "
                    "automazione workflow enterprise e gestione AI-driven dei processi su "
                    "larga scala.",
                    "Intelligent orchestration platform on the Microsoft stack, enabling "
                    "enterprise-grade workflow automation and AI-driven process management "
                    "at scale.",
                ),
                "tags": ["Azure", "Power Automate", "AI Orchestration"],
            },
        ],
    },
    # ------------------------------------------------------------ experience
    "experience": {
        "label": T("Esperienza", "Experience"),
        "title": T(
            ["Diciotto anni di software vero,", "prima degli agenti."],
            ["Eighteen years of real software,", "before the agents."],
        ),
        "now": T("oggi", "today"),
        "items": [
            {
                "from": "2026",
                "to": None,
                "role": "CTO",
                "company": "TIG Factory",
                "text": T(
                    "Guido la strategia tecnologica e la delivery di TIG Factory, business "
                    "unit di TIG (The Innovation Group) dedicata a soluzioni digitali custom "
                    "e software enterprise. Porto gli agenti AI dentro il modo in cui il "
                    "team progetta, scrive e verifica il software.",
                    "I lead technology strategy and delivery at TIG Factory, the business "
                    "unit of TIG (The Innovation Group) focused on custom digital solutions "
                    "and enterprise software. I bring AI agents into how the team designs, "
                    "writes and verifies software.",
                ),
                "tags": ["Technology Strategy", "AI in Engineering", ".NET", "Azure"],
            },
            {
                "from": "2024",
                "to": "2026",
                "role": "Innovation Director",
                "company": "Cloudia Research",
                "text": T(
                    "Direzione del Microsoft Hub (18+ consulenti) e supervisione "
                    "dell'esecuzione progetti su Azure, Custom Dev e Power Platform. Guida "
                    "dell'R&D per prodotti SaaS interni e ruolo di Solution Architect per "
                    "clienti enterprise.",
                    "Directed the Microsoft Hub (18+ consultants), overseeing project "
                    "execution across Azure, Custom Dev, and Power Platform. Led product "
                    "R&D for internal SaaS solutions and acted as Solution Architect for "
                    "enterprise clients.",
                ),
                "tags": ["Team Leadership", "Solution Architecture", "Product R&D", "Pre-sales"],
            },
            {
                "from": "2018",
                "to": "2024",
                "role": T("Solution Architect · Team Leader", "Solution Architect · Team Leader"),
                "company": "Cloudia Research",
                "text": T(
                    "Progettazione e implementazione di architetture cloud-first su .NET "
                    "Core e Azure. Modernizzazione applicativa, automazione workflow e "
                    "reportistica data-driven per clienti enterprise. Dal 2023 coordinamento "
                    "dello sviluppo .NET e delle integrazioni tra CRM, ERP e PLM.",
                    "Designed and implemented cloud-first architectures on .NET Core and "
                    "Azure. Application modernization, workflow automation, and data-driven "
                    "reporting for enterprise clients. From 2023, coordinated .NET "
                    "development and the integrations between CRM, ERP and PLM systems.",
                ),
                "tags": [".NET Core", "Azure", "Cloud Architecture", "DevOps"],
            },
            {
                "from": "2013",
                "to": "2017",
                "role": "Integration Specialist",
                "company": "Nexive",
                "text": T(
                    "Progettato QArc, middleware SOA custom per l'integrazione di Oracle, "
                    "DB2 e Salesforce ERP. Partecipazione al progetto Nexibus, un "
                    "Enterprise Service Bus su TIBCO.",
                    "Architected QArc, a custom SOA middleware layer integrating Oracle, "
                    "DB2, and Salesforce ERP across enterprise environments. Contributed to "
                    "Nexibus, an Enterprise Service Bus built on TIBCO.",
                ),
                "tags": ["SOA Middleware", "TIBCO", "System Integration", "C#"],
            },
            {
                "from": "2011",
                "to": "2013",
                "role": T("Consulente .NET · Senior Developer", ".NET Consultant · Senior Developer"),
                "company": "WICE Group",
                "text": T(
                    "In consulenza presso PwC (data access layer su SAP, Active Directory e "
                    "FIM, portale di onboarding su SharePoint), Medtronic Italia "
                    "(applicazioni interne, architettura multilayer, formazione del team "
                    "IT), Reply per Eurizon (servizi per operazioni in tempo reale su "
                    "polizze) e Magneti Marelli (portale procure su SharePoint).",
                    "Consulting at PwC (data access layer over SAP, Active Directory and "
                    "FIM, onboarding portal on SharePoint), Medtronic Italia (internal "
                    "applications, multilayer architecture, training the IT team), Reply "
                    "for Eurizon (services for real-time operations on insurance policies) "
                    "and Magneti Marelli (power-of-attorney portal on SharePoint).",
                ),
                "tags": ["PwC", "Medtronic Italia", "Reply · Eurizon", "Magneti Marelli"],
            },
            {
                "from": "2008",
                "to": "2011",
                "role": "Senior .NET Developer · Oracle DWH Developer",
                "company": "Monte dei Paschi di Siena",
                "text": T(
                    "Responsabile di pipeline ETL e gestione metadati per il data warehouse "
                    "finanziario su Oracle Warehouse Builder. Reportistica web e servizi "
                    "bancari nelle divisioni Anagrafe e Finanza.",
                    "Owned ETL pipelines and metadata management for the financial data "
                    "warehouse using Oracle Warehouse Builder. Delivered web reporting and "
                    "banking services across Anagrafe and Finance divisions.",
                ),
                "tags": ["Oracle OWB", "ETL / PL-SQL", "Reporting Services", "C# / ASP.NET"],
            },
        ],
    },
    # --------------------------------------------------------------- writing
    "writing": {
        "label": T("Articoli", "Writing"),
        "title": T(
            ["Guide e appunti", "dal lavoro."],
            ["Guides and notes", "from the work."],
        ),
        "guides_label": T("Guide, ospitate qui", "Guides, hosted here"),
        "posts_label": T("Da LinkedIn", "From LinkedIn"),
        "read": T("Leggi", "Read"),
    },
    # --------------------------------------------------------------- contact
    "contact": {
        "label": T("Contatti", "Contact"),
        "title": T(
            ["Costruiamo", "qualcosa insieme."],
            ["Let's build", "something together."],
        ),
        "text": T(
            "Se vuoi portare gli agenti AI dentro il modo in cui il tuo team costruisce "
            "software, o hai un progetto da far arrivare in produzione, scrivimi. Rispondo io.",
            "If you want to bring AI agents into how your team builds software, or you "
            "have a project that needs to reach production, write to me. I answer personally.",
        ),
    },
    # ---------------------------------------------------------------- footer
    "footer": {
        "text": T("Milano, Italia · CTO & AI Innovator", "Milan, Italy · CTO & AI Innovator"),
        "privacy": T("Privacy", "Privacy"),
    },
}
