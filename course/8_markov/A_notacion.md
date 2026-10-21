---
id: notacion-markov
title: Toda la notación, en una hoja
nav_title: Notación
summary: "Cada símbolo y cada término que usa la unidad de cadenas de Markov, cómo se lee, qué significa y en qué página se presentó."
status: ready
estimated_time: 7m
tags: [markov, referencia, notacion]
---

# Toda la notación, en una hoja

Todos los símbolos están definidos en su página. Si encuentras uno a media
lectura y no recuerdas qué era, búscalo aquí en vez de retroceder.

**Cómo leer la flecha:** al final de cada renglón, *→ página* dice dónde se
**presentó** el símbolo. Si algo te resulta opaco, vuelve a esa página.

**Dos convenciones valen en toda la unidad.** En los estados, mayúscula para lo que todavía
es azar ($S_t$) y minúscula para un valor concreto ($s$). Lo exacto va sin
gorro; la estimación por frecuencias lleva gorro, como $\widehat P$, y la suavizada, tilde, como $\widetilde p$.

## Probabilidad

| Símbolo | Cómo se lee, qué es y dónde se presenta |
|---|---|
| $\Pr(A)$ | «probabilidad de a». Qué tan probable es el evento $A$, entre 0 y 1. *→ Lo que necesitas de probabilidad* |
| $\widehat{\Pr}(A)$ | «probabilidad estimada de a». La frecuencia con que $A$ ocurrió en los datos. *→ Lo que necesitas de probabilidad* |
| $A\cap B$ | «a y be». El evento de que ocurran los dos. *→ Lo que necesitas de probabilidad* |
| ${\Pr(A\mid B)}$ | «probabilidad de a dado be». La probabilidad de $A$ si ya sabes que ocurrió $B$: ${\Pr(A\cap B)/\Pr(B)}$, definida solo si ${\Pr(B)>0}$. *→ Lo que necesitas de probabilidad* |
| $\prod$, $\sum$ | «producto», «suma». Multiplicar o sumar todos los términos que indica el índice de abajo a arriba. *→ Lo que necesitas de probabilidad* |
| ${\Pr(S_0=a, S_1=b)}$ | La coma se lee «y»: que ocurran las dos cosas. *→ Lo que necesitas de probabilidad* |
| $n$ | «ene». El número de repeticiones independientes; desde Ajustar contando, el número de réplicas de una simulación. *→ Lo que necesitas de probabilidad* |

## La cadena

