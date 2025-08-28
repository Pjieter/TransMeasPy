from local_qcodes.instrument_drivers.Keithley.Keithley_2182a import Keithley2182a


import logging

import numpy as np
import pytest
from pytest import LogCaptureFixture

from .....local_qcodes.instrument_drivers.Keithley.Keithley_2182a import Keithley2182a


@pytest.fixture(scope="function")
def k2128a():
    """
    Create a Keithley 2182a instrument
    """
    driver = Keithley2182a(
        "k2182aA", address="GPIB::2::INSTR", pyvisa_sim_file="Keithley_2182a.yaml"
    )
    yield driver
    driver.close()


def test_wrong_mode(caplog: LogCaptureFixture) -> None:
    """
    Starting an instrument in the wrong mode should result in a warning. Additionally, no
    parameters should be available, other then the parameters "IDN" and "timeout" which
    are created by the Instrument and VisaInstrument parent classes
    """
    with caplog.at_level(logging.WARNING):
        instrument = Keithley2182a(
            "wrong_mode",
            address="GPIB::1::INSTR",
            pyvisa_sim_file="Keithley_2182a.yaml",
        )
        assert "The instrument is in an unsupported language mode." in caplog.text
        assert list(instrument.parameters.keys()) == ["IDN", "timeout"]
        instrument.close()


def test_sense_current_mode(k2128a) -> None:
    """
    Test that when we are in a sense function, for example, 'current', that
    the sense property is returning to the correct submodule. We also test
    that if we are in a sense function (e.g. 'current') the returned submodule
    does not have inappropriate parameters, (e.g. 'voltage', or 'current')
    """
    sense_functions = {"current", "voltage", "resistance"}
    for sense_function in sense_functions:
        k2128a.sense.function(sense_function)
        assert k2128a.sense is k2128a.submodules[f"_sense_{sense_function}"]
        assert hasattr(k2128a.sense, sense_function)

        for other_sense_function in sense_functions.difference({sense_function}):
            assert not hasattr(k2128a.sense, other_sense_function)


def test_setpoint_always_follows_source_function(k2128a) -> None:
    """
    Changing the source and/or sense functions should not confuse the setpoints. These
    should always follow the source module
    """
    n = 100
    sense_modes = np.random.choice(["current", "voltage", "resistance"], n)
    source_modes = np.random.choice(["current", "voltage"], n)

    for sense_mode, source_mode in zip(sense_modes, source_modes):
        k2128a.sense.function("voltage")  # In 'resistance' sense mode, we cannot
        # change the source mode by design. Therefore temporarily switch to
        # 'voltage'
        k2128a.source.function(source_mode)
        k2128a.sense.function(sense_mode)
        assert k2128a.sense.sweep.setpoints == (k2128a.source.sweep_axis,)


def test_reset_sweep_on_source_change(k2128a) -> None:
    """
    If we change the source function, we need to run the sweep setup again
    """
    # first set sense to a mode where we are allowed to change source
    k2128a.sense.function("current")
    k2128a.source.function("voltage")
    k2128a.source.sweep_setup(0, 1, 10)
    assert np.all(k2128a.source.get_sweep_axis() == np.linspace(0, 1, 10))

    k2128a.source.function("current")
    with pytest.raises(ValueError):
        k2128a.source.get_sweep_axis()


def test_sweep(k2128a) -> None:
    """
    Verify that we can start sweeps
    """
    k2128a.sense.function("current")
    k2128a.source.function("voltage")
    k2128a.source.sweep_setup(0, 1, 10)
    k2128a.sense.sweep.get()


def test_Keithley_2182a():
    names = [None, "test"]
