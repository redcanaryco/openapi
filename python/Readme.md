# Red Canary Python API

## Getting started

    mkvirtualenv / workon redcanary
    python setup.py develop

If you are OS X,

    pip install requests[security]

Create a .env file in openapi/python with the following:

    RED_CANARY_CUSTOMER_ID=<YOUR CUSTOMER ID/NAME>
    RED_CANARY_AUTH_TOKEN=<YOUR API TOKEN>

## Running with a REPL

    redcanary

## Examples

    import redcanary
    rc = redcanary.RedCanaryClient()

    for detection in rc.detections(since='2015-01-10T02:15:20Z'):
        print detection.headline, detection.endpoint.hostname

    for indicator in rc.indicators(limit=10):
        print indicator

    for endpoint in rc.endpoints:
        print endpoint.hostname + " has %d detections" % len(endpoint.detections)

    for plan in rc.response_plans:
        print "plan on %s for detection [%s]" % (plan.endpoint.hostname, plan.detection.headline)

    See `test.py` for more examples.

## Running the tests

    python setup.py test
