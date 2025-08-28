from qcodes_contrib_drivers.drivers.QuTech.IVVI import IVVI
from zhinst.qcodes import MFLI
from qcodes.parameters import Parameter


def _get_current_source(current_supply: MFLI | IVVI) -> Parameter:
    """
    Get the current source parameter to set and get for the current supply

    Args:
        current_supply (MFLI | IVVI): _description_

    Returns:
        Parameter: _description_
    """
