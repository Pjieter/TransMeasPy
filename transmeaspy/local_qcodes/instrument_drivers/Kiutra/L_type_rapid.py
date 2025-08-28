from time import sleep, time
from qcodes.instrument.base import Instrument
from qcodes.instrument.channel import InstrumentChannel
from qcodes.validators import Numbers
from qcodes.parameters import Parameter

try:
    from kiutra_api.controller_interfaces import (
        TemperatureControl,
        ADRControl,
        MagnetControl,
    )
    from kiutra_api.device_interfaces import Thermometer
except ModuleNotFoundError:
    pass


class TemperatureControlChannel(InstrumentChannel):
    temp_map = {
        "upper_limit": 305,
        "lower_limit": 0.09,
        "middle_point": 3.3,  # Don't change this, if too high, adr control can't handle it
        "high_rate_limit": 5,
        "low_rate_limit": 0.3,
    }

    def __init__(self, parent, name, address) -> None:
        super().__init__(parent, name)
        self.address = address
        self.temperature_controller = TemperatureControl(
            "temperature_control", self.address
        )
        self.adr_controller = ADRControl("adr_control", self.address)
        self.thermometer = Thermometer("T_sample", self.address)
        self.init_current_controller()
        self.is_stable_states = []

        # Add parameters
        self.add_parameter(
            "temperature", get_cmd=self._get_temperature, unit="K", label="Temperature"
        )

        self.add_parameter(
            "setpoint",
            get_cmd=self.get_setpoint,
            set_cmd=lambda sp, rate=0.1: self.set_target_temperature(sp, rate),
            unit="K",
            label="Temperature Setpoint",
        )

        self.add_parameter(
            "is_stable", get_cmd=self.get_is_stable, label="Temperature Stable"
        )

        self.add_parameter(
            "is_ramping", get_cmd=self.get_is_ramping, label="Temperature Ramping"
        )

    def init_current_controller(self):
        if self.temperature_controller.is_active:
            self.current_control = "temperature_control"
        elif self.adr_controller.is_active:
            self.current_control = "adr_control"
        else:
            self.current_control = ""

    def init_stable_states(self):
        # Implement this method if needed
        pass

    def _get_temperature(self):
        return self.thermometer.kelvin

    def set_target_temperature(self, target_temperature, temperature_ramp):
        if (
            target_temperature >= self.temp_map["middle_point"]
            and target_temperature <= self.temp_map["upper_limit"]
        ):
            if self.current_control != "temperature_control":
                while self.adr_controller.is_active:
                    self.adr_controller.stop()
                    sleep(0.1)
                self.current_control = "temperature_control"
                if (
                    temperature_ramp <= self.temp_map["high_rate_limit"]
                    and temperature_ramp > 0
                ):
                    self.temperature_controller.start(
                        (target_temperature, temperature_ramp)
                    )
                    sleep(0.1)
                else:
                    print("Temperature ramping rate might be too large.")
            else:
                if (
                    temperature_ramp <= self.temp_map["high_rate_limit"]
                    and temperature_ramp > 0
                ):
                    self.temperature_controller.start(
                        (target_temperature, temperature_ramp)
                    )
                    sleep(0.1)
                else:
                    print("Temperature ramping rate might be too large.")
        elif (
            target_temperature < self.temp_map["middle_point"]
            and target_temperature >= self.temp_map["lower_limit"]
        ):
            if self.current_control != "adr_control":
                while self.temperature_controller.is_active:
                    self.temperature_controller.stop()
                    sleep(0.1)
                self.current_control = "adr_control"
                if temperature_ramp <= self.temp_map["low_rate_limit"]:
                    self.adr_controller.start_adr(
                        target_temperature, temperature_ramp, operation_mode="cadr"
                    )
                    sleep(0.1)
                else:
                    print(
                        "Temperature ramping rate should be smaller than 0.3 when setting temperature below 3K."
                    )
            else:
                if temperature_ramp <= self.temp_map["low_rate_limit"]:
                    self.adr_controller.start_adr(
                        target_temperature, temperature_ramp, operation_mode="cadr"
                    )
                    sleep(0.1)
                else:
                    print(
                        "Temperature ramping rate should be smaller than 0.3 when setting temperature below 3K."
                    )
        else:
            print("Can't set temperature lower than 0 or higher than 305 K.")
            return False

    def get_is_ramping(self):
        if self.current_control == "temperature_control":
            return self.temperature_controller.ramping
        elif self.current_control == "adr_control":
            return self.adr_controller.ramping
        else:
            print("Temperature control is not initialized.")
            return False

    def wait_for_stable(self):
        self.init_stable_states()
        while not self.get_is_stable():
            sleep(0.1)
            self.init_stable_states()

    def get_setpoint(self):
        if self.current_control == "temperature_control":
            return self.temperature_controller.setpoint
        elif self.current_control == "adr_control":
            return self.adr_controller.setpoint
        else:
            print("Temperature control is not initialized.")
            return 0

    def get_is_stable(self):
        if self.current_control == "temperature_control":
            return self.temperature_controller.stable
        elif self.current_control == "adr_control":
            return self.adr_controller.stable
        else:
            print("Temperature control is not initialized.")
            return False

    def abort_ramping(self):
        self.temperature_controller.stop()
        self.adr_controller.stop()
        self.current_control = ""

    def disconnect(self):
        pass

    def get_ramping_info(self):
        """
        Returns dictionary containing information about any ongoing ramp or temperature control process.

        """
        return self.call_method("get_ramping_info")

    def recharge(self):
        """
        Start adr recharging.

        """
        return self.call_method("recharge")

    def cooldown(self):
        """
        Cooldown to bath temperature if temperature is above bath temperature.

        """
        return self.call_method("cooldown")

    def start_single_adr(
        self,
        setpoint: float,
        ramp: float,
        start_temperature: float = None,
        setup_speed: float = None,
        init_hold: float = 0.0,
        pre_regenerate: bool = True,
    ):
        """
        Smooth single shot using only last adr-stage for seamless operation.

        Args:
            setpoint: temperature setpoint in K
            ramp: target temperature ramp in K/min
            start_temperature: start temperature in K (optional)
            setup_speed: ramp in K/min to approach start temperature if specified (optional)
            init_hold: time to wait at start temperature in s (optional)
            pre_regenerate: regenerate befor starting?

        Returns:

        """
        raise self.call_method(
            "start_single_adr",
            setpoint=setpoint,
            ramp=ramp,
            start_temperature=start_temperature,
            setup_speed=setup_speed,
            init_hold=init_hold,
            pre_regenerate=pre_regenerate,
        )

    def start_serial_adr(
        self,
        setpoint: float,
        ramp: float,
        start_temperature: float = None,
        pre_regenerate: bool = True,
        setup_speed: float = None,
        init_hold: float = 0.0,
    ):
        raise self.call_method(
            "start_serial_adr",
            setpoint=setpoint,
            ramp=ramp,
            start_temperature=start_temperature,
            setup_speed=setup_speed,
            init_hold=init_hold,
            pre_regenerate=pre_regenerate,
        )

    def start_cadr(
        self,
        setpoint: float,
        ramp: float,
        start_temperature: float = None,
        pre_regenerate: bool = True,
        setup_speed: float = None,
        init_hold: float = 0.0,
    ):
        """
        Start countinuous adr operation.
        """
        raise self.call_method(
            "start_cadr",
            setpoint=setpoint,
            ramp=ramp,
            start_temperature=start_temperature,
            pre_regenerate=pre_regenerate,
            setup_speed=setup_speed,
            init_hold=init_hold,
        )

    def start_heater_control(
        self,
        setpoint: float,
        ramp: float,
        start_temperature: float = None,
        setup_speed: float = None,
        init_hold: float = 0,
    ):
        """
        Heater only control aplicable above bath temperature.

        Args:
            setpoint: setpoint temperature to control [K]
            ramp: temperature ramp to control [K/min]
            start_temperature:
            setup_speed:
            init_hold:

        Returns:

        """
        raise self.call_method(
            "start_heater_control",
            setpoint=setpoint,
            ramp=ramp,
            start_temperature=start_temperature,
            setup_speed=setup_speed,
            init_hold=init_hold,
        )

    def propose_control_mode(
        self,
        setpoint: float,
        ramp: float,
        mode: str = "ramp",
        start_temperature: float = None,
    ):
        """
        Returns a proposed control mode based on the given parameters.

        Args:
            setpoint: setpoint temperature to control [K]
            ramp: temperature ramp to control [K/min]
            mode: Prioritization mode (ramp/stabilize).
            start_temperature:

        Returns:

        """
        return self.call_method(
            "propose_control_mode",
            setpoint=setpoint,
            ramp=ramp,
            mode=mode,
            start_temperature=start_temperature,
        )

    def start_proposed_mode(
        self,
        setpoint: float,
        ramp: float,
        mode: str = "ramp",
        start_temperature: float = None,
    ):
        """
        Returns the proposed control mode based on the given parameters.

        Args:
            setpoint: setpoint temperature to control [K]
            ramp: temperature ramp to control [K/min]
            mode: Prioritization mode (ramp/stabilize).
            start_temperature:

        Returns:

        """
        return self.call_method(
            "start_proposed_mode",
            setpoint=setpoint,
            ramp=ramp,
            mode=mode,
            start_temperature=start_temperature,
        )

    def return_to_idle(self, *args, **kwargs):
        """
        Resets or activates components of the controller to solve potential issues.

        Args:
            *args:
            **kwargs:

        Returns:

        """
        self.call_method("return_to_idle")


