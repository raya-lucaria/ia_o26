# §3 · La caja de herramientas: un dígito de punta a punta, el training loop
# anotado, y las funciones que usan todas las secciones (Contrato congelado).

# %% [texto] s03-intro

# %% [codigo] s03-construir-red
# El nombre de cada activación → la capa de PyTorch que la aplica.
ACTIVACIONES = {"relu": nn.ReLU, "sigmoide": nn.Sigmoid, "tanh": nn.Tanh,
                "gelu": nn.GELU, "identidad": nn.Identity}


def construir_red(capas, activacion="relu", batch_norm=False, dropout=0.0,
                  init="defecto"):
    """capas = [784, d_1, …, 10] → nn.Sequential.
    Cada capa oculta: Linear → (BatchNorm) → activación g → (Dropout).
    La última Linear entrega los 10 logits, SIN activación: la softmax va
    dentro de la loss (nn.CrossEntropyLoss). [784, 10] es la regresión
    logística multiclase de la unidad 9."""
    piezas = []
    for l in range(1, len(capas)):
        piezas.append(nn.Linear(capas[l - 1], capas[l]))  # W^(l): [d_l, d_{l-1}]
        if l < len(capas) - 1:                             # solo capas ocultas
            if batch_norm:
                piezas.append(nn.BatchNorm1d(capas[l]))
            piezas.append(ACTIVACIONES[activacion]())
            if dropout > 0:
                piezas.append(nn.Dropout(dropout))
    red = nn.Sequential(*piezas)
    for capa in red:
        if isinstance(capa, nn.Linear) and init != "defecto":
            if init == "he":          # normal con varianza 2 / d_{l-1}, como el 01
                nn.init.kaiming_normal_(capa.weight, nonlinearity="relu")
            elif init == "ortogonal":  # filas ortonormales: W W^T = I
                nn.init.orthogonal_(capa.weight)
            else:
                raise ValueError(f"init desconocida: {init}")
            nn.init.zeros_(capa.bias)
    return red


print(construir_red([784, 128, 10]))

# %% [texto] s03-punta-a-punta-explica

# %% [codigo] s03-punta-a-punta
torch.manual_seed(SEMILLA)
red = construir_red([784, 128, 10]).to(DEVICE)   # .to(DEVICE): pesos a la GPU
X, y = DATOS["estandar"]["train"]
xb, yb = X[:4], y[:4]                 # un batch de B = 4 dígitos, uno por FILA
print("entrada xb:", tuple(xb.shape), "← [B, 784]")

# La primera capa por dentro: z = x W^T + b. W tiene filas = destino (128)
# y columnas = origen (784), como en la notación; por eso se multiplica por W.T.
W, b = red[0].weight, red[0].bias
print("W^(1):", tuple(W.shape), "← [destino 128, origen 784]")
z = xb @ W.T + b
assert torch.allclose(z, red[0](xb), atol=1e-5)
print("z^(1) = xb @ W.T + b:", tuple(z.shape), "← [B, 128]")

logits = red(xb)                      # forward completo
print("logits:", tuple(logits.shape), "← [B, 10], un número por dígito")
print("etiquetas yb:", yb.tolist(), yb.dtype, "← enteros, no one-hot")

perdida_fn = nn.CrossEntropyLoss()    # softmax + −log de la clase correcta
perdida = perdida_fn(logits, yb)
print(f"loss = {perdida.item():.3f}  (adivinar parejo daría log 10 ≈ 2.303)")
prediccion = logits.argmax(dim=1)     # la clase con el logit más grande
print("predicción (argmax):", prediccion.tolist(), "· real:", yb.tolist())

# %% [texto] s03-loop-explica

# %% [codigo] s03-loop
torch.manual_seed(SEMILLA)
red = construir_red([784, 128, 10]).to(DEVICE)
optimizer = torch.optim.SGD(red.parameters(), lr=0.03)   # η = 0.03
X, y = DATOS["estandar"]["train"]
B = 128
for paso in range(1, 6):
    idx = torch.randint(0, len(X), (B,), device=DEVICE)  # un mini-batch 𝓑
    optimizer.zero_grad()           # 1. borra los gradientes del paso anterior
    logits = red(X[idx])            # 2. forward: [B, 784] → [B, 10]
    perdida = perdida_fn(logits, y[idx])   # 3. loss promedio sobre el batch
    perdida.backward()              # 4. backpropagation: llena p.grad
    optimizer.step()                # 5. p ← p − η · p.grad, para cada parámetro
    print(f"paso {paso}: loss del batch = {perdida.item():.3f}")

