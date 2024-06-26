![Python](https://img.shields.io/badge/python-v3.11-blue)
[![License](https://img.shields.io/badge/license-GPL%203.0-blue.svg)](LICENSE)

# outages-ge

An app that consolidates public outage data in Georgia (Sakartvelo), making it easier to track everything in one place and stay notified.  
![preview_1](https://github.com/roaddust2/outages-ge/assets/42116054/f642c74c-e60d-4ea2-b134-554c6d7f716e)


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Having lived in Georgia, I know firsthand how disruptive infrastructure outages can be, especially when working from home. That's why I created this app — it consolidates public outage data, making it easier to track everything in one place. Plus, you can subscribe to outage notifications via a Telegram bot.

Best part? It's completely free, now and in the future.

## Features

- Interactive outages map of districts with real-time updates
- Multilanguage support (English/Georgian)
- Telegram notifier
- Street search

## Technologies Used

- Python 3.11
- [FastAPI](https://github.com/tiangolo/fastapi)
- [Bootstrap 5](https://getbootstrap.com/)
- [htmx](https://github.com/bigskysoftware/htmx)
- [OpenStreetMap](https://www.openstreetmap.org/) data with [overpy](https://github.com/DinoTools/python-overpy) wrapper

## Installation

```bash
# Poetry required

make install
make dev
```

## Contributing

-

## License

This project is licensed under the [GPL 3.0 License](LICENSE).
