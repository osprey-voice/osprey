# Osprey

Osprey is a desktop program that runs as a daemon that allows for voice based computer input and usage and is an open source version of [talonvoice](https://talonvoice.com/). It can be used for coding, commanding, and dictating to a computer in a highly efficient manner. It is being initially developed for Linux and Swaywm and uses Google Cloud Speech-to-Text for voice transcription but other platforms and voice engines are welcome to be incorporated.

Osprey works by converting microphone audio to voice transcriptions using a speech-to-text engine, then matching the transcriptions to user specified commands and keyboard input. It is highly configurable with Python, and uses Python scripts to match voice transcriptions with computer commands using the APIs provided by Osprey. No commands are included by default, but a starter pack of Osprey scripts exists at [osprey-starter-pack](https://github.com/osprey-voice/osprey-starter-pack).

For help getting started, check out:

- [Getting Started with Voice Driven Development](https://whalequench.club/blog/2019/09/03/learning-to-speak-code.html)
- [Talon Voice Control: basics](https://www.youtube.com/watch?v=oB5TGMEhQp4&feature=youtu.be)
- [The Osprey wiki](https://github.com/osprey-voice/osprey/wiki)
- [Perl Out Loud](https://www.youtube.com/watch?v=Mz3JeYfBTcY)

## Requirements

- Linux
- Python 3.5+
- PortAudio
- A Google Cloud Platform account with a project setup and enabled with the Speech-to-Text API
- A (decent) microphone
- A stable internet connection

## Installation

Install using [pipx](https://github.com/pipxproject/pipx) with:

```bash
pipx install --spec git+https://github.com/osprey-voice/osprey osprey
```

### Osprey Starter Pack

It's highly recommended to clone the [osprey-starter-pack](https://github.com/osprey-voice/osprey-starter-pack) repo to the Osprey config directory for some basic voice commands.

#### Linux

```bash
mkdir -p ~/.config/osprey
git clone https://github.com/osprey-voice/osprey-starter-pack ~/.config/osprey/osprey-starter-pack
```

### PortAudio

#### Arch Linux

```bash
yay -S portaudio
```

### Google Cloud Speech-to-Text

Follow step 1 [here](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries) to easily set up a GCP project for Osprey.

Then copy the credentials to the config directory and name it `credentials.json`.

### Linux keypress simulation

In order to simulate keypresses on Linux, the current user needs to gain write access to `/dev/uinput`.

To enable this:

- Copy the [`40-uinput.rules`](./40-uinput.rules) udev rule to `/etc/udev/rules.d/` (requires `sudo`) to change the permissions on `/dev/uinput` to allow for members of the `uinput` group to write to it
- Run `sudo groupadd uinput` to create the `uinput` group
- Run `sudo usermod -a -G uinput $USER` to add the current user to the `uinput` group
- Then restart your computer to allow for the udev rule to go into effect

## Usage

Run `osprey` to start the daemon.

For more info, check out the [wiki](https://github.com/osprey-voice/osprey/wiki).

### Run as a daemon

#### Linux

Start and enable the [`osprey.service`](./osprey.service) systemd service file to run Osprey as a systemd service.

To setup the systemd service:

- Copy [`osprey.service`](./osprey.service) to `~/.config/systemd/user/`
- Run `systemctl --user daemon-reload`
- Run `systemctl --user enable --now osprey`
