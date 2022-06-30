# Bluetooth Locker
<p>
    <a href="https://pypi.org/project/bluetooth-locker/" target="_blank">
        <img src="https://img.shields.io/pypi/v/bluetooth-locker" />
    </a>
    <a href="https://github.com/leng-yue/bluetooth-locker/actions/workflows/ci.yml" target="_blank">
        <img src="https://img.shields.io/github/workflow/status/leng-yue/bluetooth-locker/CI?label=check" />
    </a>
    <img src="https://img.shields.io/github/license/leng-yue/bluetooth-locker" />
    <a href="https://pepy.tech/project/bluetooth-locker" target="_blank">
        <img src="https://pepy.tech/badge/bluetooth-locker" />
    </a>
</p>

A simple bluetooth based locker that lock and unlock your linux desktop automatically.

## How to use

You need to have `libbluetooth-dev` in your system. 

```shell
# Simple run
bluetooth-locker -d xx:xx:xx:xx:xx:xx

# Multiple devices
bluetooth-locker -d xx:xx:xx:xx:xx:xx -d xx:xx:xx:xx:xx:aa

# Install service
sudo bluetooth-locker -d xx:xx:xx:xx:xx:xx --install

# Uninstall service
sudo bluetooth-locker -d xx:xx:xx:xx:xx:xx --uninstall
```

## [Optional] Arduino Bluetooth Key

Though we recommand you to use your phone as the key.

Here is a simple arduino bluetooth server implementation.
