#!/bin/sh
set -e

# Simple health check using curl
curl --fail http://localhost:9000/health
