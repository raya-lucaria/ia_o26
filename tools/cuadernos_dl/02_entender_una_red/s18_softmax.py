# §18 · Softmax y la loss.
# Consume CORRIDAS["s16-elegido"] (el MLP elegido por validation en §16). Si
# falta, reutiliza s04-oculta o la entrena con la Config exacta de §4 y lo dice.
# Publica: corrida_18, modelo_18, escala_18, logits_val, k_18. No usa test.

# %% [texto] s18-intro

# %% [codigo] s18-modelo
# El modelo de esta sección: el que §16 eligió por validation. Si corriste
# esta sección sin §16, usamos la línea base de §4 (y la entrenamos si falta).
import torch.nn.functional as F

if "s16-elegido" in CORRIDAS:
    corrida_18 = CORRIDAS["s16-elegido"]
    print("Usamos el modelo elegido en §16:", corrida_18.id)
elif "s04-oculta" in CORRIDAS:
    corrida_18 = CORRIDAS["s04-oculta"]
    print("No hay s16-elegido (no corriste §16): usamos la línea base "
          "s04-oculta, que ya estaba entrenada.")
else:
    print("No hay s16-elegido ni s04-oculta: entrenamos ahora la línea base "
          "de §4 (784→128→10, ReLU, Adam 1e-3, 8 epochs).")
    corrida_18 = entrenar(Config(id="s04-oculta", seccion=4,
                                 capas=[784, 128, 10], activacion="relu",
                                 optimizer="adam", lr=1e-3, epochs=8))

escala_18 = corrida_18.config.escala
modelo_18 = cargar(corrida_18, "mejor")      # el checkpoint de la mejor epoch
print(modelo_18)

# Ninguna capa del modelo es softmax: la red termina en 10 LOGITS.
# El softmax vive dentro de CrossEntropyLoss (lo vemos en esta sección).
assert not any(isinstance(m, nn.Softmax) for m in modelo_18.modules())

# %% [codigo] s18-un-digito
# Logits de TODO validation (sin gradiente, por bloques de 2048).
X_val, y_val = DATOS[escala_18]["validation"]
with torch.no_grad():
    logits_val = torch.cat([modelo_18(X_val[i:i + 2048])
                            for i in range(0, len(X_val), 2048)])
prob_val = torch.softmax(logits_val, dim=1)      # [n, 10]; cada fila suma 1
confianza, prediccion = prob_val.max(dim=1)

# Un dígito con algo de duda: bien clasificado, pero con 0.5 < max ŷ_c < 0.9,
# para que se vea más de una barra. Si no hay ninguno, el acierto (o, si no
# hay aciertos, el ejemplo) con la confianza más baja.
acierto = prediccion == y_val
dudosos = torch.nonzero(acierto & (confianza > 0.5) & (confianza < 0.9))
if len(dudosos):
    k_18 = int(dudosos[0, 0])
elif acierto.any():
    k_18 = int(torch.where(acierto, confianza, 2.0).argmin())
else:
    k_18 = int(confianza.argmin())
z = logits_val[k_18].cpu()                       # z_0 … z_9
y_gorro = prob_val[k_18].cpu()                   # ŷ_0 … ŷ_9
y_k = int(y_val[k_18])
colores_k = ["#9e9e9e"] * 10
colores_k[y_k] = COLORES["validation"]           # la clase verdadera

fig, (ax_img, ax_z, ax_p) = plt.subplots(
    1, 3, figsize=(15, 3.8), gridspec_kw={"width_ratios": [1, 2, 2]})
ax_img.imshow(DATOS["01"]["validation"][0][k_18].reshape(28, 28).cpu(),
              cmap="gray_r")