| Símbolo | Cómo se lee, qué es y dónde se presenta |
|---|---|
| $t$ | «te». El paso: ${t=0,1,2,\dots}$ Los libros de cadenas usan $n$; aquí $t$, como en agentes. *→ Lo que necesitas de probabilidad* |
| $S_t$ | «ese sub te». El estado en el paso $t$, **todavía aleatorio**. *→ Lo que necesitas de probabilidad* |
| $s$, $s'$ | «ese», «ese prima». Valores concretos de un estado: de dónde sales y a dónde llegas. *→ El problema de Markov* |
| $s_1,\dots,s_k$ | «ese uno a ese ka». Los estados enumerados; sus índices identifican filas y columnas, no pasos de una trayectoria. *→ La cadena de Markov, en general* |
| $P_{ij}$, $p_{ij}$ | «pe i jota». La entrada de la fila $i$ y columna $j$: $P_{ij}=P(s_j\mid s_i)$. En el ejemplo simbólico se escribe $p_{ij}=P_{ij}$. *→ La cadena de Markov, en general* |
| $\mathbf e_i$ | «e i». El vector fila $1\times k$ con 1 en la posición $i$ y 0 en las demás: empezar seguro en $s_i$. *→ La cadena de Markov, en general* |
| $\mathbf 1$ | «uno». El vector columna $k\times 1$ de unos: $P\mathbf 1=\mathbf 1$ dice que cada fila suma 1. *→ La cadena de Markov, en general* |
| $I_k$ | «identidad de tamaño ka». La matriz $k\times k$ con unos en la diagonal y ceros fuera: $P^0=I_k$. *→ La cadena de Markov, en general* |
| $\mathbf 1^{\mathsf T}$ | «uno traspuesto». El vector fila $1\times k$ de unos; suma las entradas de una columna. *→ La cadena de Markov, en general* |
| $H_t$ | «hache sub te». Una historia: el evento $\{S_0=s_{i_0},\dots,S_t=s_{i_t}\}$. *→ La cadena de Markov, en general* |
| $(P^t)_{ij}$ | «entrada i jota de pe a la te». Probabilidad de llegar a $s_j$ en exactamente $t$ pasos al empezar en $s_i$. Equivale a ${\Pr(S_t=s_j\mid S_0=s_i)}$ cuando ${\Pr(S_0=s_i)>0}$. *→ La cadena de Markov, en general* |
| $\mathcal S$ | «ese caligráfica». El conjunto de estados posibles. *→ La cadena de Markov, en general* |
| $k$ | «ka». Número de valores posibles; en una cadena, $k=\lvert\mathcal S\rvert$. *→ Lo que necesitas de probabilidad* |
| V, C | «ve», «ce». Vocal y consonante, en ese orden. *→ Lo que necesitas de probabilidad* |
| $P$ | «pe». La matriz de transición, $k\times k$: fila = desde, columna = hacia; cada fila suma 1. No es la clase P de complejidad. *→ La cadena de Markov, en general* |
| $P(s'\mid s)$, $P_{ss'}$ | «pe de ese prima dado ese». Si $s=s_i$ y $s'=s_j$, es $P_{ij}$; con estados con nombre, $P_{CC}=P(C\mid C)$. Si $\Pr(S_t=s)>0$, coincide con $\Pr(S_{t+1}=s'\mid S_t=s)$. *→ La cadena de Markov, en general* |
| $\mu_0$ | «mu cero». La distribución del estado inicial, un vector fila que suma 1. No es el $\mu$ de KKT. *→ La cadena de Markov, en general* |
| $\mu_t$ | «mu sub te». La distribución del estado en el paso $t$: ${\mu_t(s)=\Pr(S_t=s)}$. *→ La cadena de Markov, en general* |
| $P^t$, ${\widehat P^{\,t}}$ | «pe a la te». La matriz multiplicada por sí misma $t$ veces: ${\mu_t=\mu_0P^t}$. *→ La cadena de Markov, en general* |
| $j$ | «jota». Índice de un producto o una suma: ${\prod_{j=0}^{t-1}}$. *→ Lo que necesitas de probabilidad* |
| ${p_1,\dots,p_k}$ | «pe uno a pe ka». Las entradas de una fila, en el orden de los estados, como las recibe MUESTREAR-FILA. *→ El problema de Markov* |
| $P^{\mathsf T}$ | «pe traspuesta». La matriz con filas y columnas intercambiadas; algunos libros escriben las distribuciones como columnas y usan $P^{\mathsf T}$. Aquí no. *→ La cadena de Markov, en general* |
| $u$, $\Delta_i$ | «u», «delta i». Un número al azar en ${[0,1)}$, ${u\sim\operatorname{Unif}[0,1)}$, con que MUESTREAR-FILA elige el siguiente estado: sale $s_i$ si $u$ cae en el intervalo $\Delta_i$, de largo $p_i$. *→ El problema de Markov* |
| $L$ | «ele». La longitud de una racha de consonantes, todavía aleatoria; $\ell$ es un valor: ${\Pr(L=\ell)}$. *→ El problema de Markov* |
| $\ell$, $q$ | «ele», «cu». La longitud de una racha de consonantes y la probabilidad de seguir en consonante. *→ El problema de Markov* |
| $T$ | «te mayúscula». Número de transiciones observadas al ajustar. En GENERAR cuenta símbolos nuevos: el texto devuelto mide $h+T$, incluido el contexto inicial. *→ Ajustar contando; Generar texto* |

## Ajustar desde datos

