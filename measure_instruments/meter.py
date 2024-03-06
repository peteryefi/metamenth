import uuid
from enumerations import MeterType
from enumerations import MeasurementUnit
from enumerations import MeterMeasureMode
from measure_instruments import MeterMeasure
from enumerations import MeterAccumulationFrequency
from misc import Validate


class Meter:
    """
    A representation of a meter

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, meter_location: str, measurement_frequency: float,
                 measurement_unit: MeasurementUnit, meter_type: MeterType,
                 measure_mode: MeterMeasureMode, data_accumulated: bool = False,
                 accumulation_frequency: MeterAccumulationFrequency = MeterAccumulationFrequency.NONE,
                 manufacturer: str = None):
        """
        Initializes a Meter instance.

        :param meter_location: The what3word location of the meter.
        :param manufacturer: The manufacturer of the meter.
        :param measurement_frequency: The measurement frequency of the meter.
        :param measurement_unit: The measurement unit of the meter data.
        :param meter_type: The type of the meter.
        :param measure_mode: the data measure mode: manual or automatic
        :param data_accumulated: indicate whether the data is accumulate or not
        :param accumulation_frequency: the frequency at which data is accumulated
        """
        self._UID = str(uuid.uuid4())
        self._meter_location = Validate.validate_what3word(meter_location)
        self._manufacturer = None
        self._measurement_frequency = None
        self._meter_type = None
        self._meter_measures: [MeterMeasure] = []
        self._measurement_unit = None
        self._measure_mode = None
        self._data_accumulated = data_accumulated
        self._accumulation_frequency = MeterAccumulationFrequency.NONE

        # Apply validation
        self.manufacturer = manufacturer
        self.measurement_frequency = measurement_frequency
        self.measurement_unit = measurement_unit
        self.meter_type = meter_type
        self.measure_mode = measure_mode
        self.accumulation_frequency = accumulation_frequency

    @property
    def meter_location(self):
        return self._meter_location

    @meter_location.setter
    def meter_location(self, value):
        self._meter_location = Validate.validate_what3word(value)

    @property
    def UID(self):
        return self._UID

    @property
    def manufacturer(self) -> str:
        return self._manufacturer

    @manufacturer.setter
    def manufacturer(self, value: str):
        self._manufacturer = value

    @property
    def measurement_frequency(self) -> float:
        return self._measurement_frequency

    @measurement_frequency.setter
    def measurement_frequency(self, value: float):
        if value is not None:
            self._measurement_frequency = value
        else:
            raise ValueError("measurement_frequency must be a float")

    @property
    def measure_mode(self) -> MeterMeasureMode:
        return self._measure_mode

    @measure_mode.setter
    def measure_mode(self, value: MeterMeasureMode):
        if value is not None:
            self._measure_mode = value
        else:
            raise ValueError("measure_mode must be a float")

    @property
    def data_accumulated(self) -> bool:
        return self._data_accumulated

    @data_accumulated.setter
    def data_accumulated(self, value: bool):
        if value is not None:
            self._data_accumulated = value
        else:
            raise ValueError("data_accumulated must be a boolean")

    @property
    def accumulation_frequency(self) -> MeterAccumulationFrequency:
        return self._accumulation_frequency

    @accumulation_frequency.setter
    def accumulation_frequency(self, value: MeterAccumulationFrequency):
        if value is not None:
            if self.data_accumulated and value is None:
                raise ValueError("accumulation_frequency must not be None")
            else:
                self._accumulation_frequency = value
        else:
            raise ValueError("data_accumulated must be a boolean")

    @property
    def measurement_unit(self) -> MeasurementUnit:
        return self._measurement_unit

    @measurement_unit.setter
    def measurement_unit(self, value: MeasurementUnit):
        if value is not None:
            self._measurement_unit = value
        else:
            raise ValueError("Measurement unit must be of type MeasurementUnit")

    @property
    def meter_type(self) -> MeterType:
        return self._meter_type

    @meter_type.setter
    def meter_type(self, value: MeterType):
        if value is not None:
            self._meter_type = value
        else:
            raise ValueError("Meter type must be of type MeterType")

    @property
    def meter_measures(self) -> [MeterMeasure]:
        return self._meter_measures

    def add_meter_measure(self, value: float):
        """
        Add measurement for this meter
        :param value: The numerical value of the meter measure.
        """
        meter_measure = MeterMeasure(value)
        self._meter_measures.append(meter_measure)

    def __eq__(self, other):
        # Meters are equal if they share the same UID
        if isinstance(other, Meter):
            # Check for equality based on the 'UID' attribute
            return self.UID == other.UID
        return False

    def __str__(self):
        """
        :return: A formatted string representing the meter.
        """
        meter_details = (f"Meter (UID: {self.UID}, Location: {self.meter_location}, "
                         f"Manufacturer: {self.manufacturer}, Frequency: {self.measurement_frequency}, "
                         f"Unit: {self.measurement_unit.name}, Type: {self.meter_type.name}, "
                         f"Measure Mode: {self.measure_mode}, Data Accumulated: {self.data_accumulated}, "
                         f"Accumulation Frequency: {self.accumulation_frequency})")

        measurements = "\n".join(str(measure) for measure in self.meter_measures)

        return f"{meter_details}\nMeasurements:\n{measurements}"
