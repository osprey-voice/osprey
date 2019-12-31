# Osprey

Osprey is a desktop program that runs as a daemon that allows for voice based computer input and usage and is an open source version of [talonvoice](https://talonvoice.com/). It is being initially developed for Linux and Swaywm and uses Google Cloud Speech-to-Text for voice transcription but other platforms and voice engines are welcome to be incorporated.

Osprey is highly configurable with Python, and uses Python scripts to match voice input with computer commands. No commands are included by default, but [osprey-starter-pack](https://github.com/osprey-voice/osprey-starter-pack) exists as a starting point for some basic commands.

For help getting started, check out:

- [Getting Started with Voice Driven Development](https://whalequench.club/blog/2019/09/03/learning-to-speak-code.html)
- [Talon Voice Control: basics](https://www.youtube.com/watch?v=oB5TGMEhQp4&feature=youtu.be)
- [Unofficial Talon Docs](https://github.com/dwighthouse/unofficial-talonvoice-docs)
- [Perl Out Loud](https://www.youtube.com/watch?v=Mz3JeYfBTcY)

## Requirements

- Python 3.5+
- PortAudio
- A GCP account with a project setup and enabled with the Speech-to-Text API
	- follow step 1 [here](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries) for an easy setup process
	- then copy the credentials to `~/.config/osprey/credentials.json`
- A (decent) microphone
- A stable internet connection

### Linux

In order to simulate keypresses on Linux, the current user needs to gain write access to `/dev/uinput`. To enable this, we first need to change the permissions on `/dev/uinput` to allow for members of the `uinput` group to write to it, which we do with a udev rule. Then we create the `uinput` group and add the current user to it. Make sure to restart your computer after doing the following to allow for the udev rule to go into effect.

```bash
sudo cp 40-uinput.rules /etc/udev/rules.d/
sudo groupadd uinput
sudo usermod -a -G uinput $USER
```

## Installation

Install using [pipx](https://github.com/pipxproject/pipx) with:

```bash
pipx install --spec git+https://github.com/cjbassi/osprey osprey
```

It's also highly recommended to clone the [osprey-starter-pack](https://github.com/osprey-voice/osprey-starter-pack) repo to the Osprey config directory for some basic voice commands.

On Linux do:

```bash
git clone https://github.com/osprey-voice/osprey-starter-pack ~/.config/osprey/osprey-starter-pack
```

## Usage

Run `osprey`, which runs as a daemon.

Optionally, you can start and enable the [`osprey.service`](./osprey.service) systemd service file to run Osprey as a systemd service.

To setup the systemd service:

- Copy the service file to `~/.config/systemd/user/`
- Run `systemctl --user daemon-reload`
- Run `systemctl --user enable --now osprey`
