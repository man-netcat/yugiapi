# Yu-Gi-Oh! Database REST API

## Overview

This is a RESTful API for accessing Yu-Gi-Oh! card data, archetypes, sets, and more. The API is built using Flask and Flask-RESTful, and it interacts with a Yu-Gi-Oh! database powered by the [yugitoolbox](https://github.com/man-netcat/yugitoolbox) library.

## Prerequisites

- Python 3.11 or higher
- Flask
- Flask-RESTful
- yugitoolbox
- Waitress (for production deployment)

## Installation

1. Clone the repository:

    ```bash
    git clone --recurse-submodules https://github.com/man-netcat/yugiapi.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the API

To run the API, execute the following command:

```bash
python yugiapi.py [--debug] [--port PORT_NUMBER]
```

- `--debug`: Enable debug mode.
- `--port`: Specify the port on which the server will run (default is 5000).

### API Endpoints

- **Card Data**: `/card_data` (GET)
- **Archetype Data**: `/arch_data` (GET)
- **Set Data**: `/set_data` (GET)
- **Names Data**: `/names` (GET)
- **Render Card Image**: `/render/<int:card_id>` (GET)
- **Connection Information**: `/connection` (GET, POST)

### Filter Parameters
#### Card Data
The following filter parameters are available for card data:

- **name**: Card name
- **id**: Card ID (integer)
- **race**: Card race (Race enum)
- **attribute**: Card attribute (Attribute enum)
- **atk**: Attack points (integer)
- **def**: Defense points (integer)
- **level**: Card level (integer)
- **scale**: Pendulum scale (integer)
- **koid**: Card Konami ID (integer)
- **type**: Card type (Type enum)
- **category**: Card category (Category enum)
- **genre**: Card genre (Genre enum)
- **linkmarker**: Link marker (LinkMarker enum)
- **Rarity**: Card TCG rarity (Rarity enum)

For valid enum values, see [this file](https://github.com/man-netcat/yugitoolbox/blob/main/src/enums.py). These are case insensitive.

### Archetype Data
The following filter parameters are available for archetype data:

- **name**: Archetype name
- **id**: Archetype ID (integer)

### Set Data
The following filter parameters are available for set data:

- **name**: Set name
- **abbr**: Set abbreviation
- **id**: Set ID (integer)

### Examples

#### Get Card Data

```bash
curl http://localhost:5000/card_data?name=dark%20magician&type=monster
```

#### Render Card Image

```bash
curl http://localhost:5000/render/10497636
```

## Notes

- The API supports case-insensitive query parameters.
- Debug mode is available for development. Do not use this for production deployments.

## Contributing

Feel free to contribute by opening issues, providing suggestions, or submitting pull requests. Contributions are welcome!