# El paso 5 a mano: es exactamente el W ← W − η ∇W del notebook 01.
antes = [p.detach().clone() for p in red.parameters()]
optimizer.zero_grad()
perdida_fn(red(X[idx]), y[idx]).backward()
with torch.no_grad():
    a_mano = [p - 0.03 * p.grad for p in red.parameters()]
optimizer.step()
iguales = all(torch.allclose(p, q, atol=1e-6)
              for p, q in zip(red.parameters(), a_mano))
print("optimizer.step() == p − η·grad a mano:", iguales)
del red, optimizer, antes, a_mano

# %% [texto] s03-config-explica

# %% [codigo] s03-config
@dataclass
class Config:
    """Todo lo que define una corrida. Solo id y seccion son obligatorios."""
    id: str
    seccion: int
    capas: list = field(default_factory=lambda: [784, 128, 10])
    activacion: str = "relu"
    batch_norm: bool = False
    dropout: float = 0.0
    init: str = "defecto"
    modelo: Callable | None = None      # si no es None, sustituye construir_red
    optimizer: str = "adam"             # sgd, momentum, adam, adam_l2, adamw
    lr: float = 1e-3                    # η
    weight_decay: float = 0.0           # solo pesos, nunca sesgos
    batch: int = 128                    # batch ≥ n de train ⇒ full-batch
    epochs: int = 5
    max_pasos: int | None = None        # tope de actualizaciones
    eval_cada_pasos: int | None = None  # evaluar cada tantos pasos, no por epoch
    escala: str = "estandar"            # "crudo", "01" o "estandar"
    idx_train: torch.Tensor | None = None   # subconjunto de train
    ruido_etiquetas: float = 0.0        # fracción de train con etiqueta cambiada
    paciencia: int | None = None        # early stopping sobre loss de validation
    semilla_init: int = 0               # pesos iniciales
    semilla_orden: int = 0              # orden de los batches
    medir_por_paso: bool = False        # norma del gradiente y ‖ΔW‖/‖W‖ por capa
    datos: str = "50k-limpio"           # etiqueta para agrupar la tabla maestra


@dataclass
class Corrida:
    """El resultado de entrenar(): historial y checkpoints."""
    id: str
    config: Config
    historial: pd.DataFrame        # una fila por evaluación
    por_paso: pd.DataFrame | None  # una fila por (paso, capa), si se midió
    mejor: dict                    # state_dict de la mejor evaluación, en CPU
    ultima: dict                   # state_dict de la última, en CPU
    mejor_epoch: float             # epoch de menor loss de validation
    divergio: bool                 # la loss se volvió inf o nan
    paso_no_finito: int | None     # el primer paso con loss no finita
    parametros: int                # número de pesos y sesgos


CORRIDAS = {}   # id → Corrida; reejecutar una celda reemplaza su corrida


def config_profunda(activacion="relu", **cambios):
    """La red profunda de §13–15: 6 ocultas de 128, SGD η = 0.03, pesos
    iniciales ortogonales, sesgos en cero. `cambios` sobrescribe campos."""
    base = dict(id=f"profunda-{activacion}", seccion=13,
                capas=[784] + [128] * 6 + [10], activacion=activacion,
                init="ortogonal", optimizer="sgd", lr=0.03)
    base.update(cambios)
    return Config(**base)

# %% [texto] s03-evaluar-explica

