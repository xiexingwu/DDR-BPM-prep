#!/bin/bash
shasum -a 1 "$1" | awk '{print $1}'