import json
import logging
from pathlib import Path
from typing import Tuple

import lmfit
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import quantify_core.visualization.pyqt_plotmon as pqm
from quantify_core.analysis import base_analysis as ba
from quantify_core.data.handling import (
    default_datadir,
    get_latest_tuid,
    load_dataset,
    locate_experiment_container,
    set_datadir,
)
from quantify_core.measurement import MeasurementControl
from quantify_core.utilities.examples_support import mk_cosine_instrument
from quantify_core.utilities.inspect_utils import display_source_code
from quantify_core.visualization.SI_utilities import set_xlabel, set_ylabel


class IVAnalysis(ba.BaseAnalysis):
    """
    Class for analyzing IV measurements.
    """

    def process_data(self):
        """
        Set first measured voltage to zero and calculate the differential resistance.

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

    def run_fitting(self):
        """
        Run the peak detection of the dV/dI curve using scipy peak finding.
        """
        pass
