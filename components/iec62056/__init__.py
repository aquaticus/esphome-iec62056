# components/iec62056/__init__.py
import re

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID, CONF_UPDATE_INTERVAL

AUTO_LOAD = ["uart"]
MULTI_CONF = True

iec62056_ns = cg.esphome_ns.namespace("iec62056")
IEC62056Component = iec62056_ns.class_(
    "IEC62056Component", cg.PollingComponent, uart.UARTDevice
)

# ---- Ключи/константы, которые импортируют sensor.py и text_sensor.py ----
CONF_IEC62056_ID = "iec62056_id"
CONF_OBIS = "obis"

# ---- Опции компонента ----
CONF_BAUD_RATE_MAX = "baud_rate_max"
CONF_FORCE_BAUD_RATE = "force_baud_rate"               # фиксированная скорость
CONF_DECREASE_BAUD_ON_RETRY = "decrease_baud_on_retry"  # запрет дауншифта
CONF_BATTERY_METER = "battery_meter"
CONF_CONNECTION_TIMEOUT = "connection_timeout"
CONF_MAX_RETRIES = "max_retries"
CONF_RETRY_DELAY = "retry_delay"
CONF_MODE_D = "mode_d"

# Проверка формата OBIS (например: 1.8.0, 12.7.0, 0.9.1)
def validate_obis(value):
    s = cv.string(value)
    if not re.match(r"^\d+(?:\.\d+){2,}$", s):
        raise cv.Invalid("OBIS должен быть в формате 'X.Y.Z' (например, 1.8.0)")
    return s

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(IEC62056Component),
        cv.Optional(CONF_UPDATE_INTERVAL, default="67s"): cv.positive_time_period_milliseconds,
        cv.Optional(CONF_CONNECTION_TIMEOUT, default="7s"): cv.positive_time_period_milliseconds,
        cv.Optional(CONF_BAUD_RATE_MAX, default=9600): cv.int_range(min=1200, max=9600),
        cv.Optional(CONF_FORCE_BAUD_RATE, default=0): cv.int_range(min=0, max=9600),
        cv.Optional(CONF_DECREASE_BAUD_ON_RETRY, default=True): cv.boolean,
        cv.Optional(CONF_BATTERY_METER, default=False): cv.boolean,
        cv.Optional(CONF_MAX_RETRIES, default=3): cv.uint8_t,
        cv.Optional(CONF_RETRY_DELAY, default="3s"): cv.positive_time_period_milliseconds,
        cv.Optional(CONF_MODE_D, default=False): cv.boolean,
    }
).extend(uart.UART_DEVICE_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    cg.add(var.set_update_interval(config[CONF_UPDATE_INTERVAL].total_milliseconds))
    cg.add(var.set_connection_timeout(config[CONF_CONNECTION_TIMEOUT].total_milliseconds))
    cg.add(var.set_baud_rate_max(config[CONF_BAUD_RATE_MAX]))
    cg.add(var.set_battery_meter(config[CONF_BATTERY_METER]))
    cg.add(var.set_max_retries(config[CONF_MAX_RETRIES]))
    cg.add(var.set_retry_delay(config[CONF_RETRY_DELAY].total_milliseconds))
    cg.add(var.set_force_mode_d(config[CONF_MODE_D]))

    # Новые опции
    cg.add(var.set_force_baud_rate(config[CONF_FORCE_BAUD_RATE]))
    cg.add(var.set_decrease_baud_on_retry(config[CONF_DECREASE_BAUD_ON_RETRY]))