# %% [codigo] s03-evaluar
def medir(modelo, X, y, bloque=4096):
    """Loss y accuracy promedio de `modelo` sobre (X, y) completos, por
    bloques, en modo eval() (BN usa sus promedios; dropout se apaga)."""
    estaba_entrenando = modelo.training
    modelo.eval()
    suma = torch.zeros((), device=X.device)       # se acumula en la GPU
    aciertos = torch.zeros((), device=X.device)
    with torch.no_grad():                 # evaluar no necesita gradientes
        for i in range(0, len(X), bloque):
            logits = modelo(X[i:i + bloque])
            suma += nn.functional.cross_entropy(
                logits, y[i:i + bloque], reduction="sum")
            aciertos += (logits.argmax(1) == y[i:i + bloque]).sum()
    modelo.train(estaba_entrenando)
    loss = suma.item() / len(X)
    # Con logits inf o nan la accuracy no significa nada: también es nan.
    return loss, aciertos.item() / len(X) if math.isfinite(loss) else math.nan


def evaluar(modelo, escala, conjunto):
    """(loss, accuracy) de `modelo` en DATOS[escala][conjunto], completo."""
    X, y = DATOS[escala][conjunto]
    return medir(modelo, X, y)


def crear_optimizer(cfg, modelo):
    """El optimizer de cfg. weight_decay va SOLO a los pesos (ndim > 1):
    los sesgos y los parámetros de BN quedan en un grupo sin decay."""
    pesos = [p for p in modelo.parameters() if p.ndim > 1]
    otros = [p for p in modelo.parameters() if p.ndim <= 1]
    grupos = [{"params": pesos, "weight_decay": cfg.weight_decay},
              {"params": otros, "weight_decay": 0.0}]
    if cfg.optimizer == "sgd":
        return torch.optim.SGD(grupos, lr=cfg.lr)
    if cfg.optimizer == "momentum":
        return torch.optim.SGD(grupos, lr=cfg.lr, momentum=0.9)
    if cfg.optimizer in ("adam", "adam_l2"):   # L2 acoplado: entra al gradiente
        return torch.optim.Adam(grupos, lr=cfg.lr)
    if cfg.optimizer == "adamw":               # decay desacoplado del gradiente
        return torch.optim.AdamW(grupos, lr=cfg.lr)
    raise ValueError(f"optimizer desconocido: {cfg.optimizer}")


def red_de(cfg):
    """La red que pide cfg: cfg.modelo() si existe; si no, construir_red."""
    if cfg.modelo is not None:
        return cfg.modelo()
    return construir_red(cfg.capas, cfg.activacion, cfg.batch_norm,
                         cfg.dropout, cfg.init)


def cargar(corrida, cual="mejor"):
    """Reconstruye la red de `corrida` con su checkpoint ("mejor" o "ultima")."""
    modelo = red_de(corrida.config)
    modelo.load_state_dict(corrida.mejor if cual == "mejor" else corrida.ultima)
    return modelo.to(DEVICE).eval()

# %% [texto] s03-entrenar-explica

# %% [codigo] s03-preparar
def datos_de_entrenamiento(cfg):
    """(X, y) de train para cfg: subconjunto y etiquetas alteradas."""
    X, y = DATOS[cfg.escala]["train"]
    if cfg.idx_train is not None:
        idx = cfg.idx_train.to(DEVICE)
        idx = idx[idx < len(X)]          # con RAPIDO, train es más chico
        X, y = X[idx], y[idx]
    if cfg.ruido_etiquetas > 0:
        g = torch.Generator().manual_seed(SEMILLA)       # siempre las mismas
        cuantas = round(cfg.ruido_etiquetas * len(y))
        cuales = torch.randperm(len(y), generator=g)[:cuantas].to(DEVICE)
        salto = torch.randint(1, 10, (cuantas,), generator=g).to(DEVICE)
        y = y.clone()
        y[cuales] = (y[cuales] + salto) % 10   # salto 1–9: SIEMPRE otra clase
    return X, y


def cortes(n, B, tiene_bn):
    """Los límites (i, j) de cada batch de una epoch. Con batch normalization
    un batch de un solo ejemplo no se puede normalizar: se une al anterior."""
    if tiene_bn and B < 2:
        raise ValueError("batch normalization necesita batch ≥ 2")
    inicios = list(range(0, n, B))
    if tiene_bn and len(inicios) > 1 and n - inicios[-1] < 2:
        inicios.pop()
    return list(zip(inicios, inicios[1:] + [n]))


def capas_con_pesos(modelo):
    """Las capas Linear y Conv, en orden: las que miden medir_por_paso."""
    return [m for m in modelo.modules()
            if isinstance(m, (nn.Linear, nn.Conv1d, nn.Conv2d))]