ax_img.set_title(f"validation #{k_18}: etiqueta y = {y_k}")
ax_img.axis("off")
ax_z.bar(range(10), z, color=colores_k)
ax_z.axhline(0, color="black", lw=0.8)
ax_z.set_title("Logits $z_c$ (lo que sale de la red)")
ax_z.set_ylabel("logit $z_c$")
barras = ax_p.bar(range(10), y_gorro, color=colores_k)
ax_p.set_ylim(0, 1)
ax_p.set_title(r"Probabilidades $\widehat y_c$ = softmax(z)")
ax_p.set_ylabel(r"probabilidad $\widehat y_c$")
ax_p.legend([barras[y_k]], [f"clase verdadera y = {y_k}"])
for ax in (ax_z, ax_p):
    ax.set_xticks(range(10))
    ax.set_xlabel("clase c (dígito)")
plt.tight_layout()
plt.show()

# La cuenta, clase por clase (e^z en float64 para no desbordar).
e_z = torch.exp(z.double())
display(pd.DataFrame({"clase c": range(10), "logit z_c": z.numpy(),
                      "e^{z_c}": e_z.numpy(),
                      "ŷ_c = e^{z_c} / Σ e^{z_j}": (e_z / e_z.sum()).numpy()})
        .round(4))
print(f"Σ ŷ_c = {float(y_gorro.sum()):.6f}   ·   argmax z = {int(z.argmax())}"
      f"   ·   argmax ŷ = {int(y_gorro.argmax())}")

# %% [texto] s18-un-digito-mira

# %% [texto] s18-apuesta

# %% [codigo] s18-temperatura
# Temperatura: softmax(z / T). Dividir TODOS los logits entre el mismo T > 0
# no cambia su orden, así que el argmax no cambia; la confianza sí.
TEMPERATURAS = [0.5, 1, 2, 5]
fig, ejes = plt.subplots(1, len(TEMPERATURAS), figsize=(15, 3.6), sharey=True)
filas = []
for T, ax in zip(TEMPERATURAS, ejes):
    p_T = torch.softmax(z / T, dim=0)
    ax.bar(range(10), p_T, color=colores_k)
    ax.set_title(f"T = {T}" + ("  (el modelo tal cual)" if T == 1 else ""))
    ax.set_xticks(range(10))
    ax.set_xlabel("clase c")
    filas.append({"T": T, "argmax": int(p_T.argmax()),
                  "max ŷ_c": float(p_T.max()),
                  f"ŷ_y (y = {y_k})": float(p_T[y_k]),
                  "loss −log ŷ_y":                 # estable: log_softmax
                  float(-torch.log_softmax(z / T, dim=0)[y_k])})
ejes[0].set_ylim(0, 1)
ejes[0].set_ylabel(r"probabilidad $\widehat y_c$")
fig.suptitle(f"El mismo dígito (validation #{k_18}) con softmax(z / T)")
plt.tight_layout()
plt.show()

tabla_T = pd.DataFrame(filas)
display(tabla_T.round(4))
assert tabla_T["argmax"].nunique() == 1          # el argmax no se movió
print("El argmax es el mismo en las", len(TEMPERATURAS), "temperaturas:",
      int(tabla_T["argmax"].iloc[0]))

# %% [plegada] s18-apuesta-respuesta

# %% [texto] s18-cross-entropy-texto

# %% [codigo] s18-cross-entropy
# 1) Un dígito, a mano: la loss es −log de la probabilidad de la clase y.
a_mano = -torch.log(y_gorro[y_k])               # (sin cuidar la estabilidad)
por_pytorch = F.cross_entropy(z.unsqueeze(0), torch.tensor([y_k]))
print(f"dígito #{k_18}:  −log ŷ_y a mano = {float(a_mano):.6f}"
      f"   ·   CrossEntropyLoss = {float(por_pytorch):.6f}")

# 2) Todo validation: la loss de cada ejemplo, ℓ_k = −log ŷ_{k, y_k} ...
log_p_val = torch.log_softmax(logits_val, dim=1)
filas_k = torch.arange(len(y_val), device=y_val.device)
perdida_k = -log_p_val[filas_k, y_val]           # [n], una por ejemplo

