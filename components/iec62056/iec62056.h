#pragma once

#include "esphome/core/component.h"

namespace esphome {
namespace iec62056 {

class IEC62056 : public Component {
 public:
  // Базовые сеттеры, которые уже использует Python-обёртка (__init__.py)
  void set_update_interval(uint32_t ms) { this->update_interval_ms_ = ms; }
  void set_baud_rate_max(uint32_t baud) { this->baud_rate_max_ = baud; }
  void set_receive_timeout(uint32_t ms) { this->receive_timeout_ms_ = ms; }
  void set_retry_counter_max(uint8_t n) { this->retry_counter_max_ = n; }
  void set_retry_delay(uint32_t ms) { this->retry_delay_ms_ = ms; }
  void set_battery_meter(bool v) { this->battery_meter_ = v; }

  // === Новые опции ===
  // Принудительная скорость после рукопожатия (/?!), игнорируя negotiated max.
  // 0 = не задано (используем negotiated поведение как раньше).
  void set_force_baud_rate(uint32_t baud) { this->force_baud_rate_ = baud; }

  // Запрет/разрешение автоматического понижения скорости на ретраях.
  void set_decrease_baud_on_retry(bool v) { this->decrease_baud_on_retry_ = v; }

  // Жизненный цикл компонента (реализуется в .cpp)
  void setup() override;
  void loop() override;
  float get_setup_priority() const override { return esphome::setup_priority::LATE; }

 protected:
  // ====== Конфигурация ======
  uint32_t update_interval_ms_{60000};
  uint32_t baud_rate_max_{9600};
  uint32_t receive_timeout_ms_{7000};
  uint8_t retry_counter_max_{3};
  uint32_t retry_delay_ms_{3000};
  bool battery_meter_{false};

  // Новые поля
  uint32_t force_baud_rate_{0};   // 0 → не задано; иначе 300/600/1200/2400/4800/9600
  bool decrease_baud_on_retry_{true};

  // ====== Служебные поля/методы, существующие в твоём .cpp ======
  // Обрати внимание: это декларации, реализация уже есть у тебя.
  // Здесь только то, что нам нужно для модификаций скорости.
  void switch_to_new_baud_(uint32_t baud, char code_char);
  void start_session_();                   // начало новой сессии (отправка /?! и т.п.)
  bool wait_for_readout_start_();          // ожидание старта передачи счётчика
  bool perform_readout_cycle_();           // основной цикл чтения (парс OBIS и т.п.)
  void end_session_();                     // завершение сессии

  // Параметры, вычисленные в ходе идентификации
  uint32_t negotiated_max_baud_{9600};     // из ответа счётчика ('5','4','3'...)
  char negotiated_code_char_{'5'};         // соответствующий код скорости

  // Служебное
  uint32_t last_run_ms_{0};
  uint8_t retry_index_{0};

  // Вспомогательные
  void apply_forced_or_negotiated_speed_(uint32_t &target_baud, char &code_char);
  void maybe_decrease_baud_on_retry_(uint8_t retry_index, uint32_t &target_baud, char &code_char);
};

}  // namespace iec62056
}  // namespace esphome
