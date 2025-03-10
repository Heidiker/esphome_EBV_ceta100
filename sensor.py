import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    UNIT_CELSIUS,
    UNIT_HOUR,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_DURATION,
    ICON_THERMOMETER,
    ICON_TIMER,
    ICON_COUNTER,
    CONF_UPDATE_INTERVAL,
)
from . import Ceta100Sensor, CONF_CETA100_SENSOR_ID

DEPENDENCIES = ["ceta100_sensor"]

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_CETA100_SENSOR_ID): cv.use_id(Ceta100Sensor),
        cv.Optional(CONF_UPDATE_INTERVAL, default="60s"): cv.update_interval,
        cv.Optional("pv_temp"): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            icon=ICON_THERMOMETER,
        ),
        cv.Optional("water_temp"): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            icon=ICON_THERMOMETER,
        ),
        cv.Optional("pump_hours"): sensor.sensor_schema(
            unit_of_measurement=UNIT_HOUR,
            device_class=DEVICE_CLASS_DURATION,
            icon=ICON_TIMER,
        ),
        cv.Optional("pump_starts"): sensor.sensor_schema(
            icon=ICON_COUNTER,
        ),
    }
).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = await cg.get_variable(config[CONF_CETA100_SENSOR_ID])

    # Update-Intervall setzen
    cg.add(var.set_update_interval(config[CONF_UPDATE_INTERVAL]))

    if "pv_temp" in config:
        sens = await sensor.new_sensor(config["pv_temp"])
        cg.add(var.set_pv_temp_sensor(sens))
    
    if "water_temp" in config:
        sens = await sensor.new_sensor(config["water_temp"])
        cg.add(var.set_water_temp_sensor(sens))
    
    if "pump_hours" in config:
        sens = await sensor.new_sensor(config["pump_hours"])
        cg.add(var.set_pump_hours_sensor(sens))

    if "pump_starts" in config:
        sens = await sensor.new_sensor(config["pump_starts"])
        cg.add(var.set_pump_starts_sensor(sens))
