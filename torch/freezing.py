from torch import nn as nn


def set_frozen(model: nn.Module, freeze: bool) -> None:
    """
    Freeze or unfreeze all parameters of the given model.
    :param freeze: freeze parameters if `True` or unfreeze if `False.
    """
    for param in model.parameters():
        param.requires_grad = not freeze


def get_unfrozen_params(model: nn.Module) -> list[nn.Parameter]:
    """
    Return all unfrozen parameters of the model.
    """
    return [p for p in model.parameters() if p.requires_grad]


def count_unfrozen_params(model: nn.Module) -> int:
    """Count model parameters with requires_grad set to True"""
    return sum(p.numel() for p in get_unfrozen_params(model))
