# Osprey

Osprey is a desktop program that runs as a daemon that allows for voice based computer input and usage. It is an open source version of [talonvoice](https://talonvoice.com/) and is being initially developed for Linux and Swaywm, with the eventual goal of being cross platform. It is highly configurable with Python, and there is already a thriving community of users with existing configurations that are ready to use. It uses Google Cloud Speech-to-Text for voice transcription but other engines are welcome to be incorporated.

For help getting started, check out:

- [Getting Started with Voice Driven Development](https://whalequench.club/blog/2019/09/03/learning-to-speak-code.html)
- [Talon Voice Control: basics](https://www.youtube.com/watch?v=oB5TGMEhQp4&feature=youtu.be)
- [Unofficial Talon Docs](https://github.com/dwighthouse/unofficial-talonvoice-docs)
- [talon_community](https://github.com/dwiel/talon_community)
- [Perl Out Loud](https://www.youtube.com/watch?v=Mz3JeYfBTcY)

## Requirements

- Python 3.4+
- PortAudio
- A GCP account with a project setup and enabled with the Speech-to-Text API
	- follow step 1 [here](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries) for an easy setup process
	- then copy the credentials to `~/.config/osprey/credentials.json`
- A (decent) microphone
- A stable internet connection

## Installation

Install using [pipx](https://github.com/pipxproject/pipx) with:

```bash
pipx install --spec git+https://github.com/cjbassi/osprey osprey
```

## Usage

Run `osprey`, which runs as a daemon.

Optionally, you can start and enable the [`osprey.service`](./osprey.service) systemd service file to run `osprey` as a systemd service.

To setup the systemd service:

- Copy the service file to `~/.config/systemd/user/`
- Run `systemctl --user daemon-reload`
- Run `systemctl --user enable --now osprey`