# ... y su promedio, calculado de cuatro maneras.
maneras = {
    "promedio de −log ŷ_y (a mano)": perdida_k.mean(),
    "CrossEntropyLoss(logits)": nn.CrossEntropyLoss()(logits_val, y_val),
    "NLLLoss(log_softmax(logits))": nn.NLLLoss()(log_p_val, y_val),
    "evaluar(...) de la caja": evaluar(modelo_18, escala_18, "validation")[0],
}
display(pd.DataFrame({"manera": list(maneras),
                      "loss de validation": [float(v) for v in
                                             maneras.values()]}).round(6))
valores = [float(v) for v in maneras.values()]
assert max(valores) - min(valores) < 1e-3        # la misma cantidad

# 3) Dos gráficas: la curva −log p, y cómo se reparte ℓ_k en validation.
fig, (ax_c, ax_h) = plt.subplots(1, 2, figsize=(13, 4))
p = torch.linspace(0.001, 1, 500)
ax_c.plot(p, -torch.log(p), color="black", lw=2, label=r"$-\log \widehat y_y$")
ax_c.scatter([0.1], [math.log(10)], color="gray", zorder=3,
             label=r"adivinar uniforme: $\log 10 \approx 2.30$")
ax_c.scatter([float(y_gorro[y_k])], [float(a_mano)], zorder=3, s=60,
             color=COLORES["validation"], label=f"el dígito #{k_18}")
ax_c.set_xlabel(r"probabilidad de la clase verdadera $\widehat y_y$")
ax_c.set_ylabel("loss de ese ejemplo")
ax_c.set_title("Cross-entropy de un ejemplo: $-\\log \\widehat y_y$")
ax_c.legend()
ax_h.hist(perdida_k.cpu().numpy(), bins=60, color=COLORES["validation"])
ax_h.set_yscale("log")
ax_h.axvline(valores[1], color="black", ls="--", label="promedio (la loss)")
ax_h.axvline(math.log(10), color="gray", ls=":", label=r"$\log 10$")
ax_h.set_xlabel(r"loss de cada ejemplo $\ell_k$")
ax_h.set_ylabel("número de ejemplos (escala log)")
ax_h.set_title("Validation: la loss de cada uno de sus ejemplos")
ax_h.legend()
plt.tight_layout()
plt.show()

# %% [texto] s18-cross-entropy-mira

# %% [texto] s18-estabilidad-texto

# %% [codigo] s18-estabilidad
# Un caso extremo en float32 (el tipo con el que entrena todo el notebook):
# una observación, dos clases, logits z = [0, −1000] y clase verdadera 1.
z_ext = torch.tensor([[0.0, -1000.0]], dtype=torch.float32)
y_ext = torch.tensor([1])
print("e^{-1000} en float32 =", torch.exp(torch.tensor(-1000.0)).item(),
      "  (el positivo normal más chico de float32 es",
      f"{torch.finfo(torch.float32).tiny:.1e}; e^{{-1000}} ≈ 1e-435)")

p_ingenua = torch.softmax(z_ext, dim=1)          # [[1., 0.]]
log_p_ingenua = p_ingenua.log()                  # [[0., -inf]]
maneras_ext = [
    ("softmax(z).log(), clase 1", log_p_ingenua[0, 1], "−1000"),
    ("NLLLoss(softmax(z).log())", nn.NLLLoss()(log_p_ingenua, y_ext), "1000"),
    ("NLLLoss(log_softmax(z))",
     nn.NLLLoss()(torch.log_softmax(z_ext, dim=1), y_ext), "1000"),
    ("CrossEntropyLoss(z)", nn.CrossEntropyLoss()(z_ext, y_ext), "1000"),
]
display(pd.DataFrame({"manera": [m for m, _, _ in maneras_ext],
                      "resultado en float32": [float(v) for _, v, _ in
                                               maneras_ext],
                      "valor exacto (redondeado)": [e for _, _, e in
                                                    maneras_ext]}))

# %% [codigo] s18-log-sum-exp
# El truco log-sum-exp, a mano. Con m = max_j z_j:
#   log ŷ_c = z_c − log Σ_j e^{z_j} = z_c − m − log Σ_j e^{z_j − m}
# Ahora el exponente más grande es e^0 = 1: nada desborda, y la suma
# vale al menos 1, así que su log nunca es −inf.
def log_softmax_a_mano(z):
    m = z.max(dim=1, keepdim=True).values                  # [n, 1]
    return z - m - torch.log(torch.exp(z - m).sum(dim=1, keepdim=True))


