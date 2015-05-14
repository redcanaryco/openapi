# Red Canary Python API

## Getting started

    mkvirtualenv / workon redcanary
    python setup.py develop

If you are OS X,

    pip install requests[security]

Create a .env file in openapi/python with the following:

    RED_CANARY_CUSTOMER_ID=<YOUR CUSTOMER ID/NAME>
    RED_CANARY_AUTH_TOKEN=<YOUR API TOKEN>

## Running

    redcanary

## Examples

    See `test.py`.

## Running the tests

    python setup.py test


