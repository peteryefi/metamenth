import uuid
from datatypes import BinaryMeasure
from structure import Material


class Layer:
    def __init__(
        self,
        thermal_resistance: BinaryMeasure,
        height: BinaryMeasure,
        length: BinaryMeasure,
        thickness: BinaryMeasure,
        solar_heat_gain_coefficient: float,
        material: Material,
        has_vapour_barrier: bool = False,
        has_air_barrier: bool = False,

    ):
        self.UID = str(uuid.uuid4())  # Generate a unique identifier
        self.thermal_resistance = thermal_resistance
        self.height = height
        self.length = length
        self.thickness = thickness
        self.solar_heat_gain_coefficient = self.validate_solar_heat_gain_coefficient(solar_heat_gain_coefficient)
        self.has_vapour_barrier = has_vapour_barrier
        self.has_air_barrier = has_air_barrier
        self.material = material

    def validate_solar_heat_gain_coefficient(self, value):
        if 0 <= value <= 1:
            return value
        else:
            raise ValueError("Solar Heat Gain Coefficient must be a float between 0 and 1.")

    def __str__(self):
        material_str = f"Material: {str(self.material)}" if self.material else "Material: None"
        return (
            f"Layer("
            f"UID: {self.UID}, "
            f"Thermal Resistance: {self.thermal_resistance.value} {self.thermal_resistance.measurement_unit}, "
            f"Height: {self.height.value} {self.height.measurement_unit}, "
            f"Length: {self.length.value} {self.length.measurement_unit}, "
            f"Thickness: {self.thickness.value} {self.thickness.measurement_unit}, "
            f"Solar Heat Gain Coefficient: {self.solar_heat_gain_coefficient}, "
            f"Vapour Barrier: {self.has_vapour_barrier}, "
            f"Air Barrier: {self.has_air_barrier}, "
            f"{material_str})"
        )