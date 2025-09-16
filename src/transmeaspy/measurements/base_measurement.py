from abc import abstractmethod
import quantify.visualization.pyqt_plotmon as pqm
from quantify.data.handling import default_datadir
from quantify.data.handling import set_datadir
from quantify.measurement import MeasurementControl
from quantify.visualization.instrument_monitor import InstrumentMonitor


class BaseMeasurement:
    """Base class for all measurements.

    This class provides the basic parameters for all measurements,
    such as MeasurementControl, InstrumentMonitor, and PlotMon.
    It also provides the basic methods for all measurements,
    such as start, stop, and set_datadir.
    This class is not intended to be used directly,
    but rather as a base class for all measurements.
    """

    # Ignore PLR0913
    def __init__(  # noqa: PLR0913
        self,
        experiment_name: str,
        sample_name: str,
        db_path: str | None = None,
        meas_ctrl: MeasurementControl = None,
        plot_monitor: pqm.PlotMonitor_pyqt = None,
        instrument_monitor: InstrumentMonitor = None,
        live_plot: bool = True,
    ):
        self.experiment_name = experiment_name
        self.sample_name = sample_name
        if db_path is None:
            db_path = default_datadir()
        set_datadir(db_path)
        self.db_path = db_path
        if meas_ctrl is None:
            meas_ctrl = MeasurementControl("meas_ctrl")
        self.meas_ctrl = meas_ctrl
        self.meas_ctrl.update_interval(0.2)
        if live_plot:
            if plot_monitor is None:
                plot_monitor = pqm.PlotMonitor_pyqt("plotmon")
            meas_ctrl.instr_plotmon(plot_monitor.name)
        if instrument_monitor is None:
            instrument_monitor = InstrumentMonitor("InstrumentMonitor")
        self.instrument_monitor = instrument_monitor

    @abstractmethod
    def run(self) -> None:
        """Runs the measurement.

        This method should be implemented by the subclasses.
        """
