import esphome.config_validation as cv
import esphome.codegen as cg
from esphome.const import CONF_ID

iec62056_ns = cg.esphome_ns.namespace("iec62056")
IEC62056 = iec62056_ns.class_("IEC62056", cg.Component)

CONF_UPDATE_INTERVAL = "update_interval"
CONF_BAUD_RATE_MAX = "baud_rate_max"
CONF_RECEIVE_TIMEOUT = "receive_timeout"
CONF_RETRY_COUNTER_MAX = "retry_counter_max"
CONF_RETRY_DELAY = "retry_delay"
CONF_BATTERY_METER = "battery_meter"

# Новые опции
CONF_FORCE_BAUD_RATE = "force_baud_rate"
CONF_DECREASE_BAUD_ON_RETRY = "decrease_baud_on_retry"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(IEC62056),

    cv.Optional(CONF_UPDATE_INTERVAL, default="60s"): cv.positive_time_period_seconds,
    cv.Optional(CONF_BAUD_RATE_MAX, default=9600): cv.one_of(300, 600, 1200, 2400, 4800, 9600, int=True),
    cv.Optional(CONF_RECEIVE_TIMEOUT, default="7s"): cv.positive_time_period_milliseconds,
    cv.Optional(CONF_RETRY_COUNTER_MAX, default=3): cv.int_,
    cv.Optional(CONF_RETRY_DELAY, default="3s"): cv.positive_time_period_milliseconds,
    cv.Optional(CONF_BATTERY_METER, default=False): cv.boolean,

    # Новые
    cv.Optional(CONF_FORCE_BAUD_RATE): cv.one_of(300, 600, 1200, 2400, 4800, 9600, int=True),
    cv.Optional(CONF_DECREASE_BAUD_ON_RETRY, default=True): cv.boolean,
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    cg.add(var.set_update_interval(config[CONF_UPDATE_INTERVAL]))
    cg.add(var.set_baud_rate_max(config[CONF_BAUD_RATE_MAX]))
    cg.add(var.set_receive_timeout(config[CONF_RECEIVE_TIMEOUT]))
    cg.add(var.set_retry_counter_max(config[CONF_RETRY_COUNTER_MAX]))
    cg.add(var.set_retry_delay(config[CONF_RETRY_DELAY]))
    cg.add(var.set_battery_meter(config[CONF_BATTERY_METER]))

    # Новые
    if CONF_FORCE_BAUD_RATE in config:
        cg.add(var.set_force_baud_rate(config[CONF_FORCE_BAUD_RATE]))
    cg.add(var.set_decrease_baud_on_retry(config[CONF_DECREASE_BAUD_ON_RETRY]))
