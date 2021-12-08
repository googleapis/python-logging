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

logging JSON poayloads
----------------------

Although the Python :mod:`logging` standard library `expects all logs to be strings <https://docs.python.org/3/library/logging.html#logging.Logger.debug>`_


- *logging dictionaries*


:mod:`google-cloud-logging` will also attempt to parse stringified JSON objects logged using the library.

Using `extras`
--------------

Automatic Metadata Detection
----------------------------


