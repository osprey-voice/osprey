# Osprey

Osprey is a cross-platform voice typing program that allows you to use your computer and type with your voice.
It can be used for coding, web browsing, dictating, or any other keyboard driven task.
It is built on top of [Dragonfly](https://github.com/dictation-toolbox/dragonfly) and [Kaldi Active Grammar](https://github.com/daanzu/kaldi-active-grammar) which uses [Kaldi](https://github.com/kaldi-asr/kaldi) for speech recognition.
Osprey is completely built on open source software and runs completely locally with no dependency on proprietary speech recognition APIs.
The available speech recognition models are also built from open data sets.

Osprey works by providing a Python API that allows users to specify voice commands, from which Osprey builds a strict and limited grammar that specifies the possible commands a user can say.
This grammar is then fed to a speech recognition engine, which then begins to transcribe microphone audio against the grammar by trying to match the audio to one of the commands.
If one of the commands matches, the user-specified callback associated with the voice command is then executed.
Osprey provides some built in functions for simulating key presses that can be used in command callbacks.
Voice commands are specified in user-defined Python scripts which Osprey loads from its config directory on startup.
No commands are included by default, instead an official starter pack of Osprey scripts exists at [osprey-starter-pack](https://github.com/osprey-voice/osprey-starter-pack) which can be installed by cloning them to the config directory.

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
- Git
- A (decent) microphone
- A compatible Kaldi model that supports your language
- Around 0.5GB to 2GB of memory for the Kaldi model during runtime
- (optional) pipx for installation
- (preferable) some programming and Python experience

## Installation

Install using [pipx](https://github.com/pipxproject/pipx) with:

```bash
pipx install git+https://github.com/osprey-voice/osprey
```

Osprey can later be upgraded with:

```bash
pipx upgrade osprey
```

### Osprey Starter Pack

It's highly recommended to clone the [osprey-starter-pack](https://github.com/osprey-voice/osprey-starter-pack) repo to the Osprey config directory for some basic voice commands.

There are instructions for how to do this in that project's README.

### Dependencies

Osprey depends on the following:

```
portaudio
gtk3
python3
git
```

#### Linux

Install the dependencies using your distro's package manager.

#### macOS

Install the dependencies using [Homebrew](https://brew.sh/) with:

```bash
homebrew install portaudio gtk+3 python git
```

#### Windows

TODO

### Kaldi model

Download and extract one of the Kaldi models provided by kaldi-active-grammar [here](https://github.com/daanzu/kaldi-active-grammar/blob/master/docs/models.md) to the Osprey config directory.

**Note**: Kaldi models take up quite a bit of memory during runtime, ranging from about 0.5GB to 2GB depending on the size of the model, so you have to choose your model accordingly.
Larger models have larger vocabulary, which means they can recognize more words, so you should use the largest model you can based on the available resources of your machine.

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
