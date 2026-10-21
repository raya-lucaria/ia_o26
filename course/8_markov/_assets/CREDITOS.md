# Créditos de las imágenes — Cadenas de Markov

Los diagramas SVG de esta unidad los produce `tools/gen_markov.py`. No se
editan a mano: se cambia la función del generador y se vuelve a correr. Toda
cifra de una figura sale de `tools/markov.py`, que la calcula sobre la frase
«Con la iglesia hemos dado, Sancho» o sobre el corte del *Quijote* versionado
en `tools/datos/quijote/` (dominio público; ver su `README.md`).

La vista previa `mkv-c1-generador.png` no se dibuja: es una captura del
interactivo `generador_texto.html` (que escribe `tools/gen_generador_markov.py`),
tomada con Chrome sin interfaz por `tools/gen_vista_generador.py`.
`tools/test_generador_markov.py` falla si el interactivo cambió desde la última
captura; entonces se vuelve a tomar.

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|
| `mkv-c1-flujo-muestrear.svg` | Muestrear una fila, en palabras: sortear u, recorrer la fila sumando y quedarse con el primer estado cuya suma pasa a u | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c1-flujo-contar.svg` | Contar, en palabras: tomar cada par (actual, siguiente), sumar 1 a su conteo y al final dividir cada fila entre su total | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c1-flujo-predecir.svg` | Predecir, en palabras: empezar con μ₀ y multiplicar por la matriz hasta llegar al paso t | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c1-flujo-generar.svg` | Generar, en palabras: tomar el contexto, muestrear su fila (suavizada si nunca se vio), escribir el símbolo y deslizar el contexto | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c1-grafo-vc.svg` | El grafo vocal–consonante de la frase con sus cuatro probabilidades estimadas | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c1-arbol-2-pasos.svg` | El árbol de dos pasos desde C con la matriz de la frase y la probabilidad de cada camino | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c1-mu-t.svg` | La probabilidad de vocal en cada paso, desde V y desde C: la cuenta y la simulación, con la matriz del corpus | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c1-recuperar-p.svg` | El error de la matriz estimada contra la longitud de la trayectoria, en réplicas de una matriz conocida | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c1-ceros.svg` | La fracción de transiciones de prueba nunca vistas al contar, por memoria 0 a 3 | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c1-rachas.svg` | Las rachas de consonantes del corpus contra lo que dan, simuladas, una cadena y letras independientes | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-grafo-clasificar.svg` | Una cadena de cinco estados clasificada: una clase transitoria abierta, una cerrada de periodo 2 y una cerrada aperiódica, marcadas por el borde y por rótulo | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-grafo-contraejemplos.svg` | Tres cadenas pequeñas apiladas: la alternante (periodo 2), la identidad (dos clases cerradas) y un transitorio entre dos clases cerradas | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-mu-t-inicios.svg` | La probabilidad del primer estado paso a paso: la cadena de la frase desde V y desde C se junta en su estacionaria; la alternante desde A oscila | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-flujo-potencias.svg` | La iteración de potencias, en palabras: multiplicar por P hasta que la distancia entre dos pasos baje de la tolerancia o se llegue al tope | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-tablero-chico.svg` | Un tablero de serpientes y escaleras de seis casillas con moneda, y el grafo de sus estados al final del turno con el tiempo medio que falta | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-flujo-absorcion.svg` | El tiempo medio de llegada, en palabras: quitar la meta de P, armar el sistema (I − P𝒯) m = 1 y resolverlo | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-web-juguete.svg` | Una web de cuatro páginas con una página sin salidas y su PageRank con α = 0.85 | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-ej-comunican.svg` | Ejemplo y contraejemplo de «estados que se comunican»: una cadena que lo cumple y otra que no, cada una con su grafo y su matriz | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-ej-clases.svg` | Ejemplo y contraejemplo de «comunicar parte en clases»: una cadena que lo cumple y otra que no, cada una con su grafo y su matriz | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-ej-cerrada.svg` | Ejemplo y contraejemplo de «clase cerrada»: una cadena que lo cumple y otra que no, cada una con su grafo y su matriz | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-ej-hay-cerrada.svg` | Ejemplo y contraejemplo de «finita, hay una cerrada»: una cadena que lo cumple y otra que no, cada una con su grafo y su matriz | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-ej-transitorio.svg` | Ejemplo y contraejemplo de «recurrente y transitorio»: una cadena que lo cumple y otra que no, cada una con su grafo y su matriz | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-ej-recurrente-cerrada.svg` | Ejemplo y contraejemplo de «recurrente equivale a cerrada»: una cadena que lo cumple y otra que no, cada una con su grafo y su matriz | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-ej-periodo.svg` | Ejemplo y contraejemplo de «periodo»: una cadena que lo cumple y otra que no, cada una con su grafo y su matriz | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-ej-periodo-clase.svg` | Ejemplo y contraejemplo de «un lazo vuelve el periodo 1»: una cadena que lo cumple y otra que no, cada una con su grafo y su matriz | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-ej-estacionaria.svg` | Ejemplo y contraejemplo de «distribución estacionaria»: una cadena que lo cumple y otra que no, cada una con su grafo y su matriz | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-ej-limite.svg` | Ejemplo y contraejemplo de «el límite es estacionario»: una cadena que lo cumple y otra que no, cada una con su grafo y su matriz | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-ej-existe.svg` | Ejemplo y contraejemplo de «existe una estacionaria»: una cadena que lo cumple y otra que no, cada una con su grafo y su matriz | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-ej-unica.svg` | Ejemplo y contraejemplo de «una sola clase cerrada»: una cadena que lo cumple y otra que no, cada una con su grafo y su matriz | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-ej-converge.svg` | Ejemplo y contraejemplo de «convergencia desde todo inicio»: una cadena que lo cumple y otra que no, cada una con su grafo y su matriz | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c2-ej-ergodico.svg` | Ejemplo y contraejemplo de «teorema ergódico»: una cadena que lo cumple y otra que no, cada una con su grafo y su matriz | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c1-generador.png` | Vista previa del generador de texto con memoria 2, semilla 2034, en el símbolo 150 de 200: contexto «ce», sale «s» con u = 0.7149 | Capturado de `generador_texto.html` con `tools/gen_vista_generador.py` | Propio, CC BY-SA 4.0 |
