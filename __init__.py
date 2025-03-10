import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_UPDATE_INTERVAL
from esphome.components import uart

DEPENDENCIES = ["uart"]

MULTI_CONF = True

ceta100_sensor_ns = cg.esphome_ns.namespace("ceta100_sensor")
Ceta100Sensor = ceta100_sensor_ns.class_("Ceta100Sensor", cg.PollingComponent, uart.UARTDevice)

CONF_CETA100_SENSOR_ID = "ceta100_sensor_id"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(Ceta100Sensor),
        cv.Required("uart_id"): cv.use_id(uart.UARTComponent),
        cv.Optional(CONF_UPDATE_INTERVAL, default="60s"): cv.update_interval,
    }
).extend(cv.COMPONENT_SCHEMA).extend(uart.UART_DEVICE_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)
    
    # Update-Intervall setzen
    cg.add(var.set_update_interval(config[CONF_UPDATE_INTERVAL]))
