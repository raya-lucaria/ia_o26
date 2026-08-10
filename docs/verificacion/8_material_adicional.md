# Verificación — Material adicional

Todos los enlaces se comprobaron con:

```bash
cd /home/uumami/itam/ia_o26 && while read -r url; do
  printf "%s  " "$url"
  curl -sS -o /dev/null -w "%{http_code}\n" --max-time 25 -L "$url" || echo FALLO
done <<'EOF'
[...]
EOF
```

Para las dos rutas de mayor riesgo (Rosenblatt 1958, cuyo host original es de pago; y los tres PDF
de universidades espejo) se verificó además, con `curl -o archivo && file archivo`, que la respuesta
200 correspondiera a un PDF real y no a una página de error servida con código 200.

| URL | Qué es | Código HTTP | Nota |
|---|---|---|---|
| https://courses.cs.umbc.edu/471/papers/turing.pdf | Turing, "Computing Machinery and Intelligence", *Mind*, 1950 — texto completo | 200 | PDF verificado, 22 páginas |
| http://jmc.stanford.edu/articles/dartmouth/dartmouth.pdf | McCarthy, Minsky, Rochester y Shannon, "A Proposal for the Dartmouth Summer Research Project on Artificial Intelligence", 1955 — texto completo, alojado por John McCarthy en Stanford | 200 | PDF verificado, 13 páginas |
| https://pdfs.semanticscholar.org/865f/b2cfe6fdb7af2c663ef346ea05889f237108.pdf | Rosenblatt, "The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain", *Psychological Review*, 1958 — texto completo | 200 | PDF verificado, 38 páginas. El artículo original de la APA (`psycnet.apa.org`, DOI 10.1037/h0042519) devuelve 403 y no tiene ubicación de acceso abierto según Unpaywall; este es el espejo estable que Semantic Scholar sirve como copia de acceso abierto |
| https://cse.buffalo.edu/~rapaport/572/S02/weizenbaum.eliza.1966.pdf | Weizenbaum, "ELIZA—A Computer Program For the Study of Natural Language Communication Between Man And Machine", *Communications of the ACM*, 1966 — texto completo | 200 | PDF verificado |
| https://arxiv.org/abs/1706.03762 | Vaswani et al., "Attention Is All You Need", 2017 — texto completo | 200 | arXiv, fuente estable por definición |
| https://www.ted.com/talks/oliver_brock_the_science_of_intelligence_and_a_bold_new_principle | Charla TED de Oliver Brock sobre qué es la inteligencia | 200 | Bloque «inteligencia» |
| https://www.ted.com/talks/anil_seth_why_ai_isn_t_going_to_become_conscious | Charla TED de Anil Seth, "Why AI isn't going to become conscious" | 200 | Bloque «conciencia» |
| https://www.youtube.com/watch?v=16W7c0mb-rE | Kurzgesagt, "Emergence – How Stupid Things Become Smart Together" | 200 | Bloque «comportamiento emergente» |
| https://www.youtube.com/watch?v=cQ48rP_Rs4g | Lex Fridman Podcast #27, conversación con Kai-Fu Lee, "AI Superpowers: China and Silicon Valley" | 200 | Reemplaza al material original con una conversación completa, verificable y con el mismo protagonista |
| https://www.youtube.com/watch?v=d95J8yzvjbQ | "The Thinking Game", documental de 2025 sobre Google DeepMind y Demis Hassabis, publicado gratis en YouTube por Google DeepMind | 200 | Sustituye al documental del material original (no identificado con certeza en la fuente) por uno vigente, gratuito y de la propia industria |
| https://www.openresearchlab.org/findings | OpenResearch, resultados del mayor estudio de renta básica incondicional en Estados Unidos (financiado por Sam Altman) | 200 | Sustituye la referencia genérica a "renta básica" del material original por la fuente primaria de datos, ligada directamente a la industria de IA |
| https://epoch.ai/trends | Epoch AI, tendencias de cómputo, modelos y hardware de IA | 200 | Dato vivo — se actualiza solo |
| https://ourworldindata.org/artificial-intelligence | Our World in Data, página temática sobre inteligencia artificial | 200 | Dato vivo — se actualiza solo |

## Enlaces descartados

- **Rosenblatt 1958 en su fuente editorial original** (`psycnet.apa.org/doi/10.1037/h0042519`): devuelve 403 (muro de pago de la APA). Se consultó Unpaywall con el DOI y no reporta ninguna ubicación de acceso abierto (`is_oa: false`, `oa_locations: []`). Se buscaron alternativas institucionales (Cornell, DTIC, CiteSeerX, archive.org) sin éxito: el reporte técnico previo de 1957 de Cornell Aeronautical Laboratory es una obra distinta y no está digitalizado en abierto. Se optó por el espejo de Semantic Scholar (`pdfs.semanticscholar.org`), que sirve una copia de acceso abierto indexada por su propio motor de agregación académica — es la opción más estable y legítima disponible, no una biblioteca en la sombra.
- **AlphaGo (2017), documental de DeepMind**: se consideró como candidato a "documental", pero se prefirió "The Thinking Game" (2025) por ser más reciente, seguir vigente en agosto de 2026, y estar publicado directamente por Google DeepMind como estreno gratuito reciente en su propio canal.
- No se descartó ningún enlace por devolver un código distinto de 200 tras la sustitución: todos los que aparecen en la tabla final ya pasaron la verificación.
