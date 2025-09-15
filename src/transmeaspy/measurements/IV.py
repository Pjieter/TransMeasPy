from pathlib import Path
import string
import numpy as np

import qcodes as qc

## Multidimensional scanning module
from qcodes.dataset import (
    LinSweep,
    Measurement,
    ThreadPoolParamsCaller,
    dond,
    experiments,
    initialise_or_create_database_at,
    load_by_run_spec,
    load_or_create_experiment,
    plot_dataset,
)

from qcodes.station import Station

qcodes_contrib_drivers.drivers.QuTech.IVVI.IVVI

from qcodes.instrument.base import Instrument
from qcodes.instrument.parameter import Parameter

## Using interactive widget
from qcodes.interactive_widget import experiments_widget

import IPython.lib.backgroundjobs as bg
from local_qcodes.measurements import BaseMeasurement
from plottr.apps import inspectr

from qcodes_contrib_drivers.drivers.QuTech.IVVI import IVVI
from zhinst.qcodes import MFLI
from local_qcodes.instrument_drivers.Keithley.Keithley_2182a import Keithley2182a
from local_qcodes.utilities import utilities


import numpy as np

import quantify_core.visualization.pyqt_plotmon as pqm
from quantify_core.analysis import base_analysis as ba
from quantify_core.analysis import cosine_analysis as ca

from quantify_core.measurement import MeasurementControl
from quantify_core.visualization.instrument_monitor import InstrumentMonitor


class IV_measurement(BaseMeasurement):
    """
    IV measurement class for QCoDeS
    """

    def __init__(
        self,
        experiment_name: str,
        sample_name: str,
        current_supply: Parameter,
        voltage_meter: Keithley2182a,
        db_path: str | None = None,
        meas_ctrl: MeasurementControl | None = None,
        plot_monitor: pqm.PlotMon | None = None,
        instrument_monitor: InstrumentMonitor | None = None,
        live_plot: bool = True,
    ):
        """
        Initialize the IV measurement class
        """

        super().__init__(
            experiment_name,
            sample_name,
            db_path=db_path,
            meas_ctrl=meas_ctrl,
            plot_monitor=plot_monitor,
            instrument_monitor=instrument_monitor,
            live_plot=live_plot,
        )
        self.current_source = current_supply
        self.voltage_meter = voltage_meter

    def run(
        self,
        start: float,
        stop: float,
        num_points: int,
        delay: float = 0.05,
    ):
        """
        Run the IV measurement.
        This method performs a linear sweep of the current source from start to stop,

        Args:
            start (float): Start current value.
            stop (float): Stop current value. Includes the stop value in the measurement.
            num_points (int): Number of points in the sweep.
            delay (float, optional): _description_. Defaults to 0.01.
        """
        if isinstance(self.current_source.instrument, IVVI):
            setpoints = self.current_source.instrument.linspace(start, stop, num_points)
            self.current_source.instrument.dac_delay(delay)
        else:
            setpoints = np.linspace(start, stop, num_points)
        self.meas_ctrl.settables(self.current_source)
        self.meas_ctrl.setpoints(setpoints)
        self.meas_ctrl.gettables(self.voltage_meter.measure)

        dataset = self.meas_ctrl.run()

        analysis = ba.BaseAnalysis(
            dataset=dataset, label=f"{self.sample_name}-{self.experiment_name}"
        )
        return analysis.run()
