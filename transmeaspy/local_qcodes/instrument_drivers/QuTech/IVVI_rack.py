# Instrument driver for the IVVI rack from QuTech, documentation can be found at: https://qtwork.tudelft.nl/~schouten/ivvi/index-ivvi.htm


from typing import Any
from qcodes.instrument import Instrument, InstrumentChannel
from qcodes.parameters import ManualParameter, Parameter, DelegateParameter
from qcodes.utils.validators import Numbers, Enum, Validator


class S0(InstrumentChannel):
    """
    Galvanic isolation module with 2 channels in the IVVI rack.

    Args:
        Instrument (_type_): _description_
    """

    def __init__(self, parent: Instrument, name: str, **kwargs):
        super().__init__(parent, name, **kwargs)

        self.add_submodule("channel1", S0Channel(self, "channel1", scaling_factor=1.0))
        self.add_submodule("channel2", S0Channel(self, "channel2", scaling_factor=0.01))


class S0Channel(InstrumentChannel):
    """
    A channel for the S0C module in the IVVI rack.
    """

    def __init__(
        self, parent: Instrument, name: str, scaling_factor: float = 1.0
    ) -> None:
        super().__init__(parent, name)
        self._scaling_factor = scaling_factor

        self.add_parameter(
            "bandwith",
            label="Bandwith",
            unit="Hz",
            initial_value=1000,
            parameter_class=ManualParameter,
            vals=Numbers(1000, 10000),
        )

        self.add_parameter(
            "output",
            label="Output",
            parameter_class=ManualParameter,
            unit="V",
            get_cmd=self._get_output,
        )

        self.add_parameter(
            "input",
            label="Input",
            parameter_class=ManualParameter,
            vals=Numbers(-1, 1),
            unit="V",
        )

    def _get_output(self):
        return self.input() * self._scaling_factor


class OutputValidator(Validator[float]):
    """
    Validator for the output parameter of the S4C module.
    Ensures that the output value is within the range of -1 to 1.
    """

    def __init__(self, instrument: Instrument):
        self.instrument = instrument
        self._scale = None

    def validate(self, value: float, context: str = "") -> None:
        scale = self._scale

        if isinstance(self.instrument, S4C):
            scale = self.instrument.range()
        validator = Numbers(-1 * scale, 1 * scale)
        validator.validate(value)


class S4C(InstrumentChannel):
    """
    S4C: Current/Voltage source module for the IVVI rack.
    Documentation: https://qtwork.tudelft.nl/~schouten/ivvi/doc-mod/docs4c.htm

    This module takes its input from one of the S0 channels depending on its slot:
    - Slot 2 is connected to S0 channel 1
    - Slot 3 is connected to S0 channel 2 and is also connected to dac1
    """

    def __init__(self, parent, name, **kwargs):
        super().__init__(parent, name, **kwargs)

        self.add_parameter(
            "slot",
            label="Slot",
            parameter_class=ManualParameter,
            initial_value=None,
            vals=Numbers(2, 3),
        )

        # Add parameters
        self.add_parameter(
            "output_mode",
            label="Output Mode",
            parameter_class=ManualParameter,
            initial_value="symmetric",
            vals=Enum("single", "symmetric"),
            docstring="Output mode: single (pin 2 at ground) or symmetric (pin 2 at -V)",
        )

        self.add_parameter(
            "range",
            label="Range",
            parameter_class=ManualParameter,
            initial_value=1e-6,
            vals=Enum(1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 2e-3),
            docstring="Range selection, For I mode: A/V, For V mode: V with current limit 3x range, For V+R mode: V output resistance 1/range Ohms",
        )

        self.add_parameter(
            "source_mode",
            label="Source Mode",
            parameter_class=ManualParameter,
            initial_value="I",
            vals=Enum("I", "V", "V+R"),
            docstring="Operation mode: current (I), voltage (V) or voltage with output resistance (V+R)",
        )

        self.add_parameter(
            "output",
            label="Output",
            unit=self._get_unit,
            set_cmd=self._set_input,
            docstring="Output current or voltage depending on mode",
            vals=OutputValidator(self),
        )

        # self.add_parameter(
        #     "input",
        #     label="Input",
        #     get_cmd=self._set_input,
        #     vals=Numbers(-1, 1),
        #     unit="V",
        # )

    def _get_unit(self):
        """
        Returns the unit of the output parameter based on the source mode.
        """
        if self.source_mode() == "I":
            return "A"
        elif self.source_mode() == "V":
            return "V"
        elif self.source_mode() == "V+R":
            return "V"
        else:
            raise ValueError("Unknown source mode: {}".format(self.source_mode()))

    def _set_input(self, value: float) -> None:
        """
        Sets the wanted input value to achieve the desired output.

        """
        # value = self.output()
        source_mode = self.source_mode()
        range_scale = self.range()
        if source_mode == "I":
            # For current mode, the input is the current in Amperes
            return value / range_scale
        elif source_mode == "V":
            # For voltage mode, the input is the voltage in Volts
            return value
        elif source_mode == "V+R":
            # For voltage with output resistance mode, the input is the voltage in Volts
            return value
        else:
            raise ValueError(f"Unknown source mode: {source_mode}")


class IVVIRack(Instrument):
    """
    Instrument driver for the IVVI rack from QuTech.

    Args:
        name: The name of the instrument used in QCoDeS
        address: The GPIB address of the instrument
    """

    def __init__(self, name: str, **kwargs: Any):
        super().__init__(name, **kwargs)

        # self.add_submodule("s0", S0(parent=self, name="s0"))
        self.add_submodule("s4c", S4C(parent=self, name="s4c"))
