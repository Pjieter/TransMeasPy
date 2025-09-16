import numpy as np
import xarray as xr
from quantify.analysis import base_analysis as ba


class IVAnalysis(ba.BaseAnalysis):
    """Class for analyzing IV measurements."""

    def process_data(self) -> None:
        """Set first measured voltage to zero and calculate the differential resistance.

        Returns:
            _type_: _description_
        """
        self.dataset_processed = xr.Dataset(
            {
                "Voltage": self.dataset.y0.data,
                "dVdI": np.gradient(self.dataset.y0.data, self.dataset.x0.data),
            },
            coords={
                "Current": self.dataset.x0.data,
            },
        )
        self.dataset_processed.Voltage.attrs["Name"] = "Voltage"
        self.dataset_processed.Voltage.attrs["units"] = self.dataset.y0.units
        self.dataset_processed.Voltage.attrs["long_name"] = "Voltage"

        self.dataset_processed.dVdI.attrs["Name"] = "dV/dI"
        self.dataset_processed.dVdI.attrs["long_name"] = "Differential Resistance"
        self.dataset_processed.dVdI.attrs["units"] = "Ohm"

        self.dataset_processed.Current.attrs["Name"] = "Current"
        self.dataset_processed.Current.attrs["long_name"] = "Current"
        self.dataset_processed.Current.attrs["units"] = "A"

    def run_fitting(self) -> None:
        """Run the peak detection of the dV/dI curve using scipy peak finding."""