def medida_por_paso(capas, antes):
    """Por capa: norma del gradiente y cociente ‖W_nuevo − W‖ / ‖W‖."""
    normas = [c.weight.grad.norm() for c in capas]
    cocientes = [(c.weight.detach() - a).norm() / a.norm()
                 for c, a in zip(capas, antes)]
    return torch.stack(normas + cocientes)


def norma_pesos(modelo):
    """‖θ‖ de los pesos (matrices y filtros), sin sesgos ni parámetros de BN."""
    return math.sqrt(sum((p.detach() ** 2).sum()
                         for p in modelo.parameters() if p.ndim > 1).item())


def checkpoint(modelo):
    """Copia del state_dict en CPU (pesos y estadísticas de BN)."""
    return {k: v.detach().cpu().clone() for k, v in modelo.state_dict().items()}


def sincronizar():
    """Espera a la GPU y devuelve la hora: sin esperar, el reloj mediría
    cuándo se ENCARGÓ el trabajo, no cuándo terminó."""
    if DEVICE.type == "cuda":
        torch.cuda.synchronize()
    return time.perf_counter()

# %% [codigo] s03-registrar
def _registrar(e, cfg, modelo, X, y, filas, epoch):
    """Una evaluación: loss y accuracy en train (el que se usa para entrenar),
    validation y test completos; actualiza el mejor checkpoint y la paciencia."""
    fila = dict(epoch=epoch, pasos=e["paso"], ejemplos=e["ejemplos"],
                segundos=e["segundos"])
    for conjunto in ("train", "validation", "test"):
        Xc, yc = (X, y) if conjunto == "train" else DATOS[cfg.escala][conjunto]
        fila[f"loss_{conjunto}"], fila[f"acc_{conjunto}"] = medir(modelo, Xc, yc)
    fila["norma_pesos"] = norma_pesos(modelo)
    filas.append(fila)
    if not math.isfinite(fila["loss_train"]) and not e["divergio"]:
        e.update(divergio=True, no_finito=e["paso"], parar=True)
    lv = fila["loss_validation"]
    if math.isfinite(lv) and lv < e["mejor_loss"]:   # mejor = menor loss val
        e.update(mejor_loss=lv, mejor=checkpoint(modelo), mejor_epoch=epoch,
                 sin_mejora=0)
    else:
        e["sin_mejora"] += 1
    if cfg.paciencia is not None and e["sin_mejora"] >= cfg.paciencia:
        e["parar"] = True                            # early stopping

def revisar_finitos(pendientes, e):
    """Revisa de golpe las losses pendientes (una sola espera a la GPU). Si
    alguna es inf o nan, la corrida divergió: anota el primer paso y para."""
    if pendientes:
        malos = ~torch.isfinite(torch.stack(pendientes))
        if malos.any():
            primero = e["paso"] - len(pendientes) + 1 + int(malos.nonzero()[0, 0])
            e.update(divergio=True, no_finito=primero, parar=True)
        pendientes.clear()

