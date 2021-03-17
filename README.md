# Harmonogram odpadów MPO w formie sensora MQTT

Jeśli męczy Cię ręczne sprawdzanie harmonogramu wywozu śmieci, to tym skryptem
możesz sobie to zautomatyzowac.
## Instalacja

```
python3 -m pip install -r requirements.txt
```
## Użytkowanie

1. Utwórz i wypełnij prawidłowymi danymi plik konfiguracyjny `config.yaml` 
(np. na podstawie `config.yaml.orig`).
2. Uruchom:

```
python3 main.py once
```

3. Opcjonalnie skonfiguruj sensor home-assistanta:

```
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

4. Opcjonalnie skonfiguruj crona.

