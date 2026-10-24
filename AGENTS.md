# AGENTS.md

Guidance for AI agents working in this repository.

## What this repo is

`ble-gateway` is a Raspberry Pi gateway for BLE sensors, currently RuuviTags.
It scans for BLE advertisements with the
[`ruuvitag_sensor`](https://pypi.org/project/ruuvitag_sensor/) library, decodes
them, and ships the readings to a data backend.

Docker is used to containerize the application, but deployment to edge devices
runs through **balena** (balenaCloud): `balena push` sends the build directory
to balena's cloud builders, which build the image and publish a release; the
device supervisor on the gateway downloads and runs it as a privileged system
container. The `docker_debian/` variant exists for plain Docker hosts (laptop,
server) — it is for local testing, not edge deployment.

Two data paths are supported (details and diagrams in `README.md`):

* **InfluxDB-direct** (`app.py`): the container writes to InfluxDB itself,
  configured by `config.py`.
* **HTTP backend** (`app_http.py`): the container POSTs JSON to a separate
  `sensor_data_backend` service; all settings come from environment variables
  (`SENSOR_DATA_HOST`, `SENSOR_DATA_PORT`, `GATEWAY_NAME`, set as balena fleet
  env vars — never as committed files).

## Layout

* `app/` — **source of truth** for all Python files.
* `docker_debian/` — plain Docker variant (`Dockerfile`, `docker-compose.yml`).
* `balena_basic/`, `balena_wificonnect/`, `balena_basic_http/` — balena fleet
  build directories (`Dockerfile.template`; `balena_wificonnect/` adds WiFi
  provisioning via `start.sh`).
* Variant `app/` directories are **generated copies** created before each
  build. Never edit them directly — edit `app/`, then re-copy (`cp app/*.* <variant>/app`).

## Commands

```bash
# local (bare-metal) run — BLE tools need sudo
sudo ./venv/bin/python3 ruuvi_app_multitag.py

# plain docker
cp app/*.* docker_debian/app && docker compose build && docker compose up -d

# balena release
cp app/*.* balena_basic_http/app && cd balena_basic_http && balena push <fleet-slug>
```

## Verification

There is no unit-test suite. Verify changes by:

1. `docker compose build` from a clean variant directory succeeds.
2. `app/test_sensor_data_backend.py` posts a fabricated reading to the backend
   endpoint — only against a **test** sensor name, never production names.
3. On a device (or balena logs), confirm the container stays up and POSTs.

## Git

* Commits by an agent use `Hermes Agent <hermes@agent.local>`; human work is
  authored by `Jussi Korpela <jussitapiokorpela@gmail.com>`.
* Commit locally by default; push only on explicit instruction from Jussi.
* Keep the README `# Changelog` updated: one bulleted line per notable change,
  format `- **YYYY-MM-DD** — description.`

## Boundaries

* **Never commit secrets**: balena tokens, gateway API tokens, DB passwords.
  `config*.py` may carry LAN IPs and MAC lists, nothing else sensitive.
* **Never run `balena push` or touch the balenaCloud fleet without explicit
  instruction** — it deploys to a live edge device.
* Don't add framework-level abstractions; keep each Python file self-contained
  and easy to copy (the build process copies files by glob, so deep imports or
  package layout will break the variants).
* Production backend details (endpoint names, IPs) documented in `README.md`
  and the homelab wiki take precedence over memory — re-check them when unsure.