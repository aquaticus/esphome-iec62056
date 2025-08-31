# components/iec62056/__init__.py
# -*- coding: utf-8 -*-

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID

# Экспортируемые константы — на них ссылаются sensor.py / text_sensor.py
CONF_IEC62056_ID = "iec62056_id"
CONF_OBIS = "obis"

# Настройки самого компонента
CONF_BAUD_RATE_MAX = "baud_rate_max"
CONF_RECEIVE_TIMEOUT = "receive_timeout"
CONF_RETRY_COUNTER_MAX = "retry_counter_max"
CONF_RETRY_DELAY = "retry_delay"
CONF_BATTERY_METER = "battery_meter"

# Новые опции
CONF_FORCE_BAUD_RATE = "force_baud_rate"
CONF_DECREASE_BAUD_ON_RETRY = "decrease_baud_on_retry"

AUTO_LOAD = ["sensor", "text_sensor"]
DEPENDENCIES = ["uart"]

iec62056_ns = cg.esphome_ns.namespace("iec62056")
IEC62056Component = iec62056_ns.class_(
    "IEC62056",  # имя класса совпадает с заголовком в репозитории
    cg.PollingComponent,
    uart.UARTDevice,
)

def _baud_choice():
    # Разрешаем реальные значения для D0: 0=авто, иначе фикс
    return cv.one_of(0, 1200, 2400, 4800, 9600, int=True)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(IEC62056Component),

            cv.Optional(CONF_BAUD_RATE_MAX, default=0): _baud_choice(),
            cv.Optional(CONF_RECEIVE_TIMEOUT, default="7s"): cv.positive_time_period_milliseconds,
            cv.Optional(CONF_RETRY_COUNTER_MAX, default=3): cv.int_range(min=0, max=10),
            cv.Optional(CONF_RETRY_DELAY, default="3s"): cv.positive_time_period_milliseconds,
            cv.Optional(CONF_BATTERY_METER, default=False): cv.boolean,

            # Новые ключи:
            cv.Optional(CONF_FORCE_BAUD_RATE, default=0): _baud_choice(),
            cv.Optional(CONF_DECREASE_BAUD_ON_RETRY, default=True): cv.boolean,
        }
    )
    .extend(cv.polling_component_schema("60s"))
    .extend(uart.UART_DEVICE_SCHEMA)
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    # Базовые опции
    if config[CONF_BAUD_RATE_MAX] != 0:
        cg.add(var.set_baud_rate_max(config[CONF_BAUD_RATE_MAX]))
    cg.add(var.set_receive_timeout(config[CONF_RECEIVE_TIMEOUT].total_milliseconds))
    cg.add(var.set_retry_counter_max(config[CONF_RETRY_COUNTER_MAX]))
    cg.add(var.set_retry_delay(config[CONF_RETRY_DELAY].total_milliseconds))
    cg.add(var.set_battery_meter(config[CONF_BATTERY_METER]))

    # Новые опции
    if config[CONF_FORCE_BAUD_RATE] != 0:
        cg.add(var.set_force_baud_rate(config[CONF_FORCE_BAUD_RATE]))
    cg.add(var.set_decrease_baud_on_retry(config[CONF_DECREASE_BAUD_ON_RETRY]))
