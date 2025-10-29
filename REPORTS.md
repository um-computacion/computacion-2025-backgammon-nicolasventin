# Automated Reports
## Coverage Report
```text
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
src/__init__.py              0      0   100%
src/game/__init__.py         0      0   100%
src/game/backgammon.py     119     35    71%   29-30, 36, 55, 71, 91-96, 100, 103, 113, 138-140, 145, 147, 152, 156-162, 165, 168-186
src/game/checker.py         12      0   100%
src/game/dado.py            14      0   100%
src/game/jugador.py          6      0   100%
src/game/tablero.py        108      8    93%   61-63, 75-76, 80-81, 96
src/ui/__init__.py           0      0   100%
src/ui/cli.py               25     25     0%   1-45
src/ui/gui.py                0      0   100%
------------------------------------------------------
TOTAL                      284     68    76%

```
## Pylint Report
```text
************* Module src.game.jugador
src/game/jugador.py:4:0: R0903: Too few public methods (1/2) (too-few-public-methods)
************* Module src.game.dado
src/game/dado.py:8:0: R0903: Too few public methods (1/2) (too-few-public-methods)
************* Module src.game.backgammon
src/game/backgammon.py:32:4: R0914: Too many local variables (19/15) (too-many-locals)
src/game/backgammon.py:32:4: R0911: Too many return statements (16/6) (too-many-return-statements)
src/game/backgammon.py:32:4: R0912: Too many branches (26/12) (too-many-branches)
src/game/backgammon.py:126:4: R0912: Too many branches (19/12) (too-many-branches)

-----------------------------------
Your code has been rated at 9.89/10


```
