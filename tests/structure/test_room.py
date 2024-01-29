from unittest import TestCase
from misc import MeasureFactory
from enumerations import RecordingType
from datatypes.measure import Measure
from enumerations import MeasurementUnit
from measure_instruments.meter import Meter
from structure.open_space import OpenSpace
from enumerations import OpenSpaceType
from enumerations import RoomType
from structure.room import Room
from enumerations import MeterType
from transducer.sensor import Sensor
from enumerations import SensorMeasure
from enumerations import MeasureType
from datatypes.zone import Zone
from enumerations import ZoneType


class TestRoom(TestCase):

    def setUp(self) -> None:
        self.area = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                  Measure(MeasurementUnit.SQUARE_METER, 30))
        self.room = Room(self.area, "Room 145", RoomType.CLASSROOM)

    def test_classroom_with_name_and_area(self):
        self.assertEqual(self.room.room_type, RoomType.CLASSROOM)
        self.assertEqual(self.room.area.value, 30)
        self.assertEqual(self.room.area.measurement_unit, MeasurementUnit.SQUARE_METER)
        self.assertEqual(self.room.name, "Room 145")
        self.assertEqual(self.room.location, "")
        self.assertIsNone(self.room.meter)

    def test_classroom_with_power_meter_with_different_location(self):
        try:
            power_meter = Meter("huz.cab.err", "Honeywell", 5, MeasurementUnit.KILOWATTS, MeterType.POWER)
            self.room.meter = power_meter
        except ValueError as err:
            self.assertEqual(err.__str__(), "what3words location of meter should be the same as room")

    def test_classroom_with_power_meter_and_same_location(self):
        self.room.location = "huz.cab.err"
        power_meter = Meter("huz.cab.err", "Honeywell", 5, MeasurementUnit.KILOWATTS, MeterType.POWER)
        self.room.meter = power_meter
        self.assertEqual(self.room.meter.meter_type, power_meter.meter_type)
        self.assertEqual(self.room.location, power_meter.meter_location)

    def test_classroom_with_adjacent_hall(self):
        hall = OpenSpace(self.area, OpenSpaceType.HALL)
        self.room.add_adjacent_space(hall)
        self.assertEqual(len(self.room.adjacent_spaces), 1)
        self.assertEqual(self.room.adjacent_spaces[0], hall)
        self.assertEqual(self.room.adjacent_spaces[0].space_type, OpenSpaceType.HALL)

    def test_classroom_as_adjacent_room_to_hall(self):
        self.hall = OpenSpace(self.area, OpenSpaceType.HALL)
        self.room.add_adjacent_space(self.hall)
        self.hall.add_adjacent_space(self.room)
        self.assertEqual(self.hall.adjacent_spaces[0], self.room)
        self.assertEqual(self.hall.adjacent_spaces[0].room_type, RoomType.CLASSROOM)

    def test_classroom_with_co2_and_temp_sensors(self):
        co2_sensor = Sensor("Co2_Sensor", SensorMeasure.CARBON_DIOXIDE,
                            MeasurementUnit.PARTS_PER_MILLION, MeasureType.PT_100, 5)
        temp_sensor = Sensor("Temp_Sensor", SensorMeasure.TEMPERATURE,
                             MeasurementUnit.DEGREE_CELSIUS, MeasureType.PT_100, 5)
        self.room.add_transducer(co2_sensor)
        self.room.add_transducer(temp_sensor)
        self.assertEqual(len(self.room.transducers), 2)
        self.assertEqual(self.room.transducers[0].measure, SensorMeasure.CARBON_DIOXIDE)
        self.assertEqual(self.room.transducers[1].measure, SensorMeasure.TEMPERATURE)
        self.assertEqual(self.room.transducers[0].data_frequency, self.room.transducers[1].data_frequency)

    def test_classroom_and_hall_in_the_same_hvac_zone(self):
        hvac_zone = Zone('HVAC ZONE', ZoneType.HVAC)
        hall = OpenSpace(self.area, OpenSpaceType.HALL)
        hall.add_zone(hvac_zone)
        self.room.add_zone(hvac_zone)
        self.assertEqual(self.room.zones[0].zone_type, ZoneType.HVAC)
        self.assertEqual(hall.zones[0], self.room.zones[0])
