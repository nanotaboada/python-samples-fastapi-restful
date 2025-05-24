#!/bin/sh
set -e

# Minimal curl-based health check with timeout and error reporting
curl --fail --silent --show-error --connect-timeout 1 --max-time 2 http://localhost:9000/health
