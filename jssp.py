import argparse
import itertools
import time

import pulp

def ler_instancia(caminho):
    with open(caminho) as f:
        linhas = [l.split() for l in f if l.strip() and not l.startswith("#")]
    n, m = int(linhas[0][0]), int(linhas[0][1])
    rotas = []  
    for j in range(n):
        v = list(map(int, linhas[1 + j]))
        rotas.append([(v[2 * k], v[2 * k + 1]) for k in range(m)])
    return n, m, rotas


def resolver(n, m, rotas, tempo_limite=None, verbose=True):
    J, M = range(n), range(m)
    p = {(j, maq): d for j in J for (maq, d) in rotas[j]}
    V = sum(p.values())  

    modelo = pulp.LpProblem("JSSP", pulp.LpMinimize)


    s = pulp.LpVariable.dicts("s", p.keys(), lowBound=0)          
    cmax = pulp.LpVariable("Cmax", lowBound=0)                    
    y = {}                                                        
    for k in M:
        for i, j in itertools.combinations(J, 2):
            y[i, j, k] = pulp.LpVariable(f"y_{i}_{j}_{k}", cat="Binary")

    modelo += cmax
 
    for j in J:
        for a in range(m - 1):
            (k1, d1), (k2, _) = rotas[j][a], rotas[j][a + 1]
            modelo += s[j, k2] >= s[j, k1] + d1, f"prec_{j}_{a}"

    for (i, j, k), yv in y.items():
        modelo += s[i, k] >= s[j, k] + p[j, k] - V * yv, f"disjA_{i}_{j}_{k}"
        modelo += s[j, k] >= s[i, k] + p[i, k] - V * (1 - yv), f"disjB_{i}_{j}_{k}"
  
    for j in J:
        k_ult, d_ult = rotas[j][-1]
        modelo += cmax >= s[j, k_ult] + d_ult, f"cmax_{j}"

    solver = pulp.PULP_CBC_CMD(msg=verbose, timeLimit=tempo_limite)
    t0 = time.time()
    modelo.solve(solver)
    tempo = time.time() - t0

    resultado = {
        "status": {1: "Otimo provado", 2: "Viavel"}
                  .get(modelo.sol_status, pulp.LpStatus[modelo.status]),
        "makespan": pulp.value(cmax),
        "tempo_s": round(tempo, 2),
        "n_variaveis": len(modelo.variables()),
        "n_binarias": len(y),
        "n_restricoes": len(modelo.constraints),
        "inicio": {op: s[op].value() for op in p},
    }
    return resultado


def imprimir_agenda(n, m, rotas, inicio):
    print("\nAgenda por maquina (job:inicio-fim):")
    for k in range(m):
        ops = sorted((inicio[j, k], j) for j in range(n))
        dur = {j: d for j in range(n) for (maq, d) in rotas[j] if maq == k}
        txt = "  ".join(f"J{j}:{int(t)}-{int(t + dur[j])}" for t, j in ops)
        print(f"  M{k}: {txt}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("instancia")
    ap.add_argument("--tempo", type=float, default=None, help="limite de tempo (s)")
    ap.add_argument("--silencioso", action="store_true")
    a = ap.parse_args()

    n, m, rotas = ler_instancia(a.instancia)
    r = resolver(n, m, rotas, a.tempo, verbose=not a.silencioso)

    print(f"\nInstancia: {a.instancia} ({n} jobs x {m} maquinas)")
    for chave in ["status", "makespan", "tempo_s", "n_variaveis", "n_binarias", "n_restricoes"]:
        print(f"  {chave}: {r[chave]}")
    if r["makespan"] is not None:
        imprimir_agenda(n, m, rotas, r["inicio"])
