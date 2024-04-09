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

### Filter Parameters
Parameters can be concatenated with `,` or `|` for `AND` and `OR` functionality. `AND` is evaluated first, then `OR`.

An additional parameter `get` can be added to only include particular parameters in the output. This parameter can be comma separated.

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
- **rarity**: Card TCG rarity (Rarity enum)
- **in_name**: Substring search for card name
- **mentions**: Substring search for card description

#### Valid values (case insensitive):
    
**type**:
    monster, spell, trap, normal, ritual, tuner, pendulum, trapmonster, spsummon, fusion, synchro, xyz, link, token, spirit, union, gemini, flip, toon, effect, quickplay, continuous, equip, field, counter


**linkmarker**:
    bottomleft, bottom, bottomright, left, right, topleft, top, topright


**race**:
    warrior, spellcaster, fairy, fiend, zombie, machine, aqua, pyro, rock, wingedbeast, plant, insect, thunder, dragon, beast, beastwarrior, dinosaur, fish, seaserpent, reptile, psychic, divinebeast, creatorgod, wyrm, cyberse, illusion, cyborg, magicalknight, highdragon, omegapsychic, celestialknight, galaxy


**attribute**:
    earth, water, fire, wind, light, dark, divine


**category**:
    skillcard, speedspellcard, bosscard, betacard, actioncard, commandcard, doublescript, rushlegendary, preerrata, darkcard, duellinks, rushcard, startcard, onecard, twocard, threecard, levelzero, treatedas, bluegod, yellowgod, redgod, rushmax, sc


**genre**:
    stdestroy, destroymonster, banish, graveyard, backtohand, backtodeck, destroyhand, destroydeck, draw, search, recovery, position, control, changeatkdef, piercing, repeatattack, limitattack, directattack, specialsummon, token, typerelated, attributerelated, damagelp, recoverlp, destroy, select, counter, gamble, fusionrelated, tunerrelated, xyzrelated, negateeffect, ritualrelated, pendulumrelated, linkrelated, handtrap


**status**:
    ocg, tcg, legal, illegal


**rarity**:
    common, shortprint, supershortprint, rare, super, ghostgold, ultra, ultimate, secret, ultrasecret, goldsecret, prismaticsecret, ghost, platinum, normalparallel, superparallel, ultraparallel, duelterminalnormal, duelterminalrare, duelterminalsuper, duelterminalshatterfoil, starlight, gold, platinumsecret, tenthousandsecret, mezuki, starfoil, collectors, premiumgold, mosaic, pharaohs, shatterfoil

**race**, **attribute**, **level**, **atk** and **def** support the value **?**. 

**atk** can be set equal to **def**. 

```
/api/v1/card_data?atk=def
```

Additional comparators `<`, `>`, `<=` and `>=` are supported and can be used as follows:

```
/api/v1/card_data?level=>4
```

This finds monsters with a level greater than 4.

Negation is suppored as well, using the prefix `~` operator, and will negate everything that follows. This can be combined with comparators and concatenation.

```
/api/v1/card_data?level=~5
```

This finds all monsters with level not equal to 5.

### Archetype Data
The following filter parameters are available for archetype data:

- **name**: Archetype name
- **id**: Archetype ID (integer)
- **in_name**: Substring search for archetype name

### Set Data
The following filter parameters are available for set data:

- **name**: Set name
- **abbr**: Set abbreviation
- **id**: Set ID (integer)
- **in_name**: Substring search for set name

### Examples

#### Get Card Data

```
/api/v1/card_data?name=dark%20magician&type=monster # Finds all monster cards named Dark Magician
/api/v1/card_data?in_name=dragon&race=~dragon&type=monster # Finds all monsters with 'Dragon' in the name that are not 'Dragon-Type'
/api/v1/card_data?type=synchro,pendulum|fusion,pendulum # Finds all Fusion and Synchro Pendulum Monsters
```

#### Render Card Image

```
/api/v1/render/10497636
```

## Notes

- The API supports case-insensitive query parameters.
- Debug mode is available for development. Do not use this for production deployments.

## Contributing

Feel free to contribute by opening issues, providing suggestions, or submitting pull requests. Contributions are welcome!
