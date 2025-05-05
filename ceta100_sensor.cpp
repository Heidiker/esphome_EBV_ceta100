#include "esphome/core/log.h"
#include "ceta100_sensor.h"

namespace esphome {
namespace ceta100_sensor {

static const char *TAG = "ceta100_sensor";

void Ceta100Sensor::setup() {
  ESP_LOGI(TAG, "CETA100 Sensor setup complete.");
}

void Ceta100Sensor::update() {
  if (available() >= 43) {
      uint8_t data[43];
      for (int i = 0; i < 43; i++) {
      data[i] = read();
    }
    
    if (data[0] != 0x21 || data[1] != 0x0A || data[2] != 0x15) {
      return;
    }
    if (pv_temp_sensor_ != nullptr) {
      //pv_temp_sensor_->publish_state((data[14] | (data[15] << 8)) / 10.0);
      int16_t raw_temp = static_cast<int16_t>(data[14] | (data[15] << 8)); // In signed 16-Bit umwandeln
      pv_temp_sensor_->publish_state(raw_temp / 10.0);
    }
    if (water_temp_sensor_ != nullptr) {
      //water_temp_sensor_->publish_state((data[16] | (data[17] << 8)) / 10.0);
      int16_t raw_temp2 = static_cast<int16_t>(data[16] | (data[17] << 8)); // In signed 16-Bit umwandeln
      water_temp_sensor_->publish_state(raw_temp2 / 10.0);
    }
    if (pump_hours_sensor_ != nullptr) {
      pump_hours_sensor_->publish_state(data[18] | (data[19] << 8));
    }
    if (pump_starts_sensor_ != nullptr) {
      pump_starts_sensor_->publish_state(data[20] | (data[21] << 8));
    }
    if (burner_mode_binary_sensor_ != nullptr) {
      burner_mode_binary_sensor_->publish_state(data[13] > 0);
    }
  }
}


void Ceta100Sensor::dump_config() {
    ESP_LOGCONFIG(TAG, "CETA100 sensor");
}

}  // namespace ceta100_sensor
}  // namespace esphome

//publish_state(bytes[1]);
//00:01:02:03:04:05:06:07:08:09:10:11:12:13:14:15:16:17:18:19:20:21:22:23:24:25:26:27:28:29:30:31:32:33:34:35:36:37:38:39:40:41:42
//21:0A:15:8E:17:00:22:00:00:1F:00:00:01:00:80:00:5C:01:6D:13:6A:07:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:A8:E6

//#0...#2: unknown, most likely start marker, seem to be always 210a0a ?
//#3...#4: unknown, most likely message type, seem to be always 8417 ?
//#5...#7: unknown, message length seem to be always 0011 (=dec 17= 26 bytes total - 7 bytes header - 2 bytes checksum)
//....
//
//#9: 0 unknown
//#8: 0,1 unknown
//#9: unknown, seem to be always 1
//(#10+#11*256)/10 (long int):
//(#12+#13*256)/10 (long int): Nominal Temperature Water
//(#14+#15*256)/10 (long int): Actual Temperature Burner
//#16: duplicate of 15?
//#17: "Burner mode (0=off, 1=heat, 2=water)" ?
//#18: unknown, always 0
//#19: unknown, always 128 (or 1000000, so it could be bit-coded, still it always remains the same)
//#20+#21*256)/10 (signed long int): Outdoor Temperature
//#21+#22*256)/10 (long int): Nominal Temperature Burner
//...
//
//#23,#24: CRC-16 checksum (over ?)