class MagnetControlChannel(InstrumentChannel):
    field_maps = {
        10: {
            "upper": 5,
            "lower": -5,
            "upper ramp": 0.5,
        }
    }

    def __init__(self, parent, name, address):
        super().__init__(parent, name)
        self.address = address
        self.magnet_controller = MagnetControl("sample_magnet", self.address)
        self.thermometer = Thermometer("T_sample", self.address)

        # Add parameters
        self.add_parameter(
            "field", get_cmd=self._get_field, unit="T", label="Magnetic Field"
        )

        self.add_parameter(
            "target_field",
            set_cmd=lambda value, rate=0.1: self.set_target_field(value, rate),
            get_cmd=lambda: (
                self.magnet_controller.setpoint
                if hasattr(self.magnet_controller, "setpoint")
                else 0
            ),
            unit="T",
            label="Target Field",
        )

        self.add_parameter(
            "is_stable",
            get_cmd=lambda: self.magnet_controller.stable,
            label="Field Stable",
        )

    def _get_field(self):
        return self.magnet_controller.field

    def set_target_field(self, target_field, field_ramp):
        self.current_temperature = self.thermometer.kelvin
        if self.current_temperature < 200:
            self.magnet_controller.start((target_field, field_ramp))
            return True
        else:
            print(r"Temperature is too high to apply magnetic field!")
            return False

    def abort_ramping(self):
        self.magnet_controller.stop()


class L_type_rapid(Instrument):
    """
    Qcodes driver for the Kiutra L-type Rapid cryostat.
    """

    def __init__(self, name, address, **kwargs):
        super().__init__(name, **kwargs)
        self.address = address

        self.add_submodule(
            "temperature_control",
            TemperatureControlChannel(self, "temperature_control", address),
        )

        self.add_submodule(
            "magnet_control", MagnetControlChannel(self, "magnet_control", address)
        )

    def get_idn(self) -> dict:
        """
        Returns the VISA ID string of the instrument. Got these values manually from the kiutra control computer.
        """
        idn = {
            "vendor": "Kiutra",
            "model": "L-type Rapid",
            "serial": "unknown",
            "firmware": "20240422_113925 (2024-04-22_17-14_v2_0_51_beta)",
        }
        return idn
