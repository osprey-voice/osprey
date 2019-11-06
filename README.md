# claw

## Requirements

- Python 3.4+
- PortAudio
- A GCP account with a project setup and enabled with the Speech-to-Text API
	- follow step 1 [here](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries) for an easy setup process
	- then copy the credentials to `~/.config/claw/credentials.json`
- A (decent) microphone
- A stable internet connection

## Installation

```bash
pip install --user git+https://github.com/cjbassi/claw
```

Note that `~/.local/bin` needs to be added to your `$PATH` for user installs.

## Usage

Run `claw`, which runs as a daemon.

Optionally, you can start and enable the [`claw.service`](./claw.service) systemd service file to run `claw` as a systemd service.

To setup the systemd service:

- Copy the service file to `~/.config/systemd/user/`
- Run `systemctl --user daemon-reload`
- Run `systemctl --user enable --now claw`
