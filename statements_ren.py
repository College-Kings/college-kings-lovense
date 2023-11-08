from typing import Callable, Optional

from renpy.lexer import Lexer
import renpy.exports as renpy

from game.lovense.LovenseAction_ren import LovenseAction
from game.lovense.Lovense_ren import Lovense

path_builder: bool
lovense = Lovense()

"""renpy
python early:
"""


def parse_lovense(lexer: Lexer) -> tuple[str, str]:
    action: Optional[str] = lexer.name()

    if not action:
        renpy.error("Expected action name.")  # type: ignore

    if action == "stop":
        return (action, "0")

    strength = lexer.simple_expression()

    if not strength:
        renpy.error("Expected strength.")  # type: ignore

    return (action, strength)  # type: ignore


def lint_lovense(lovense_expr: tuple[str, str]) -> None:
    action: str = lovense_expr[0]
    try:
        action_func = getattr(lovense, action)
    except AttributeError:
        renpy.error(f"Unrecognized lovense action '{action}'. Please check if the action name is correct and supported.")  # type: ignore
        return

    if not callable(action_func):
        renpy.error(f"The lovense action '{action}' is not a function. Please ensure that it is a valid callable action.")  # type: ignore
        return

    if action == "stop":
        return

    try:
        strength = eval(lovense_expr[1])
    except (SyntaxError, NameError, TypeError) as e:
        renpy.error(f"The strength expression '{lovense_expr[1]}' could not be evaluated due to an error: {e}")  # type: ignore
        return

    if not isinstance(strength, int):
        renpy.error(f"The lovense strength value '{strength}' is not an integer. Strength values must be integer types.")  # type: ignore
        return

    if strength < 0:
        renpy.error(f"The lovense strength value '{strength}' is negative. Strength values must be non-negative integers.")  # type: ignore
        return

    max_strength = Lovense.MAX_STRENGTHS.get(LovenseAction[action.upper()], None)
    if max_strength is None:
        renpy.error(f"The action '{action}' is not associated with a maximum strength value in 'Lovense.MAX_STRENGTHS'.")  # type: ignore
        return

    if strength > max_strength:
        renpy.error(f"The strength '{strength}' exceeds the maximum allowed strength of '{max_strength}' for the action '{action}'.")  # type: ignore
        return


def execute_lovense(lovense_expr: tuple[str, str]) -> None:
    action: str = lovense_expr[0]
    strength: int = eval(lovense_expr[1])

    f: Callable[..., None] = getattr(lovense, action)

    if action == "stop":
        f()
    else:
        f(strength)

    return


renpy.register_statement(  # type: ignore
    name="lovense",
    parse=parse_lovense,
    lint=lint_lovense,
    execute=execute_lovense,
)