# %% [codigo] s03-entrenar
def entrenar(cfg):
    """Entrena según cfg, evalúa train/validation/test completos en la epoch 0
    y tras cada epoch (o cada cfg.eval_cada_pasos), y registra en CORRIDAS."""
    epochs, max_pasos = cfg.epochs, cfg.max_pasos
    if RAPIDO:
        epochs, max_pasos = min(epochs, 2), min(max_pasos or 30, 30)
    X, y = datos_de_entrenamiento(cfg)
    n, B = len(X), min(cfg.batch, len(X))
    torch.manual_seed(cfg.semilla_init)              # mismos pesos iniciales
    modelo = red_de(cfg).to(DEVICE)
    optimizer = crear_optimizer(cfg, modelo)
    perdida_fn = nn.CrossEntropyLoss()
    orden = torch.Generator(device=DEVICE).manual_seed(cfg.semilla_orden)
    tiene_bn = any(isinstance(m, nn.BatchNorm1d) for m in modelo.modules())
    limites = cortes(n, B, tiene_bn)
    por_epoch = len(limites)                         # pasos por epoch
    capas = capas_con_pesos(modelo)
    e = dict(paso=0, ejemplos=0, segundos=0.0, sin_mejora=0, mejor_loss=math.inf,
             mejor=None, mejor_epoch=0, divergio=False, no_finito=None, parar=False)
    filas, medidas, pendientes = [], [], []
    registrar = lambda epoch: _registrar(e, cfg, modelo, X, y, filas, epoch)
    registrar(0)
    for ep in range(1, epochs + 1):
        modelo.train()
        t0 = sincronizar()
        perm = torch.randperm(n, device=DEVICE, generator=orden)
        for i, j in limites:
            idx = perm[i:j]
            optimizer.zero_grad()
            perdida = perdida_fn(modelo(X[idx]), y[idx])
            perdida.backward()
            antes = cfg.medir_por_paso and [c.weight.detach().clone()
                                            for c in capas]
            optimizer.step()
            e.update(paso=e["paso"] + 1, ejemplos=e["ejemplos"] + len(idx))
            if cfg.medir_por_paso:               # ‖∇W‖ y ‖ΔW‖/‖W‖ por capa
                medidas.append(medida_por_paso(capas, antes))
            pendientes.append(perdida.detach())  # sin esperar a la GPU
            evalua = cfg.eval_cada_pasos and e["paso"] % cfg.eval_cada_pasos == 0
            if e["paso"] % 25 == 0 or evalua or e["paso"] == max_pasos:
                revisar_finitos(pendientes, e)   # ¿inf o nan? ⇒ divergió
                if e["parar"]:
                    break
            if evalua:
                e["segundos"] += sincronizar() - t0
                registrar(e["paso"] / por_epoch)
                t0 = time.perf_counter()
                if e["parar"]:
                    break
            if max_pasos and e["paso"] >= max_pasos:
                e["parar"] = True
                break
        revisar_finitos(pendientes, e)
        e["segundos"] += sincronizar() - t0
        fin = e["parar"] or ep == epochs
        if (fin or not cfg.eval_cada_pasos) and filas[-1]["pasos"] != e["paso"]:
            registrar(e["paso"] / por_epoch if e["parar"] else ep)
        if e["parar"]:
            break
    return _cerrar(cfg, modelo, optimizer, filas, medidas, capas, e)

# %% [codigo] s03-cerrar
def _cerrar(cfg, modelo, optimizer, filas, medidas, capas, e):
    """Arma la Corrida, la registra en CORRIDAS y libera la GPU."""
    historial = pd.DataFrame(filas)
    historial["parada_temprana"] = False
    if cfg.paciencia is not None and e["sin_mejora"] >= cfg.paciencia:
        historial.loc[historial.index[-1], "parada_temprana"] = True
    por_paso = None
    if cfg.medir_por_paso and medidas:
        m = torch.stack(medidas).cpu().numpy()       # [pasos, 2 · capas]
        L = len(capas)
        por_paso = pd.DataFrame([
            dict(paso=p + 1, capa=l + 1, norma_grad=m[p, l],
                 cociente_actualizacion=m[p, L + l])
            for p in range(len(m)) for l in range(L)])
    ultima = checkpoint(modelo)
    corrida = Corrida(
        id=cfg.id, config=cfg, historial=historial, por_paso=por_paso,
        mejor=e["mejor"] if e["mejor"] is not None else ultima, ultima=ultima,
        mejor_epoch=e["mejor_epoch"], divergio=e["divergio"],
        paso_no_finito=e["no_finito"],
        parametros=sum(p.numel() for p in modelo.parameters()))
    CORRIDAS[cfg.id] = corrida                       # mismo id ⇒ reemplaza
    del modelo, optimizer
    if DEVICE.type == "cuda":
        torch.cuda.empty_cache()
    f = historial.loc[historial["epoch"] == corrida.mejor_epoch].iloc[0]
    aviso = (f" · DIVERGIÓ en el paso {corrida.paso_no_finito}"
             if corrida.divergio else "")
    print(f"{cfg.id}: {corrida.parametros:,} parámetros · {e['paso']} pasos · "
          f"mejor epoch {corrida.mejor_epoch:g} · acc validation "
          f"{f['acc_validation']:.3f} · {e['segundos']:.1f} s{aviso}")
    return corrida

