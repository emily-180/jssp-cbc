# Job Shop Scheduling Problem (JSSP) – Minimização do Makespan

**Grupo:** Lnicker, Emilly e Arielce

Modelo de Programação Linear Inteira (formulação disjuntiva de Manne) em Python com PuLP, resolvido com o solver CBC.

## Arquivos

```
jssp.py               # modelo matemático e resolução
gerar_instancia.py    # gerador de instâncias aleatórias 
instancias/
  facil_ft06.txt      # 6 jobs x 6 máquinas (ft06, OR-Library; ótimo = 55)
  media_8x6.txt       # 8 jobs x 6 máquinas (semente 1)
  dificil_10x10.txt   # 10 jobs x 10 máquinas (semente 2026)
```

## Requisitos

- Python 3.8 ou superior
- PuLP (o solver CBC já vem incluído):

```
pip install pulp
```

## Como executar

```
python jssp.py instancias/facil_ft06.txt
python jssp.py instancias/media_8x6.txt
python jssp.py instancias/dificil_10x10.txt --tempo 600
```

- `--tempo 600` limita a execução a 600 segundos (recomendado para a instância difícil).
- `--silencioso` oculta o log do solver e mostra só o resumo.

No Mac/Linux, use `python3` e `pip3`.

## Observação

Máquinas e jobs são numerados a partir de 0 (M0, M1, … / J0, J1, …).
