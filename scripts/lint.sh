#!/bin/sh

poetry run isort bluetooth_locker
poetry run black bluetooth_locker
