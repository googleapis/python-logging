Integration with `logging` Standard Library
===========================================

The recommended way to use :mod:`google-cloud-logging` is to allow it to integrate with
the Python :mod:`logging` standard library. This way, you can write logs using Python
standards, and still have your logs appear in Google Cloud Logging using custom handlers
behind the scenes.

Automatic Configuration
-----------------------

To integrate :mod:`google-cloud-logging` with the standard :mod:`logging` module,
simply call :meth:`setup_logging` on a :class:`~google.cloud.logging.client.Client` instance.

.. literalinclude:: ../samples/snippets/handler.py
    :start-after: [START logging_handler_setup]
    :end-before: [END logging_handler_setup]
    :dedent: 4

This function will automatically choose the best configurations for the environment your
code is running on. After running :meth:`setup_logging`, you can write logs using the
standard :mod:`logging` module as normal:

.. literalinclude:: ../samples/snippets/handler.py
    :start-after: [START logging_handler_usage]
    :end-before: [END logging_handler_usage]
    :dedent: 4

For more information on the library, see the `Google Cloud Logging documentation <https://cloud.google.com/logging/docs/setup/python>`_.
For more information on the Python :mod:`logging` standard library, see the `logging documentation <https://docs.python.org/3/howto/logging.html#a-simple-example>`_

Manual Handler Configuration
-----------------------------

Automatic Configuration will automatically determine the appropriate handler for the environment.
If you would rather choose the handler yourself, you can construct an instance manually and pass it in
as an argument to :meth:`setup_logging`:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START setup_logging]
    :end-before: [END setup_logging]
    :dedent: 4

There are two supported handler classes to choose from:

- :class:`~google.cloud.logging.handlers.CloudLoggingHandler`: 
    - Sends logs directly to Cloud Logging over the network (gRPC or HTTP)
    - This is the default handler on most environments, including local development
- :class:`~google.cloud.logging.handlers.StructuredLogHandler`: 
    - Outputs logs as `structured JSON <https://cloud.google.com/logging/docs/structured-logging#special-payload-fields>`_ 
      to standard out, to be read and parsed by a GCP logging agent
    - This is the default handler on Kubernetes Engine, Cloud Functions and Cloud Run

.. _JSON:

Logging JSON Payloads
----------------------

Although the Python :mod:`logging` standard library `expects all logs to be strings <https://docs.python.org/3/library/logging.html#logging.Logger.debug>`_,
Google Cloud Logging allows `JSON payload data <https://cloud.google.com/logging/docs/structured-logging>`_.
You can write JSON logs using the standard library integration in one of the following ways:

1. Using the `json_fields` `extra` argument:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logging_extra_json_fields]
    :end-before: [END logging_extra_json_fields]
    :dedent: 4

2. Logging a JSON-parsable string:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logging_json_dumps]
    :end-before: [END logging_json_dumps]
    :dedent: 4

Using the `extra` Argument
--------------------------

The Python :mod:`logging` standard library accepts `an "extra" argument <https://docs.python.org/3/library/logging.html#logging.Logger.debug>`_ when
writing logs, which can be used to populate LogRecord objects with user-defined
key-value pairs. Google Cloud Logging uses the `extra` field as a way to pass in
metadata to populate `LogEntry fields <https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry>`_.

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logging_extras]
    :end-before: [END logging_extras]
    :dedent: 4


The following `LogEntry fields <https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry>`_
can be set through the `extra` argument:

- labels
- trace
- span_id
- trace_sampled
- http_request
- source_location
- resource
- :ref:`json_fields<JSON>`


Metadata sent explicitly through the `extra` argument will override any :ref:`automatically detected<Autodetection>` fields.

.. _Autodetection:

Automatic Metadata Detection
----------------------------


