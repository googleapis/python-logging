Python Client for Stackdriver Logging
=====================================

|pypi| |versions|

`Stackdriver Logging API`_: Writes log entries and manages your Stackdriver
Logging configuration.

- `Client Library Documentation`_
- `Product Documentation`_

.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-logging.svg
   :target: https://pypi.org/project/google-cloud-logging/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-logging.svg
   :target: https://pypi.org/project/google-cloud-logging/
.. _Stackdriver Logging API: https://cloud.google.com/logging
.. _Client Library Documentation: https://googleapis.dev/python/logging/latest
.. _Product Documentation:  https://cloud.google.com/logging/docs
.. _Setting Up Cloud Logging for Python: https://cloud.google.com/logging/docs/setup/python

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Stackdriver Logging API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Stackdriver Logging API.:  https://cloud.google.com/logging
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html

Installation
~~~~~~~~~~~~

Install this library in a `venv`_ using pip. `venv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `venv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`venv`: https://docs.python.org/3/library/venv.html


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.5

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7. Python 2.7 support was removed on January 1, 2020.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    python -m venv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-logging


Windows
^^^^^^^

.. code-block:: console

    python -m venv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-logging

Using the API
-------------

Connecting the library to Python logging

.. code:: python

    # Imports the Cloud Logging client library
    import google.cloud.logging

    # Instantiates a client
    client = google.cloud.logging.Client()

    # Retrieves a Cloud Logging handler based on the environment
    # you're running in and integrates the handler with the
    # Python logging module. By default this captures all logs
    # at INFO level and higher
    client.setup_logging()

Using the Python root logger:

.. code:: python

    # Imports Python standard library logging
    import logging

    # The data to log
    text = 'Hello, world!'

    # Emits the data using the standard logging module
    logging.warning(text)

Next Steps
~~~~~~~~~~

-  Read the `Setting Up Cloud Logging for Python`_ getting started doc
-  Read the `Product documentation`_ to learn more about the product and see
   How-to Guides.
-  Read the `Client Library Documentation`_ for to see other available
   methods on the client.
