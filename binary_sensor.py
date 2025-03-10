import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import DEVICE_CLASS_RUNNING, CONF_UPDATE_INTERVAL
from . import Ceta100Sensor, CONF_CETA100_SENSOR_ID

DEPENDENCIES = ["ceta100_sensor"]

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_CETA100_SENSOR_ID): cv.use_id(Ceta100Sensor),
        cv.Optional(CONF_UPDATE_INTERVAL, default="60s"): cv.update_interval,
        cv.Optional("burner_mode"): binary_sensor.binary_sensor_schema(
            device_class=DEVICE_CLASS_RUNNING,
        ),
    }
).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = await cg.get_variable(config[CONF_CETA100_SENSOR_ID])

    # Update-Intervall setzen
    cg.add(var.set_update_interval(config[CONF_UPDATE_INTERVAL]))

    if "burner_mode" in config:
        bin_sens = await binary_sensor.new_binary_sensor(config["burner_mode"])
        cg.add(var.set_burner_mode_binary_sensor(bin_sens))
