# Automated Reports
## Coverage Report
```text
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
src/game/backgammon.py     124      3    98%   233, 350-351
src/game/checker.py         13      0   100%
src/game/dado.py            12      0   100%
src/game/jugador.py         14      0   100%
src/game/tablero.py         91      2    98%   74, 207
src/ui/cli.py              163     17    90%   29, 55-57, 69-71, 186-189, 309, 352-356
src/ui/pygame_ui.py        606    606     0%   1-1159
------------------------------------------------------
TOTAL                     1023    628    39%

```
## Pylint Report
```text
************* Module src.game.dado
src/game/dado.py:8:0: R0903: Too few public methods (1/2) (too-few-public-methods)
************* Module test_backgammon
tests/test_backgammon.py:10:0: R0904: Too many public methods (25/20) (too-many-public-methods)

-----------------------------------
Your code has been rated at 9.97/10


```
