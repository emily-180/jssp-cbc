import random
import sys

n, m, semente, saida = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
rng = random.Random(semente)
with open(saida, "w") as f:
    f.write(f"# JSSP aleatorio {n}x{m}, semente {semente}\n{n} {m}\n")
    for _ in range(n):
        maqs = list(range(m))
        rng.shuffle(maqs)
        f.write(" ".join(f"{k} {rng.randint(1, 99)}" for k in maqs) + "\n")
