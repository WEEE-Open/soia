#!/bin/bash
# Slightly modified version of https://github.com/WEEE-Open/sso/blob/master/ca/cert.sh

# Accept a hostname or default to localhost, then export it
HOSTNAME=${1:-localhost}
export SAN=$HOSTNAME

# Create noise.bin from random using ssl if it does not exist
if [[ ! -f files/openssl/noise.bin ]]; then
	 openssl rand -out files/openssl/noise.bin 4096
fi

# Generate certificates but only if they do not exist
if [[ -f fullchain-certificate.pem ]] && [[ -f tls.key ]]; then
	echo "Reusing previous certificate"
else
	# Save certificate and key in ./files/
	# https://security.stackexchange.com/a/86999
	openssl req -x509 -newkey rsa:2048 -sha256 -keyout files/tls.key -out files/fullchain-certificate.pem -days 365 -nodes -extensions eku -config files/openssl/openssl.cnf -subj "/CN=${HOSTNAME}"
fi
