#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/uart/uart.h"

namespace esphome {
namespace ceta100_sensor {

class Ceta100Sensor : public PollingComponent, public uart::UARTDevice {
 public:
  void setup() override;
  void update() override;
  void dump_config() override;

  void set_pv_temp_sensor(sensor::Sensor *sensor) { pv_temp_sensor_ = sensor; }
  void set_water_temp_sensor(sensor::Sensor *sensor) { water_temp_sensor_ = sensor; }
  void set_pump_hours_sensor(sensor::Sensor *sensor) { pump_hours_sensor_ = sensor; }
  void set_pump_starts_sensor(sensor::Sensor *sensor) { pump_starts_sensor_ = sensor; }
  void set_burner_mode_binary_sensor(binary_sensor::BinarySensor *sensor) { burner_mode_binary_sensor_ = sensor; }

 protected:
  sensor::Sensor *pv_temp_sensor_{nullptr};
  sensor::Sensor *water_temp_sensor_{nullptr};
  sensor::Sensor *pump_hours_sensor_{nullptr};
  sensor::Sensor *pump_starts_sensor_{nullptr};
  binary_sensor::BinarySensor *burner_mode_binary_sensor_{nullptr};
};

}  // namespace ceta100_sensor
}  // namespace esphome