| Símbolo | Cómo se lee, qué es y dónde se presenta |
|---|---|
| ${N(s,s')}$ | «ene de ese, ese prima». Cuántas veces, en los datos, a $s$ le sigue $s'$. *→ Ajustar contando* |
| $N(s)$ | «ene de ese». Las salidas observadas de $s$: ${\sum_{s'}N(s,s')}$. La última letra no cuenta: no tiene sucesor. *→ Ajustar contando* |
| $\widehat P$ | «pe gorro». La matriz estimada: si $N(s)>0$, $\widehat P(s'\mid s)=N(s,s')/N(s)$. Sin salidas, los datos no determinan la fila. *→ El problema de Markov; justificación en Ajustar contando* |
| $\mathcal L(P)$ | «ele caligráfica de pe». La verosimilitud de los datos observados como función de $P$, condicionada al primer estado. *→ Ajustar contando* |
| $\Sigma$ | «sigma mayúscula». Alfabeto de símbolos; con las 27 letras y el espacio, $\lvert\Sigma\rvert=28$. Con memoria $h$, los estados son contextos de $\Sigma^h$. *→ Ajustar contando* |
| $z$, $z_t$, $z_j$ | «zeta». Valor concreto de un símbolo. Al ajustar, $t$ recorre el texto observado; en GENERAR, $j$ cuenta los símbolos nuevos. *→ Ajustar contando* |
| $Z_j$ | «zeta mayúscula sub jota». El símbolo número $j$ de la continuación, todavía aleatorio; $z_j$ es su valor. *→ Generar texto* |
| $p$ | «pe». Una probabilidad escalar, cuyo evento se declara al usarla; no es una matriz. *→ Ajustar contando* |
| $p(z\mid c)$, $\widehat p(z\mid c)$ | Probabilidad del símbolo $z$ desde el contexto $c$; el gorro indica la frecuencia estimada. La tabla por símbolos tiene forma ${\lvert\Sigma\rvert^h\times\lvert\Sigma\rvert}$; $P$ sigue siendo la matriz cuadrada entre estados. *→ Generar texto* |
| $\delta$ | «delta». Error al recuperar una matriz: $\delta=\max_{i,j}\lvert\widehat P_{ij}-P_{ij}\rvert$. *→ Ajustar contando* |
| $\varepsilon$ | «épsilon». Una cantidad positiva para construir un contraejemplo. *→ La cadena de Markov, en general* |
| $\widetilde p$ | «pe tilde». Estimación de Laplace: ${\widetilde p(z\mid s)}={[N(s,z)+1]}/{[N(s)+\lvert\Sigma\rvert]}$. *→ Ajustar contando* |
| $c_t$, $c_j$ | «ce sub te», «ce sub jota». Contexto de $h$ símbolos: termina en la posición $t$ al contar; en GENERAR, queda tras escribir $j$ símbolos nuevos desde $c_0$. *→ Ajustar contando; Generar texto* |
| $\operatorname{suf}_h(w)$ | Últimos $h$ símbolos de $w$; con $h=0$, contexto vacío. *→ Generar texto* |
| memoria $h$ | «memoria hache». Cuántos símbolos anteriores forman el estado. Memoria 0, 1, 2 = unigrama, bigrama, trigrama. No es la profundidad de UCT. *→ Ajustar contando* |

## A la larga

| Símbolo | Cómo se lee, qué es y dónde se presenta |
|---|---|
| $\lVert x-y\rVert_1$ | «norma uno de equis menos ye». La distancia entre dos distribuciones: ${\sum_i\lvert x_i-y_i\rvert}$. *→ Lo que necesitas de álgebra y límites.* |
| $\mathrm{tol}$ | «tolerancia». El umbral para dejar de iterar: se para cuando la distancia entre dos iteraciones queda por debajo. *→ Lo que necesitas de álgebra y límites.* |
| $E_s[X]$, $\Pr_s(\cdot)$ | «esperanza de equis empezando en ese». Valor esperado y probabilidad de la cadena que arranca en $s$. *→ Lo que necesitas de álgebra y límites.* |
| $s\to s'$, $s\leftrightarrow s'$ | «ese alcanza a ese prima», «se comunican». Hay un camino de flechas positivas de $s$ a $s'$; y, en el segundo caso, también de regreso. *→ Clasificar los estados.* |
| $d(s)$ | «de de ese». El periodo de $s$: el máximo común divisor de los pasos $t\ge1$ en que se puede regresar a $s$. Aperiódico si ${d(s)=1}$. *→ Clasificar los estados.* |
| $\mu$ | «mu», sin índice. La distribución estacionaria: ${\mu P=\mu}$, con entradas $\ge0$ que suman 1. *→ La estacionaria y sus cuatro teoremas.* |
| $N_T(s)$ | «ene sub te mayúscula de ese». Cuántas veces visita la cadena el estado $s$ en los pasos ${0,\dots,T-1}$; la fracción del tiempo es ${N_T(s)/T}$. *→ La estacionaria y sus cuatro teoremas.* |
| $A$, $\tau_A$ | «a», «tau sub a». El conjunto de estados a los que se quiere llegar, y el primer paso en que la cadena está en él: ${\tau_A=\min\{t\ge0: S_t\in A\}}$. *→ Cuánto falta para terminar.* |
| $m(s)$, $P_{\mathcal T}$ | «eme de ese», «pe sub te caligráfica». El tiempo medio de llegada desde $s$, ${m(s)=E_s[\tau_A]}$, y la matriz $P$ restringida a los estados fuera de $A$. *→ Cuánto falta para terminar.* |
| $\operatorname{salidas}(s)$ | «salidas de ese». En una red de páginas, cuántos enlaces salen de la página $s$; una fila sin salidas es la de una página que no enlaza a nada. *→ PageRank.* |
| $\alpha$, $v$ | «alfa», «ve». En PageRank, la probabilidad de seguir un enlace y el vector de salto. *→ PageRank.* |
| $\overline P$, $G$ | «pe barra», «ge». $P$ con cada fila sin salidas sustituida por $v$, y la matriz de Google ${G=\alpha\overline P+(1-\alpha)\mathbf 1v}$. *→ PageRank.* |

## Términos

| Término | Qué significa aquí y dónde se presenta |
|---|---|
| Experimento | Un procedimiento con azar; aquí, sortear una posición de la frase. *→ Lo que necesitas de probabilidad.* |
| Evento | Un conjunto de resultados del experimento: «la siguiente es vocal». *→ Lo que necesitas de probabilidad.* |
| Probabilidad conjunta | La de que ocurran dos eventos a la vez, ${\Pr(A\cap B)}$. *→ Lo que necesitas de probabilidad.* |
| Independencia | Saber uno no cambia la probabilidad del otro: ${\Pr(A\cap B)}$ es ${\Pr(A)\Pr(B)}$. *→ Lo que necesitas de probabilidad.* |
| Independencia condicional | Dado $B$, saber $D$ ya no agrega nada: si ${\Pr(D\cap B)>0}$, ${\Pr(A\mid D,B)}$ es ${\Pr(A\mid B)}$. *→ Lo que necesitas de probabilidad.* |
| Partición | Casos que no se traslapan y cubren todo. *→ Lo que necesitas de probabilidad.* |
| Ley de los grandes números | El promedio de muchas repeticiones independientes se acerca a la probabilidad. *→ Lo que necesitas de probabilidad.* |
| Estado | Valor posible de $S_t$; puede ser una clase de letra o un contexto. *→ La cadena de Markov, en general.* |
| Muestrear una fila | Elegir un estado con las probabilidades de una fila y un uniforme $u$. *→ El problema de Markov.* |
| Trayectoria | Secuencia de estados $s_{i_0},\dots,s_{i_t}$, con repeticiones permitidas. El pseudocódigo de conteo la abrevia como $s_0,\dots,s_T$. *→ La cadena de Markov, en general.* |
| Réplica | Una trayectoria simulada, independiente de las demás. *→ La cadena de Markov, en general.* |
| Salidas | Las transiciones que parten de un estado, $N(s)$; la última letra no tiene salida. *→ Ajustar contando.* |
| Verosimilitud | La probabilidad de los datos observados vista como función de $P$. *→ Ajustar contando.* |
| Cero estructural | Transición imposible por las reglas o la normalización: dos espacios seguidos. *→ El problema de Markov.* |
| Transición no observada | Un par con conteo 0 que sí podría ocurrir: q→a. *→ Ajustar contando.* |
| Estado sin salidas | Un estado con ${N(s)=0}$: no aparece, como la «k» en el *Quijote*, o solo aparece al final. Los datos no determinan su fila. *→ Ajustar contando.* |
| Contexto | Los $h$ símbolos anteriores, que forman el estado con memoria $h$. *→ Ajustar contando.* |
| Suavizado (Laplace) | Suavizado aditivo: sumar 1 a cada conteo por símbolo siguiente antes de dividir. *→ Ajustar contando.* |
| Error estándar | La dispersión de la fracción observada en $n$ réplicas independientes alrededor de su probabilidad $p$: ${\sqrt{p(1-p)/n}}$. *→ Predecir.* |
| Semilla | El número que fija la sucesión de uniformes $u$: con el mismo modelo, inicio, orden de estados y procedimiento, la misma semilla reproduce la corrida. Las réplicas de una corrida no reinician la semilla. *→ El problema de Markov.* |
| Generar | Producir una trayectoria muestreando una fila tras otra y deslizando el contexto. *→ Generar texto.* |
| Memoria 0, 1, 2 | Unigrama, bigrama, trigrama. Shannon los numera uno arriba: su «primer orden» es memoria 0. *→ Ajustar contando; Shannon, en Generar texto.* |
| Clase | Un grupo de estados que se comunican entre sí. *→ Clasificar los estados.* |
| Clase cerrada | Una clase de la que no sale ninguna flecha: una vez dentro, la cadena se queda. Si tiene un solo estado, ese estado es **absorbente**. *→ Clasificar los estados.* |
| Transitorio, recurrente | Un estado es recurrente si la cadena, al salir de él, regresa con probabilidad 1; transitorio si no. En cadenas finitas, recurrente = estar en una clase cerrada. *→ Clasificar los estados.* |
| Irreducible | Una cadena con una sola clase, que abarca todos los estados. *→ Ajustar contando; Clasificar los estados.* |
| Distribución estacionaria | Una $\mu$ que no cambia al dar un paso: si arrancas en ella, te quedas en ella. *→ La estacionaria y sus cuatro teoremas.* |
| Las tres preguntas | En el paso $t$ ($\mu_t$), en el límite (${\lim\mu_t}$) y fracción del tiempo (${N_T(s)/T}$). No son la misma. *→ La estacionaria y sus cuatro teoremas.* |
| Iteración de potencias | Multiplicar una distribución por $P$ una y otra vez hasta que deje de cambiar más que $\mathrm{tol}$. *→ ¿Olvida su inicio?.* |

## En las figuras

- **Los estados:** V es un círculo azul con la letra V, y C un cuadrado
  amarillo con la C. La forma y la letra bastan; el color solo ayuda.
- **El árbol de dos pasos:** el borde grueso marca las hojas que entran a la
  suma que se pide.
- **Recuperar una matriz:** el punto con línea es la mediana de las réplicas,
  y la franja va del 5 % al 95 % de ellas.
- **Rachas:** las barras son las rachas reales; el rombo es la cadena y el
  triángulo, las letras independientes, cada uno con su franja del 5 % al
  95 %.
- **La probabilidad de vocal paso a paso:** la línea es la cuenta exacta y
  la marca, la fracción de las réplicas. La franja del panel de abajo mide
  ±0.010: dos errores estándar en el peor caso.
- **Diagramas «…, en palabras»:** cajas con verbos, rombos con una
  pregunta y una salida marcada con borde de otro color.

## Avisos de letras

- **$\pi$ queda reservada para la política de un agente.** En el video de la tarea representa una distribución estacionaria; aquí la escribimos $\mu$, con $\mu P=\mu$.
- **$\mu$** es una distribución sobre estados, como en el libro de Sutton y
  Barto; no es el multiplicador de KKT de optimización.
- **$T$** es el largo de una trayectoria, en pasos, como el $T$ de un
  episodio en Sutton y Barto. No es la transición $T(s,a)$ de juegos: aquí
  la transición es $P$.
- **$k$** es el número de estados. No son las simulaciones por jugada de
  Monte Carlo plano en juegos.
- **$N(s)$** cuenta **salidas**, no visitas como en juegos: la última letra
  aparece pero no sale.
- **$N_T(s)$**, con el subíndice, sí cuenta **visitas**. Son las de $s$ en
  los primeros $T$ pasos.
- **$\alpha$** es, en PageRank, la probabilidad de seguir un enlace. No es
  la $\alpha$ de alfa-beta. Brin y Page la llamaban $d$.
- **$P_{\mathcal T}$** es lo que muchos libros llaman $Q$. Aquí $Q$ queda
  para el valor de una acción, como en refuerzo.
- **La barra** de $\overline P$ no es la tilde de $\widetilde p$. La tilde
  dice «suavizada»; la barra, «filas sin salida arregladas».
- **$P$** es la matriz de transición, la misma $P$ de
  $\langle S,A,P,R,\gamma\rangle$ en agentes; no es la clase P de
  complejidad.
