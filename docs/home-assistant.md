# Konfiguracja Home-Asisstanta

## Przykładowa konfiguracja sensora mqtt

```yaml
- platform: mqtt
  state_topic: "garbage/schedule/MT"
  name: Data wywozu metali i tworzyw
  value_template: "{{ value_json.data }}"
- platform: mqtt
  state_topic: "garbage/schedule/OP"
  name: Data wywozu papieru
  value_template: "{{ value_json.data }}"
- platform: mqtt
  state_topic: "garbage/schedule/OS"
  name: Data wywozu szkła
  value_template: "{{ value_json.data }}"
- platform: mqtt
  state_topic: "garbage/schedule/WG"
  name: Data wywozu gabarytów
  value_template: "{{ value_json.data }}"
- platform: mqtt
  state_topic: "garbage/schedule/ZM"
  name: Data wywozu odpadów zmieszanych
  value_template: "{{ value_json.data }}"
```

## Przykładowa automatyzacja

```yaml
alias: harmonogram wywozu odpadów MT
description: ''
trigger:
  - platform: event
    event_type: state_changed
    event_data:
      entity_id: sensor.data_wywozu_metali_i_tworzyw
condition: []
action:
  - service: google.add_event
    data:
      calendar_id: abcdef20375089764@group.calendar.google.com
      summary: Wywóz metali i tworzyw sztucznych
      start_date_time: >-
        {{ strptime(states("sensor.data_wywozu_metali_i_tworzyw"),
        "%Y-%m-%dT%H:%M:%S")}}
      end_date_time: >-
        {{ strptime(states("sensor.data_wywozu_metali_i_tworzyw"),
        "%Y-%m-%dT%H:%M:%S") + timedelta( minutes = 30 )}}
mode: single
```