# %% [texto] s03-graficas-explica

# %% [codigo] s03-curvas
ESTILOS = ["-", "--", ":", "-."]
EJE_X = {"epoch": "epoch", "pasos": "actualizaciones (pasos)",
         "actualizaciones": "actualizaciones (pasos)",
         "ejemplos": "ejemplos vistos", "segundos": "segundos de entrenamiento"}


def curvas(corridas, x="epoch", metrica="loss",
           conjuntos=("train", "validation", "test"), ax=None, titulo=None,
           log=False):
    """Curvas de `metrica` ("loss" o "acc") contra `x` para varias corridas.
    Color = conjunto y estilo de línea = corrida; con un solo conjunto y
    varias corridas, cada corrida lleva su color. Omite valores no finitos."""
    metrica = "acc" if metrica in ("acc", "accuracy") else "loss"
    columna_x = "pasos" if x == "actualizaciones" else x
    ax = ax or plt.subplots()[1]
    paleta = plt.cm.viridis(np.linspace(0, 0.9, max(len(corridas), 1)))
    algo = False
    for k, c in enumerate(corridas):
        h = c.historial
        for conjunto in conjuntos:
            v = h[f"{metrica}_{conjunto}"].to_numpy(dtype=float)
            ok = np.isfinite(v) & (v > 0 if log else True)
            if not ok.any():
                continue
            un_color = len(conjuntos) == 1 and len(corridas) > 1
            color = paleta[k] if un_color else COLORES[conjunto]
            estilo = "-" if un_color else ESTILOS[k % len(ESTILOS)]
            marca = " (divergió)" if c.divergio else ""
            ax.plot(h[columna_x].to_numpy()[ok], v[ok], estilo, color=color,
                    marker="o", ms=3, label=f"{c.id} · {conjunto}{marca}")
            algo = True
    if not algo:
        ax.text(0.5, 0.5, "divergió", transform=ax.transAxes, ha="center",
                va="center", fontsize=14, color="crimson")
    if log and algo:
        ax.set_yscale("log")
    ax.set_xlabel(EJE_X.get(x, x))
    ax.set_ylabel("loss (cross-entropy)" if metrica == "loss" else "accuracy")
    ax.set_title(titulo or f"{'Loss' if metrica == 'loss' else 'Accuracy'} "
                 f"contra {EJE_X.get(x, x)}")
    if algo:
        ax.legend(fontsize=8)
    return ax


def rejilla(corridas, x="epoch", metrica="loss", columnas=3, misma_y=True):
    """Small multiples: un panel por corrida, mismos ejes si misma_y."""
    filas = math.ceil(len(corridas) / columnas)
    fig, ejes = plt.subplots(filas, columnas, figsize=(4 * columnas, 3 * filas),
                             sharex=True, sharey=misma_y, squeeze=False)
    for ax, c in zip(ejes.flat, corridas):
        curvas([c], x=x, metrica=metrica, ax=ax, titulo=c.id)
        ax.get_legend() and ax.get_legend().remove()
    for ax in list(ejes.flat)[len(corridas):]:
        ax.set_visible(False)
    muestras = [plt.Line2D([], [], color=COLORES[k], marker="o", ms=3, label=k)
                for k in ("train", "validation", "test")]
    fig.legend(handles=muestras, loc="upper right", fontsize=8)
    fig.tight_layout()
    return fig

# %% [codigo] s03-tabla
def tabla_maestra(secciones=None):
    """Una fila por corrida registrada, con sus números en la MEJOR epoch
    (elegida por loss de validation, nunca por test)."""
    filas, vistas = [], set()
    for c in CORRIDAS.values():
        if id(c) in vistas:          # la misma corrida guardada con dos nombres
            continue
        vistas.add(id(c))
        if secciones is not None and c.config.seccion not in secciones:
            continue
        h = c.historial
        f = h.loc[h["epoch"] == c.mejor_epoch].iloc[0]
        filas.append(dict(
            id=c.id, seccion=c.config.seccion, datos=c.config.datos,
            parametros=c.parametros, mejor_epoch=c.mejor_epoch,
            pasos=int(f["pasos"]), ejemplos=int(f["ejemplos"]),
            acc_train=f["acc_train"], acc_validation=f["acc_validation"],
            acc_test=f["acc_test"], loss_train=f["loss_train"],
            loss_validation=f["loss_validation"], loss_test=f["loss_test"],
            brecha=f["acc_train"] - f["acc_validation"],
            segundos=h["segundos"].iloc[-1], divergio=c.divergio))
    tabla = pd.DataFrame(filas)
    return tabla.sort_values("seccion", kind="stable").reset_index(drop=True) \
        if len(tabla) else tabla

