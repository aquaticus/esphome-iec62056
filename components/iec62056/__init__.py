# components/iec62056/__init__.py
import re
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID, CONF_UPDATE_INTERVAL

AUTO_LOAD = ["sensor", "text_sensor"]
DEPENDENCIES = ["uart"]

iec62056_ns = cg.esphome_ns.namespace("iec62056")
IEC62056Component = iec62056_ns.class_("IEC62056Component", cg.Component, uart.UARTDevice)

# ---- keys exported for sensor.py / text_sensor.py ----
CONF_IEC62056_ID = "iec62056_id"
CONF_OBIS = "obis"

# ---- component options ----
CONF_BAUD_RATE_MAX = "baud_rate_max"
CONF_FORCE_BAUD_RATE = "force_baud_rate"
CONF_DECREASE_BAUD_ON_RETRY = "decrease_baud_on_retry"
CONF_BATTERY_METER = "battery_meter"
CONF_MAX_RETRIES = "max_retries"
CONF_RETRY_DELAY = "retry_delay"
CONF_RECEIVE_TIMEOUT = "receive_timeout"
CONF_MODE_D = "mode_d"  # опционально, если используете принудит. Mode D

def validate_obis(value):
    value = cv.string_strict(value)
    # Примеры валидных кодов: 1.8.0, 2.6.0, 12.7.0, 15.8.1
    if not re.fullmatch(r"\d+(?:\.\d+){2,3}", value):
        raise cv.Invalid("OBIS должен выглядеть как '1.8.0', '2.6.0', '12.7.0' и т.п.")
    return value

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(CONF_IEC62056_ID): cv.declare_id(IEC62056Component),
            cv.Optional(CONF_UPDATE_INTERVAL, default="67s"): cv.positive_time_period_milliseconds,
            cv.Optional(CONF_BAUD_RATE_MAX, default=9600): cv.int_,
            cv.Optional(CONF_FORCE_BAUD_RATE, default=0): cv.int_,  # 0 = авто по ID
            cv.Optional(CONF_DECREASE_BAUD_ON_RETRY, default=True): cv.boolean,
            cv.Optional(CONF_BATTERY_METER, default=False): cv.boolean,
            cv.Optional(CONF_MAX_RETRIES, default=3): cv.int_range(min=0, max=10),
            cv.Optional(CONF_RETRY_DELAY, default="3s"): cv.positive_time_period_milliseconds,
            cv.Optional(CONF_RECEIVE_TIMEOUT, default="7s"): cv.positive_time_period_milliseconds,
            cv.Optional(CONF_MODE_D, default=False): cv.boolean,
        }
    )
    .extend(uart.UART_DEVICE_SCHEMA)
    .extend(cv.COMPONENT_SCHEMA)
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_IEC62056_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if CONF_UPDATE_INTERVAL in config:
        cg.add(var.set_update_interval(config[CONF_UPDATE_INTERVAL].total_milliseconds))
    if CONF_BAUD_RATE_MAX in config:
        cg.add(var.set_baud_rate_max(config[CONF_BAUD_RATE_MAX]))
    if CONF_RECEIVE_TIMEOUT in config:
        cg.add(var.set_receive_timeout(config[CONF_RECEIVE_TIMEOUT].total_milliseconds))
    if CONF_MAX_RETRIES in config:
        cg.add(var.set_retry_counter_max(config[CONF_MAX_RETRIES]))
    if CONF_RETRY_DELAY in config:
        cg.add(var.set_retry_delay(config[CONF_RETRY_DELAY].total_milliseconds))
    if CONF_BATTERY_METER in config:
        cg.add(var.set_battery_meter(config[CONF_BATTERY_METER]))
    if CONF_MODE_D in config:
        cg.add(var.set_force_mode_d(config[CONF_MODE_D]))

    # Новые опции
    if CONF_FORCE_BAUD_RATE in config:
        cg.add(var.set_force_baud_rate(config[CONF_FORCE_BAUD_RATE]))
    if CONF_DECREASE_BAUD_ON_RETRY in config:
        cg.add(var.set_decrease_baud_on_retry(config[CONF_DECREASE_BAUD_ON_RETRY]))
