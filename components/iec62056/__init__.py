# SPDX-License-Identifier: MIT
# IEC 62056-21 (Mode A/B/C/D) component for ESPHome

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.const import (
    CONF_ID,
    CONF_UPDATE_INTERVAL,
    CONF_BAUD_RATE,
)
from esphome.components import uart

AUTO_LOAD = ["uart"]

iec62056_ns = cg.esphome_ns.namespace("iec62056")
IEC62056Component = iec62056_ns.class_("IEC62056Component", cg.Component, uart.UARTDevice)

# существующие ключи
CONF_BAUD_RATE_MAX = "baud_rate_max"
CONF_RECEIVE_TIMEOUT = "receive_timeout"
CONF_RETRY_COUNTER_MAX = "retry_counter_max"
CONF_RETRY_DELAY = "retry_delay"
CONF_BATTERY_METER = "battery_meter"
CONF_MODE_D = "mode_d"

# НОВЫЕ ключи
CONF_FORCE_BAUD_RATE = "force_baud_rate"                  # 0/1200/2400/4800/9600
CONF_DECREASE_BAUD_ON_RETRY = "decrease_baud_on_retry"    # bool

# значения по умолчанию оставляем как раньше
DEFAULT_UPDATE_INTERVAL = "60s"
DEFAULT_RECV_TIMEOUT = "7s"
DEFAULT_RETRY_MAX = 3
DEFAULT_RETRY_DELAY = "3s"
DEFAULT_BAUD_MAX = 0  # 0 = авто (по идентификатору счётчика)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(IEC62056Component),
        cv.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): cv.update_interval,
        cv.Optional(CONF_BAUD_RATE_MAX, default=DEFAULT_BAUD_MAX): cv.int_range(min=0),
        cv.Optional(CONF_RECEIVE_TIMEOUT, default=DEFAULT_RECV_TIMEOUT): cv.positive_time_period_milliseconds,
        cv.Optional(CONF_RETRY_COUNTER_MAX, default=DEFAULT_RETRY_MAX): cv.int_range(min=0, max=10),
        cv.Optional(CONF_RETRY_DELAY, default=DEFAULT_RETRY_DELAY): cv.positive_time_period_milliseconds,
        cv.Optional(CONF_BATTERY_METER, default=False): cv.boolean,
        cv.Optional(CONF_MODE_D, default=False): cv.boolean,
        # НОВОЕ:
        cv.Optional(CONF_FORCE_BAUD_RATE, default=0): cv.one_of(0, 1200, 2400, 4800, 9600, int=True),
        cv.Optional(CONF_DECREASE_BAUD_ON_RETRY, default=True): cv.boolean,
    }
).extend(uart.UART_DEVICE_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    # базовые настройки
    if CONF_UPDATE_INTERVAL in config:
        cg.add(var.set_update_interval_ms(config[CONF_UPDATE_INTERVAL]))
    if CONF_BAUD_RATE_MAX in config:
        cg.add(var.set_baud_rate_max(config[CONF_BAUD_RATE_MAX]))
    if CONF_RECEIVE_TIMEOUT in config:
        cg.add(var.set_receive_timeout_ms(config[CONF_RECEIVE_TIMEOUT]))
    if CONF_RETRY_COUNTER_MAX in config:
        cg.add(var.set_retry_counter_max(config[CONF_RETRY_COUNTER_MAX]))
    if CONF_RETRY_DELAY in config:
        cg.add(var.set_retry_delay_ms(config[CONF_RETRY_DELAY]))
    if CONF_BATTERY_METER in config:
        cg.add(var.set_battery_meter(config[CONF_BATTERY_METER]))
    if CONF_MODE_D in config:
        cg.add(var.set_force_mode_d(config[CONF_MODE_D]))

    # НОВОЕ:
    if CONF_FORCE_BAUD_RATE in config:
        cg.add(var.set_force_baud_rate(config[CONF_FORCE_BAUD_RATE]))
    if CONF_DECREASE_BAUD_ON_RETRY in config:
        cg.add(var.set_decrease_baud_on_retry(config[CONF_DECREASE_BAUD_ON_RETRY]))
