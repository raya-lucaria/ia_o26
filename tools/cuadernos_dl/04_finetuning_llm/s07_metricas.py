# §7 · Métricas, explicadas: loss y perplexity solo en el completion, exact
# match normalizado y token F1 (estilo SQuAD), base contra LoRA en
# validation. Publica normalizar, exact_match, token_f1, evaluar.

# %% [texto] s07-intro

# %% [texto] s07-loss

# %% [texto] s07-em

# %% [texto] s07-f1

# %% [codigo] s07-funciones
from collections import Counter


def normalizar(texto):
    """Minúsculas y espacios colapsados (ni puntuación ni artículos se tocan)."""
    return " ".join(texto.lower().split())


def exact_match(pred, real):
    return float(normalizar(pred) == normalizar(real))


def token_f1(pred, real):
    """F1 entre las bolsas de palabras de pred y real (estilo SQuAD)."""
    p, r = normalizar(pred).split(), normalizar(real).split()
    if not p or not r:
        return float(p == r)
    comunes = sum((Counter(p) & Counter(r)).values())
    if comunes == 0:
        return 0.0
    precision, recall = comunes / len(p), comunes / len(r)
    return 2 * precision * recall / (precision + recall)


# Un ejemplo a mano, para ver la diferencia entre las dos:
real = "SELECT name FROM students WHERE age > 20"
pred = "select name from students where age >= 20"
print(f"exact match = {exact_match(pred, real):.0f} · "
      f"token F1 = {token_f1(pred, real):.3f}")

# %% [codigo] s07-evaluar
def evaluar(parte):
    """Base y LoRA en los primeros n_eval ejemplos de `parte`: una tabla con
    las cuatro métricas y las respuestas de cada modelo."""
    ejs = DATOS[parte][:P["n_eval"]]
    reales = [e["completion"] for e in ejs]
    filas, preds = {}, {}
    for nombre, lora in [("base", False), ("LoRA", True)]:
        t0 = time.perf_counter()
        loss = perdida_val(parte, lora=lora)
        preds[nombre] = generar([e["prompt"] for e in ejs], lora=lora)
        filas[nombre] = {
            "loss": loss, "perplexity": math.exp(min(loss, 50)),
            "exact match %": 100 * np.mean(
                [exact_match(p, r) for p, r in zip(preds[nombre], reales)]),
            "token F1 %": 100 * np.mean(
                [token_f1(p, r) for p, r in zip(preds[nombre], reales)])}
        print(f"{nombre}: {time.perf_counter() - t0:.0f} s")
    print(f"({len(ejs)} ejemplos de {parte} para generar, "
          f"{min(len(TOKS[parte]), P['n_val_loss'])} para la loss)")
    return pd.DataFrame(filas).T, preds


def por_ejemplo(parte, preds, n=5):
    """Las primeras n respuestas, con su exact match y su F1."""
    ejs = DATOS[parte][:min(n, len(preds["base"]))]
    df = respuestas([e["prompt"] for e in ejs],
                    esperado=[e["completion"] for e in ejs],
                    base=preds["base"][:n], LoRA=preds["LoRA"][:n])
    df["EM base / LoRA"] = [
        f"{exact_match(b, e['completion']):.0f} / "
        f"{exact_match(l, e['completion']):.0f}"
        for b, l, e in zip(preds["base"], preds["LoRA"], ejs)]
    df["F1 base / LoRA"] = [
        f"{token_f1(b, e['completion']):.2f} / "
        f"{token_f1(l, e['completion']):.2f}"
        for b, l, e in zip(preds["base"], preds["LoRA"], ejs)]
    return df

# %% [codigo] s07-validation
VAL_TABLA, VAL_PRED = evaluar("validation")
display(VAL_TABLA.round(3))
mostrar(por_ejemplo("validation", VAL_PRED))

# %% [texto] s07-lee
