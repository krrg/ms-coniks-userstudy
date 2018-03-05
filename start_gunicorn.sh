#!/bin/bash

gunicorn --bind 0.0.0.0:2236 simple:app
