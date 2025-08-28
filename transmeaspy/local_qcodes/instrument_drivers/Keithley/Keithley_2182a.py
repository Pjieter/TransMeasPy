############################################################################################################
# This code is based on drivers from QCoDes and the Qcodes-contrib project. This is the driver for the Keithley 2182a nanovoltmeter.
# It uses PyVisa to communicate with the instrument.
# The Keithley 2182a is a nanovoltmeter that can measure voltage from 1nV to 100V. It can also measure temperature with a thermocouple.
# The driver is based on the SCPI commands from the Keithley 2182a manual. The manual can be found here: https://www.tek.com/keithley-source-measure-units/smu-2182a-nanovoltmeter-manual-7
# The driver is tested with a Keithley 2182a nanovoltmeter. The driver should work with other Keithley 2182a nanovoltmeters as well.
############################################################################################################


from __future__ import annotations

import logging
import struct
import sys
import warnings
from enum import Enum
from typing import TYPE_CHECKING, Any, Literal

import qcodes.validators as vals
from qcodes.instrument import (
    Instrument,
    InstrumentChannel,
    VisaInstrument,
    VisaInstrumentKWArgs,
)
from qcodes.parameters import (
    ArrayParameter,
    Parameter,
    ParameterWithSetpoints,
    ParamRawDataType,
    create_on_off_val_mapping,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from qcodes_loop.data.data_set import DataSet
    from typing_extensions import Unpack


if sys.version_info >= (3, 11):
    from enum import StrEnum
else:

    class StrEnum(str, Enum):
        pass


log = logging.getLogger(__name__)


class Keithley2182a(VisaInstrument):
    """
    QCoDeS driver for the Keithley 2182a nanovoltmeter.

    This driver is based on the Keithley 2000 driver from QCoDes and the Keithley 2450 driver from Qcodes-contrib.

    The Keithley 2182a is a nanovoltmeter that can measure voltage from 1nV to 1V. It can also measure temperature with a thermocouple.

    The driver is based on the SCPI commands from the Keithley 2182a manual. The manual can be found here: https://www.tek.com/keithley-source-measure-units/smu-218
    """

    def __init__(self, name: str, address: str, **kwargs: Any) -> None:
        """
        Args:
            name: The name of the instrument used in QCoDeS
            address: The GPIB address of the instrument
        """
        super().__init__(name, address, terminator="\n", **kwargs)

        self.add_parameter(
            "idn",
            get_cmd="*IDN?",
            docstring="Get the identification string of the instrument",
        )

        self.add_parameter(
            "measure",
            label="Measure",
            get_cmd=":SENS:DATA:FRES?",
            get_parser=float,
            docstring="Get the measurement",
            unit="V",
        )

        self.add_parameter(
            "set_measurement_mode",
            label="Set measurement mode",
            set_cmd=":SENS:FUNC: {}",
            get_cmd=":SENS:FUNC?",
            val_mapping={"voltage": '"VOLT:DC"', "temperature": "TEMP"},
            docstring="Set the measurement mode to voltage or temperature",
            initial_value = "voltage"
        )

        self.add_parameter(
            "auto_range",
            label="Auto range",
            get_cmd=":SENS:VOLT:RANG:AUTO?",
            set_cmd=":SENS:VOLT:RANG:AUTO {}",
            val_mapping = create_on_off_val_mapping(on_val="1", off_val="0"),
            docstring="Get or set the auto range setting",
            initial_value = True
        )

        self.add_parameter(
            "range",
            label="Range",
            get_cmd=":SENS:VOLT:RANG?",
            set_cmd=":SENS:VOLT:RANG {}",
            get_parser = float,
            vals=vals.Numbers(1e-7, 100),
            docstring="Get or set the range",
            unit="V",
        )

        self.add_parameter(
            "nplc",
            label="NPLC",
            get_cmd=":SENS:VOLT:NPLC?",
            set_cmd=":SENS:VOLT:NPLC {}",
            get_parser=float,
            vals=vals.Numbers(0.01, 50),
            docstring="Set integration rate in line cycles (PLC); 0.01 to 50",
            initial_value = 1
        )

        self.add_parameter(
            "auto_zero",
            label="Auto zero",
            get_cmd=":SYST:AZER?",
            set_cmd=":SYST:AZER {}",
            val_mapping={True: "1", False: "0"},
            docstring="Get or set the auto zero setting",
        )

        self.add_parameter(
            "clear",
            label="Clear",
            set_cmd="*CLS",
            docstring="Clears all event registers and Error Queue",
        )

        self.add_parameter(
            "reset",
            label="Reset",
            set_cmd="*RST",
            docstring="Returns the 2182 to the *RST default conditions.",
        )

        self.add_parameter(
            "display_enabled",
            label="Display enabled",
            get_cmd=":DISP:ENAB?",
            set_cmd=":DISP:ENAB {}",
            val_mapping=create_on_off_val_mapping(on_val="1", off_val="0"),
            docstring="Get or set the display state",
            initial_value = False
        )

        self.add_parameter(
            "analog_filter_enabled",
            label="Analog filter enabled",
            get_cmd=":SENS:VOLT:LPAS?",
            set_cmd=":SENS:VOLT:LPAS {}",
            val_mapping=create_on_off_val_mapping(on_val="1", off_val="0"),
            docstring="Get or set the analog filter state",
            initial_value = False

        )

        self.add_parameter(
            "channel",
            label="Measurement channel",
            get_cmd=":SENS:CHAN?",
            set_cmd=":SENS:CHAN {}",
            val_mapping={0: "0", 1: "1", 2: "2"},
            docstring="Select channel to measure; 0, 1 or 2 (0 = internal temperature sensor).",
            initial_value = 1
        )

        self.add_parameter(
            "digital_filter",
            label="Digital filter",
            get_cmd=":SENS:VOLT:DFIL?",
            set_cmd=":SENS:VOLT:DFIL {}",
            val_mapping=create_on_off_val_mapping(on_val="1", off_val="0"),
            docstring="Get or set the digital filter state",
            initial_value = False
        )

