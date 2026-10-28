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
| `mkv-c3-bellman-1d.svg` | Ecuación de Bellman en la casilla 2 como gráfica de una variable, x = V(2) | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-cuatro-cadenas.svg` | Las cuatro políticas del pasillo, cada una dibujada como su cadena | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-cuatro-politicas-plano.svg` | Las cuatro políticas del pasillo como puntos (V(1), V(2)) | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-ej-bellman.svg` | Ejemplo y contraejemplo de Bellman en una variable: un solo cruce en −2; con esperar gratis, pegada a y = x e infinitas soluciones | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-ej-codiciosa.svg` | La codiciosa de V* da caminar–correr; la de una estimación equivocada U = (−8, −8) da caminar–caminar | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-ej-empates.svg` | Conservar la acción en un empate termina; cambiarla hace alternar para siempre entre dos políticas del mismo valor | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-ej-evaluar.svg` | Caminar–correr tiene I − P invertible y valor (−5, −2); esperar siempre gratis deja I − P singular | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-ej-hacia-atras.svg` | La escalera sin ciclos se resuelve con una pasada; con un resbalón en el escalón 3, costo(3) depende de sí mismo | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-ej-lineal.svg` | El mínimo del programa lineal es V* = (−5, −2); con esperar gratis la región no cambia y el mínimo ya no es V* = (0, 0) | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-ej-mdp.svg` | Las matrices de caminar y correr con filas que suman 1, contra una fila de correr que suma 3/2 | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-ej-paro.svg` | En el pasillo el error es igual al residuo; en el lazo de 99/100 es 99 veces el residuo | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-ej-punto-fijo.svg` | f(x) = −1 + x/2 cruza y = x una vez y la iteración se acerca; con f(x) = x todo número es punto fijo | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-ej-termina.svg` | Caminar–correr llega a la meta con probabilidad 1; esperar siempre nunca llega | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-escalera-arbol-vs-grafo.svg` | Arriba, el árbol de llamadas de rutas(0) | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-escalera.svg` | Escalera de escalones 0 a 5 que suben a la derecha; desde cada escalón se brinca 1 o 2 sin pasarse del 5. Pisar los escalones 1 a 5 cuesta 1, 2, 9, 1, 1 (el 3 está flojo) | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-flujo-evaluar.svg` | Diagrama de flujo de evaluar una política, en palabras | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-flujo-hacia-atras.svg` | Diagrama de flujo de la pasada hacia atrás, en palabras | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-flujo-politicas.svg` | Diagrama de flujo de la iteración de políticas, en palabras | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-flujo-valores.svg` | Diagrama de flujo de la iteración de valores, en palabras | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-fronteras.svg` | Mapa de la mejor política del pasillo según el costo de caminar (de 0 a 6) y el castigo del hueco (de 0 a 12) | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-iterar-valores.svg` | Iteración de valores en el pasillo desde V⁽⁰⁾ = 0, rondas 0 a 8: V(1) y V(2) contra la ronda | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-mapa-decidir.svg` | Mapa de la clase: pregunta, ecuación y algoritmo, en tres filas | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-pasillo-largo.svg` | El pasillo de 200 casillas: la acción óptima en cada casilla y su valor óptimo | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-pasillo-mdp.svg` | El MDP del pasillo como grafo con nodos de acción, y debajo las matrices de caminar y de correr | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-pasillo.svg` | El pasillo mojado: inicio, la casilla 1 con hueco sin barandal, la casilla 2 con barandal y la meta | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-politica-elige-filas.svg` | La política caminar–correr elige la fila 1 de P caminar (0, 1, 0) y la fila 2 de P correr (0, 1/2, 1/2), marcadas; juntas forman Pπ, la matriz de la política | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-punto-fijo.svg` | Gráfica de y = f(x) = −1 + x/2 y de y = x, con x de −4 a 1. Se cruzan una vez, en x = −2 | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-region-lp.svg` | Plano V(1)–V(2) con las cuatro restricciones del programa lineal del pasillo, una recta por par (estado, acción) | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-residuo.svg` | Escala logarítmica, rondas 1 a 10 de la iteración de valores en el pasillo | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-rondas-politicas.svg` | Iteración de políticas en el pasillo de dos casillas | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c3-simular-politica.svg` | Histograma del retorno de 10 000 episodios de caminar–correr desde la casilla 1 (semilla 2044) | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-hmm-grafo.svg` | El paraguas como modelo oculto: estados ocultos (lluvia, sol) arriba con borde punteado y sus transiciones, señales que se ven abajo con borde sólido y las emisiones, con μ₀ | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-ej-modelo.svg` | Ejemplo y contraejemplo de «un modelo oculto»: el paraguas con B cuyas filas suman 1, y la misma B copiada por columnas, con filas que suman 11/10 y 9/10 | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-ej-creencia.svg` | Ejemplo y contraejemplo de «una creencia»: barras de la creencia del día 0 tras ver paraguas (lluvia 9/11, sol 2/11, suman 1) y, abajo, el clima real oculto del día 6 de la semana simulada con la creencia en gris (≈ 0.194 y ≈ 0.806) | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-ej-filtrar.svg` | Ejemplo y contraejemplo del filtrado recursivo: barras de la creencia con las flechas predecir y corregir (paraguas, paraguas: 9/11, 69/110, 621/703) y el clima fijo con P y B identidad, donde la última barra se tacha por señal imposible | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-flujo-filtrar.svg` | Diagrama de flujo de FILTRAR, en palabras: corregir, sumar los pesos, parar si la evidencia es 0, normalizar, y predecir con P mientras queden días | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-filtrar-traza.svg` | Creencia de lluvia por día (0 a 2) con las señales paraguas, paraguas, sin paraguas: punto hueco con la predicción y punto lleno con la creencia, con la línea punteada en 1/2 | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-flujo-viterbi.svg` | Diagrama de flujo de VITERBI, en palabras: máximo y apuntadores por día, y regreso por los apuntadores | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-trellis-1.svg` | Retícula de Viterbi para sin paraguas, paraguas, sin paraguas, tramo 1: solo el día 0 lleno (lluvia 1/20, sol 2/5) | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-trellis-2.svg` | La misma retícula, tramo 2: el día 1 nuevo (lluvia 27/250, sol 7/125) con las flechas de dónde viene el máximo | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-trellis-3.svg` | La misma retícula, tramo 3: el día 2 (lluvia 189/25000, sol 98/3125) y el camino de regreso sol, sol, sol, con conjunta 98/3125 | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-ej-decodificar.svg` | Ejemplo y contraejemplo de Viterbi: la retícula con conjunta 98/3125 y la misma retícula con B de 2×3 y la señal nieve, donde las columnas valen 0 y no hay ruta | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-ej-aprender.svg` | Ejemplo y contraejemplo de aprender lo oculto: la tira de siete días anotados con su P gorro estimada, y la de los días 2 a 6, cuya fila de sol queda sin estimar | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-flujo-aprender.svg` | Diagrama de flujo del ciclo de Baum-Welch, en palabras: repartir, contar con fracciones, modelo nuevo y repetir hasta que la verosimilitud deje de subir | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-lenguaje-grafo.svg` | El modelo de lenguaje pequeño como modelo oculto: tres estados gramaticales con sus transiciones, los cuatro ceros marcados, las palabras de cada estado con su probabilidad y μ₀ | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-ds-costos.svg` | Costo esperado del día según la creencia b para llevar, no llevar, mirar y ver gratis, con la envolvente inferior y las tres regiones donde gana cada acción | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-ej-decidir.svg` | Ejemplo y contraejemplo de pagar por mirar: dos árboles de decisión con b = 1/3 y precio 1/2 (total 5/6 contra 1; con la ventana con niebla, 16/15) | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
| `mkv-c4-mapa-2x2.svg` | El mapa de dos ejes (estado visible u oculto, modelo conocido o desconocido) con lo visto relleno y lo que falta punteado | Generado con `tools/gen_markov.py` | Propio, CC BY-SA 4.0 |
