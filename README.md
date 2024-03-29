# Orbyt ✨

> Orbyt is a versatile, quality-of-life Discord Bot for Discord enthusiasts.
 [ ⚠️ In Development ] (See: [Contributing](#contributing)) <br><br>
> Invite Orbyt [HERE](https://discord.com/oauth2/authorize?client_id=900057091031580783&permissions=1945627743&redirect_uri=https://discord.gg/yYSjejHX9G&response_type=code&scope=identify+bot+applications.commands)
### Table of contents
1. [Features](#features)
2. [License](#license)
3. [Getting Started](#getting-started)
    - [Clone the Repository](#clone-the-repository)
    - [Install Dependencies](#install-dependencies)
    - [Set Up Configuration](#set-up-configuration)
    - [Bot Authorization](#bot-authorization)
    - [Configure Debugging (Optional)](#configure-debugging-optional)
    - [Invite the Bot](#invite-the-bot)
    - [Start the Bot](#start-the-bot)
4. [Extended Configuration](#configuration)
5. [Support](#support)
6. [Contributing](#contributing)

## Features

- ``Tags`` A Robust system for quick responders, saving text etc.
- ``Information`` Based commands like `/info user`, `/info server` etc.
- ``Festive`` Limited time commands for a season.
- ``Embedding`` Interactive embed builders! `/embed-builder`

## Getting Started

To get started with Orbyt on your local machine:

1. #### Clone the Repository:
   - Clone this repository to your local machine.

2. #### Install Dependencies:
   - Run `python[3] -m pip install -r requirements.txt` to install all necessary dependencies.
   - Run `python[3] -m pip install -r requirements.dev.txt` if you consider Contributing.

3. #### Set Up Configuration:
   - Rename `config.example.py` to `config.py`.
   - Fill out the `config.py` file. (See [Configuration](#configuration))

4. #### Bot Authorization:
   - Create a new Discord Application + Bot on the [Discord Developer Portal](https://discord.com/developers/applications).
   - Set your main bot token into `config.py`.

5. #### Configure Debugging (Optional):
   - If testing/debugging, set `DEBUG` to `True` in the `config.py`.
   - ⚠️ Set the `DEBUG_BOT_TOKEN` for the bot to function in debug mode.

6. #### Invite the Bot:
   - Generate an invite link from the [Discord Developer Portal](https://discord.com/developers/applications) and invite the bot.

7. #### Start the Bot:
   - Run the bot using `python[3] main.py`.

## Configuration

Ensure to configure the `config.py` file with the following parameters:
- `PROD_TOKEN` is your main bot token
- `MYSTBIN_API_KEY` is your [mystb.in](https://msytb.in/) API Key
- `DEBUG` & `DEBUG_BOT_TOKEN` For debugging (Optional)

```python
# config.py

## ----- PRODUCTION RELATED ----- ##
PROD_TOKEN = ""  # Main Discord Bot Token

## ----- MYSTBIN RELATED ----- ##
MYSTBIN_API_KEY = "" # Mystb.in API Key

## ----- DEBUG RELATED ----- ##
DEBUG = False  # Debug Mode? (Optional) - If True then DEBUG_BOT_TOKEN must be set
DEBUG_BOT_TOKEN = ""  # Debug Bot Token (Optional)

```

## Support

For any assistance, feedback, or bug reports, join the [Support Server](https://discord.gg/dg8SQr3PfY).

---

## Contributing

I appreciate your contributions! Create a pull request for any improvements or corrections after forking the repository.

## License

Copyright (c) 2023-present Ritam Das

This project is licensed under the [GNU Affero General Public License v3.0 (AGPL-3.0)](https://www.gnu.org/licenses/agpl-3.0.en.html). See the [LICENSE](LICENSE) for details.

