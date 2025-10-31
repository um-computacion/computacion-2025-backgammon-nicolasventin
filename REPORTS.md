# Automated Reports
## Coverage Report
```text
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
src/__init__.py              0      0   100%
src/game/__init__.py         0      0   100%
src/game/backgammon.py     117      3    97%   136, 208-209
src/game/checker.py         13      0   100%
src/game/dado.py            12      0   100%
src/game/jugador.py         14      0   100%
src/game/tablero.py         91      1    99%   49
src/ui/__init__.py           0      0   100%
src/ui/cli.py              163     17    90%   22, 39-41, 53-55, 115-118, 198, 232-236
src/ui/gui.py                0      0   100%
------------------------------------------------------
TOTAL                      410     21    95%

```
## Pylint Report
```text
************* Module src.game.dado
src/game/dado.py:8:0: R0903: Too few public methods (1/2) (too-few-public-methods)
************* Module src.game.backgammon
src/game/backgammon.py:78:32: W0613: Unused argument 'end_point' (unused-argument)
src/game/backgammon.py:104:14: W0613: Unused argument 'start_point' (unused-argument)
************* Module test_cli
tests/test_cli.py:58:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_cli.py:60:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_cli.py:70:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_cli.py:72:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_cli.py:74:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_cli.py:84:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_cli.py:117:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_cli.py:140:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_cli.py:181:75: C0303: Trailing whitespace (trailing-whitespace)
tests/test_cli.py:183:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_cli.py:186:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_cli.py:188:70: C0303: Trailing whitespace (trailing-whitespace)
tests/test_cli.py:189:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_cli.py:193:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_cli.py:197:0: C0304: Final newline missing (missing-final-newline)
tests/test_cli.py:26:25: W0212: Access to a protected member _get_piece_char of a client class (protected-access)
tests/test_cli.py:27:25: W0212: Access to a protected member _get_piece_char of a client class (protected-access)
tests/test_cli.py:31:23: W0212: Access to a protected member _get_owner_and_count of a client class (protected-access)
tests/test_cli.py:35:23: W0212: Access to a protected member _get_owner_and_count of a client class (protected-access)
tests/test_cli.py:39:23: W0212: Access to a protected member _get_owner_and_count of a client class (protected-access)
tests/test_cli.py:45:15: W0212: Access to a protected member _get_drawing_grid of a client class (protected-access)
tests/test_cli.py:107:25: W0212: Access to a protected member _parsear_input of a client class (protected-access)
tests/test_cli.py:108:25: W0212: Access to a protected member _parsear_input of a client class (protected-access)
tests/test_cli.py:109:25: W0212: Access to a protected member _parsear_input of a client class (protected-access)
tests/test_cli.py:110:25: W0212: Access to a protected member _parsear_input of a client class (protected-access)
tests/test_cli.py:111:25: W0212: Access to a protected member _parsear_input of a client class (protected-access)
tests/test_cli.py:112:25: W0212: Access to a protected member _parsear_input of a client class (protected-access)
tests/test_cli.py:113:25: W0212: Access to a protected member _parsear_input of a client class (protected-access)
tests/test_cli.py:119:12: W0212: Access to a protected member _parsear_input of a client class (protected-access)
tests/test_cli.py:121:12: W0212: Access to a protected member _parsear_input of a client class (protected-access)
tests/test_cli.py:124:12: W0212: Access to a protected member _parsear_input of a client class (protected-access)
tests/test_cli.py:127:12: W0212: Access to a protected member _parsear_input of a client class (protected-access)
tests/test_cli.py:129:12: W0212: Access to a protected member _parsear_input of a client class (protected-access)
tests/test_cli.py:141:8: W0212: Access to a protected member _realizar_turno of a client class (protected-access)
tests/test_cli.py:133:66: W0613: Unused argument 'mock_sleep' (unused-argument)
tests/test_cli.py:158:8: W0212: Access to a protected member _realizar_turno of a client class (protected-access)
tests/test_cli.py:149:70: W0613: Unused argument 'mock_sleep' (unused-argument)
tests/test_cli.py:175:8: W0212: Access to a protected member _realizar_turno of a client class (protected-access)
tests/test_cli.py:166:57: W0613: Unused argument 'mock_input' (unused-argument)
tests/test_cli.py:166:69: W0613: Unused argument 'mock_sleep' (unused-argument)
tests/test_cli.py:6:0: W0611: Unused import time (unused-import)
************* Module test_jugador
tests/test_jugador.py:24:0: C0303: Trailing whitespace (trailing-whitespace)
************* Module test_tablero
tests/test_tablero.py:128:0: C0303: Trailing whitespace (trailing-whitespace)
************* Module test_backgammon
tests/test_backgammon.py:245:82: W0613: Unused argument 'mock_validar' (unused-argument)
tests/test_backgammon.py:313:83: W0613: Unused argument 'mock_validar' (unused-argument)
tests/test_backgammon.py:10:0: R0904: Too many public methods (25/20) (too-many-public-methods)

-----------------------------------
Your code has been rated at 9.33/10


```
