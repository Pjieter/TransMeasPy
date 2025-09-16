import numpy as np

## Multidimensional scanning module
import quantify.visualization.pyqt_plotmon as pqm
from qcodes.instrument.parameter import Parameter
from qcodes_contrib_drivers.drivers.QuTech.IVVI import IVVI
from quantify.analysis import base_analysis as ba
from quantify.measurement import MeasurementControl
from quantify.visualization.instrument_monitor import InstrumentMonitor
from transmeaspy.measurements import base_measurement


class IVMeasurement(base_measurement):
    """IV measurement class for QCoDeS."""

    # Ignore PLR0913
    def __init__(  # noqa: PLR0913
        self,
        experiment_name: str,
        sample_name: str,
        current_supply: Parameter,
        voltage_meter: Parameter,
        db_path: str | None = None,
        meas_ctrl: MeasurementControl | None = None,
        plot_monitor: pqm.PlotMon | None = None,
        instrument_monitor: InstrumentMonitor | None = None,
        live_plot: bool = True,
    ):
        """Initialize the IV measurement class."""
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
    ) -> ba.BaseAnalysis:
        """Runs the IV measurement.

        This method performs a linear sweep of the current source from start to stop.

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
            dataset=dataset,
            label=f"{self.sample_name}-{self.experiment_name}",
        )
        return analysis.run()
