# IEC 62056-21 component for ESPHome

IEC 62056-21 is an international standard for a protocol to exchange data with utility meters. Mostly for electricity but also water, thermal and other meters. It was previously known as IEC 61107

The `iec62056` component allows you to read data from any compatible meter. It requires a serial port and an external optical interface.

**Documentation:** https://aquaticus.info/iec62056.html

**Build you own meter interface:** https://aquaticus.info/meter.html

## Older IEC 61107 meters

Some meters made for the older IEC 61107 (IEC 1107) edition don't follow IEC 62056-21 exactly. Some of them calculate the block check character (BCC) differently. The `bcc` option handles this:

| Option | Default | Description |
|---|---|---|
| `bcc` | `xor` | Block check character algorithm: `xor` (standard), `sum` (arithmetic sum, M-Bus style; only the low 7 bits are compared on a 7-bit link) or `none` (no check). When verification fails, the log shows both the XOR and the sum, so you can see which one the meter uses. |

Example for a Kamstrup 382 (685-382), which uses an arithmetic BCC:

```yaml
uart:
  rx_pin: GPIOXX  # your optical head pins
  tx_pin: GPIOXX
  baud_rate: 300
  data_bits: 7
  parity: EVEN
  stop_bits: 1

iec62056:
  bcc: sum

sensor:
  - platform: iec62056
    obis: "1.20"
    name: "Energy"
```
