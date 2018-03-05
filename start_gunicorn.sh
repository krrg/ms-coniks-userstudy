#!/bin/bash

gunicorn --bind 0.0.0.0:2236 --workers=2 simple:app