def experimentos_unicos():
    """Cuántas corridas distintas hay en CORRIDAS (sin contar alias)."""
    return len({id(c) for c in CORRIDAS.values()})

# %% [codigo] s03-dibujar-red
def dibujar_red(capas, ax=None, titulo=None, max_nodos=10):
    """Columnas de nodos, una por capa. La ALTURA de cada columna y cuántos
    nodos se dibujan crecen con log2 del ancho: un embudo se ve embudo.
    Si una capa tiene más nodos de los dibujados, «⋮» en medio; el número
    real va siempre debajo."""
    ax = ax or plt.subplots(figsize=(1.6 * len(capas) + 1, 3.6))[1]
    tope = math.log2(max(max(capas), 2))
    posiciones = []
    for d in capas:
        h = max(0.12, (math.log2(max(d, 2)) / tope) ** 1.5)  # media altura
        k = int(np.clip(round(1.5 * math.log2(max(d, 1))), 2, max_nodos))
        k = max(2, min(k, int(2 * h / 0.09)))       # que quepan sin encimarse
        if d <= k:                                          # caben todos
            ys = np.linspace(h, -h, d) if d > 1 else np.array([0.0])
            hueco = None
        else:                                               # se recorta
            arriba, abajo, g = (k + 1) // 2, k // 2, max(0.35 * h, 0.1)
            h = max(h, g + 0.09 * (arriba - 1))     # espacio para «⋮»
            ys = np.concatenate([np.linspace(h, g, arriba),
                                 np.linspace(-g, -h, abajo)])
            hueco = 0.0
        posiciones.append((ys, hueco))
    for j, ((ys, _), (zs, _)) in enumerate(zip(posiciones, posiciones[1:])):
        for a in ys:
            for b in zs:
                ax.plot([j, j + 1], [a, b], color="gray", lw=0.4, alpha=0.25)
    for j, (ys, hueco) in enumerate(posiciones):
        es_borde = j in (0, len(capas) - 1)
        ax.scatter(np.full(len(ys), j), ys, s=40, zorder=3, edgecolor="black",
                   color="#cfe2f3" if es_borde else "white")
        if hueco is not None:
            ax.text(j, hueco, "⋮", ha="center", va="center", fontsize=11,
                    zorder=4)
        ax.text(j, -1.2, f"{capas[j]:,}", ha="center", va="top", fontsize=9)
    ax.text(0, 1.2, "entrada\n(píxeles)", ha="center", va="bottom", fontsize=9)
    ax.text(len(capas) - 1, 1.2, "salida\n(logits)", ha="center", va="bottom",
            fontsize=9)
    ax.set_xlim(-0.6, len(capas) - 0.4)
    ax.set_ylim(-1.6, 1.7)
    ax.axis("off")
    ax.set_title(titulo or " → ".join(str(d) for d in capas), fontsize=10)
    return ax

# %% [texto] s03-demo-explica

# %% [codigo] s03-demo
# Una corrida corta de prueba: 2000 ejemplos de train, 2 epochs.
demo = entrenar(Config(id="s03-demo", seccion=3, epochs=2,
                       idx_train=subconjunto(2000), datos="2k-limpio"))
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.6),
                             gridspec_kw={"width_ratios": [1.4, 1]})
curvas([demo], metrica="loss", ax=a1, titulo="s03-demo: loss por epoch")
dibujar_red(demo.config.capas, ax=a2, titulo="La red de s03-demo")
plt.show()
print("Mirar test en cada epoch está mal (test se usa una vez, al final);")
print("aquí lo graficamos solo para aprender a leer las curvas.")
tabla_maestra()

# %% [texto] s03-que-viste
