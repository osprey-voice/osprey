# Osprey

[![Matrix](https://img.shields.io/badge/matrix-%23osprey-blue.svg)](https://matrix.to/#/#osprey:matrix.org)

Osprey is a cross-platform voice typing program that allows you to use your computer and type with your voice. It can be used for coding, web browsing, dictating, and more in an efficient and reliable way. It is built on top of [Dragonfly](https://github.com/dictation-toolbox/dragonfly) and [Kaldi Active Grammar](https://github.com/daanzu/kaldi-active-grammar) which uses [Kaldi](https://github.com/kaldi-asr/kaldi) for speech recognition but other engines are welcome to be incorporated.

Osprey works by first transcribing microphone audio to text using a speech recognition engine, then it matches the transcription to user specified commands and keyboard input. It is highly configurable with Python, and uses Python scripts to specify the commands using the Osprey APIs. No commands are included by default, but an official starter pack of Osprey scripts exists at [osprey-starter-pack](https://github.com/osprey-voice/osprey-starter-pack).

Official resources:

- [The Osprey wiki](https://github.com/osprey-voice/osprey/wiki)
- [The Osprey Matrix room](https://matrix.to/#/#osprey:matrix.org)
- [osprey-starter-pack](https://github.com/osprey-voice/osprey-starter-pack)

Other great resources for help getting started:

- [Getting Started with Voice Driven Development](https://whalequench.club/blog/2019/09/03/learning-to-speak-code.html)
- [Talon Voice Control: basics](https://www.youtube.com/watch?v=oB5TGMEhQp4&feature=youtu.be)
- [Perl Out Loud](https://www.youtube.com/watch?v=Mz3JeYfBTcY)

## Requirements

- Python 3.5+
- GTK3
- PortAudio
- A (decent) microphone
- A compatible Kaldi language model
- About 1GB of memory for the Kaldi model

## Installation

Install using [pipx](https://github.com/pipxproject/pipx) with:

```bash
pipx install --spec git+https://github.com/osprey-voice/osprey osprey
```

### Osprey Starter Pack

It's highly recommended to clone the [osprey-starter-pack](https://github.com/osprey-voice/osprey-starter-pack) repo to the Osprey config directory for some basic voice commands.

There are instructions for how to do this in that project's README.

### PortAudio

#### Linux

Install PortAudio using your distro's package manager.

### Kaldi

Download and extract one of the Kaldi models from [here](https://github.com/daanzu/kaldi-active-grammar/releases) to the Osprey config directory.

Note that Kaldi models take up quite a bit of memory, ranging from about 0.5GB to 2GB depending on the size of its vocabulary, so you have to choose your model accordingly.

### Wayland keypress simulation

In order to simulate keypresses in Wayland, the current user needs to gain write access to `/dev/uinput`.

To enable this:

- Copy the [`40-uinput.rules`](./40-uinput.rules) udev rule to `/etc/udev/rules.d/` (requires `sudo`) to change the permissions on `/dev/uinput` to allow for members of the `uinput` group to write to it
- Run `sudo groupadd uinput` to create the `uinput` group
- Run `sudo usermod -a -G uinput $USER` to add the current user to the `uinput` group
- Then restart your computer to allow for the udev rule to go into effect

## Usage

Run `osprey` to start the daemon.

Osprey will load the Python scripts that it finds in the Osprey config directory.

For more info, check out the [wiki](https://github.com/osprey-voice/osprey/wiki).

### Run as a service

#### Linux

A systemd service file is provided [here](./osprey.service) to run Osprey as a systemd service.

To setup this up:

- Copy [`osprey.service`](./osprey.service) to `~/.config/systemd/user/`
- Run `systemctl --user daemon-reload`

From here, you can start the service by running:

```bash
systemctl --user start osprey
```

And you can enable the service to be started when you login with:

```bash
systemctl --user enable osprey
```

## Related projects

- [Caster](https://github.com/dictation-toolbox/Caster)
- [Serenade](https://serenade.ai/) (closed source)
- [Talon](https://talonvoice.com/) (closed source)
