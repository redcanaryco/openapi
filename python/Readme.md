# Red Canary Python API

## Getting started

    mkvirtualenv / workon redcanary
    python setup.py install

Set environment variables below or pass as optional parameters to Detections object:

    RED_CANARY_CUSTOMER_ID=<YOUR CUSTOMER ID/NAME>
    RED_CANARY_AUTH_TOKEN=<YOUR API TOKEN>

## Running with a REPL

    redcanary

## Examples

    import redcanary
    rc = redcanary.Detections()

    for detection in rc.all(since='2015-05-10T02:15:20Z'):
        print(detection.headline, detection.hostname)

## Running the tests

    python3 -m unittest discover -s test