def softmax_ingenuo(z):                                    # sin restar m
    e = torch.exp(z)
    return e / e.sum(dim=1, keepdim=True)


# Dos logits peligrosos: uno muy negativo (underflow: e^z se vuelve 0)
# y uno muy positivo (overflow: e^z se vuelve inf, e inf / inf = nan).
for z_prueba in ([[0.0, -1000.0]], [[1000.0, 0.0]]):
    zt = torch.tensor(z_prueba)
    print(f"z = {z_prueba[0]}")
    print("   log(softmax ingenuo):", softmax_ingenuo(zt).log().tolist()[0])
    print("   log-sum-exp a mano:  ", log_softmax_a_mano(zt).tolist()[0])
    print("   torch.log_softmax:   ", torch.log_softmax(zt, dim=1).tolist()[0])

# Y en los logits reales de validation, el truco da lo mismo que PyTorch.
assert torch.allclose(log_softmax_a_mano(logits_val), log_p_val, atol=1e-5)
print("\nEn los", len(logits_val), "logits de validation, log-sum-exp a mano "
      "= torch.log_softmax")

# %% [texto] s18-estabilidad-mira

# %% [texto] s18-arquitectura-texto

# %% [codigo] s18-arquitectura
# La red completa del modelo elegido y, a la derecha, el paso que la red no
# hace pero la loss sí: softmax de los 10 logits del dígito de arriba.
fig, (ax_red, ax_sm) = plt.subplots(
    1, 2, figsize=(15, 4.8), gridspec_kw={"width_ratios": [3, 2]})
if corrida_18.config.modelo is None:
    dibujar_red(corrida_18.config.capas, ax=ax_red,
                titulo=f"El modelo elegido ({corrida_18.id}): "
                       f"{corrida_18.config.capas}")
else:                                           # una CNN no se dibuja así
    ax_red.text(0.5, 0.5, f"{corrida_18.id}: no es un MLP", ha="center")
    ax_red.axis("off")

filas_y = np.arange(10)[::-1]                    # clase 0 arriba
for c, fila in zip(range(10), filas_y):
    ax_sm.text(0.0, fila, f"$z_{c}$ = {float(z[c]):6.2f}", va="center",
               ha="right", fontsize=9, family="monospace")
    ax_sm.text(3.0, fila, rf"$\widehat y_{c}$", va="center", ha="right")
ax_sm.barh(filas_y, 1.6 * y_gorro.numpy(), left=3.15, height=0.6,
           color=colores_k)
for c, fila in zip(range(10), filas_y):                  # el valor de ŷ_c
    ax_sm.text(3.2 + 1.6 * float(y_gorro[c]), fila, f"{float(y_gorro[c]):.2f}",
               va="center", fontsize=8)
ax_sm.add_patch(plt.Rectangle((0.6, 1.5), 1.6, 6, fill=False, lw=1.5))
ax_sm.text(1.4, 5.6, "softmax", ha="center", va="center", fontsize=13)
ax_sm.text(1.4, 3.9, r"$\frac{e^{z_c}}{\sum_j e^{z_j}}$", ha="center",
           va="center", fontsize=20)
for x0, x1 in ((0.1, 0.55), (2.25, 2.7)):
    ax_sm.annotate("", xy=(x1, 4.5), xytext=(x0, 4.5),
                   arrowprops=dict(arrowstyle="->", lw=1.5))
ax_sm.set_xlim(-1.6, 5.4)
ax_sm.set_ylim(-0.8, 9.8)
ax_sm.axis("off")
ax_sm.set_title(f"10 logits → softmax → 10 probabilidades (#{k_18}, y = {y_k})")
plt.tight_layout()
plt.show()

print("En el código, la red termina en los logits; softmax y −log ŷ_y van")
print("juntos dentro de CrossEntropyLoss (con log-sum-exp).")

# %% [texto] s18-que-viste
