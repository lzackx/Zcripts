#! /bin/bash

# Check openssl
echo "Checking..."
if [ `command -v openssl` ];then
    echo 'openssl installed'
else
    echo 'please install openssl first'
    exit
fi

# Check cert.p12 and key.p12 file
CURRENT_PATH=$(pwd)
CERT_PATH="$CURRENT_PATH/cert.p12"
KEY_PATH="$CURRENT_PATH/key.p12"
CERT_PEM_PATH="$CURRENT_PATH/cert.pem"
KEY_PEM_PATH="$CURRENT_PATH/key.pem"
CERT_KEY_PEM_PATH="$CURRENT_PATH/ck.pem"
DEVELOPMENT_URL="gateway.sandbox.push.apple.com:2195"
DISTRIBUTION_URL="gateway.push.apple.com:2195"


if [ ! -f "$CERT_PATH" ]; then 
    echo 'please move cert.p12 file in this directory'
    exit
fi

if [ ! -f "$KEY_PATH" ]; then 
    echo 'please move key.p12 file in this directory'
    exit
fi 

# Encrypt
echo "Encrypting..."
echo "Certificate:"
echo `openssl pkcs12 -clcerts -nokeys -in $CERT_PATH -out $CERT_PEM_PATH`
echo
echo "Private Key"
echo `openssl pkcs12 -nocerts -in $KEY_PATH -out $KEY_PEM_PATH`
echo `cat $CERT_PEM_PATH $KEY_PEM_PATH > $CERT_KEY_PEM_PATH`


if [ ! -f "$CERT_PEM_PATH" ]; then 
    echo 'generate cert.pem failed'
    exit
fi

if [ ! -f "$KEY_PEM_PATH" ]; then 
    echo 'generate key.pem failed'
    exit
fi 

if [ ! -f "$CERT_KEY_PEM_PATH" ]; then 
    echo 'generate ck.pem failed'
    exit
fi 

# Verify
echo "Verifing..."
REQUEST_URL=$DISTRIBUTION_URL
if [ "$1" = "-d" ]; then
    REQUEST_URL=$DEVELOPMENT_URL
fi

echo $REQUEST_URL
echo $CERT_PEM_PATH
echo $KEY_PEM_PATH
echo $CERT_KEY_PEM_PATH
echo `openssl s_client -connect $REQUEST_URL -cert cert.pem -key key.pem`
