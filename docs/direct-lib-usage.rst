Direct Library Usage
====================

Although the recommended way of using the :mod:`google-cloud-logging` library
is to integrate it with the :doc:`Python logging standard library</std-lib-integration>`,
you can also use the library to interact with the Googel Cloud Logging API 
directly.

In addition to writing logs, using the library in this way allows you to manage 
:doc:`logs</entries>`, :doc:`sinks</sink>`, :doc:`metrics</metric>`, and other resources.

Setup
----------------------------

Creating a Client
~~~~~~~~~~~~~~~~~

Before using the library, you must first set up a :doc:`Client</client>`:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START usage_client_setup]
    :end-before: [END usage_client_setup]
    :dedent: 4

When setting up the :doc:`Client</client>`, you can also disable gRPC to put the library
into HTTP mode:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START usage_http_client_setup]
    :end-before: [END usage_http_client_setup]
    :dedent: 4

Creating a Logger
~~~~~~~~~~~~~~~~~

After creating a :doc:`Client</client>`, you can use it to create a :doc:`Logger</logger>`, which can be used
to read, write, and delete logs from Google Cloud:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_create]
    :end-before: [END logger_create]
    :dedent: 4

You can add custom labels initializing a :doc:`Logger</logger>`, which will
be added on to each :doc:`LogEntry</entries>` created by it:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_custom_labels]
    :end-before: [END logger_custom_labels]
    :dedent: 4

By default, the library will attempt to add a `Monitored Resource field <https://cloud.google.com/logging/docs/api/v2/resource-list>`_
associated with the environment the code is run on. For example, code run on
App Engine will have a `gae_app <https://cloud.google.com/monitoring/api/resources#tag_gae_app>`_
resource, while code run locally will have a `global <https://cloud.google.com/monitoring/api/resources#tag_global>`_ resource field.
If you want to manually set the resource field, you can do so when initializing the :doc:`Logger</logger>`:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_custom_resource]
    :end-before: [END logger_custom_resource]
    :dedent: 4


Writing Log Entries
-------------------

You can write logs using :meth:`Logger.log <google.cloud.logging_v2.logging.Logger.log>`:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_log_basic]
    :end-before: [END logger_log_basic]
    :dedent: 4

Additional `LogEntry fields <https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry>`_
can be set by passing them as keyword arguments:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_log_fields]
    :end-before: [END logger_log_fields]
    :dedent: 4

:meth:`Logger.log <google.cloud.logging_v2.logger.Logger.log>` will attempt to choose the appropriate :doc:`LogEntry </entries>` type
based on input type. If you want to be more explicit about the type used, you can use the following
Logger methods:

- :meth:`Logger.log_text <google.cloud.logging_v2.logger.Logger.log_text>` creates a  :class:`TextEntry <google.cloud.logging_v2.entries.TextEntry>`
- :meth:`Logger.log_struct <google.cloud.logging_v2.logger.Logger.log_struct>` creates a :class:`StructEntry <google.cloud.logging_v2.entries.StructEntry>`
- :meth:`Logger.log_proto <google.cloud.logging_v2.logger.Logger.log_proto>` creates a :class:`ProtobufEntry <google.cloud.logging_v2.entries.ProtobufEntry>`
- :meth:`Logger.log_empty <google.cloud.logging_v2.logger.Logger.log_empty>` creates an empty :class:`LogEntry <google.cloud.logging_v2.entries.LogEntry>`

Batch Writing Logs
------------------

By default, each log write will take place in an individual network request, which may be inefficient at scale.
Instead, you can use a :class:`Batch <google.cloud.logging_v2.logger.Batch>`:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_log_batch]
    :end-before: [END logger_log_batch]
    :dedent: 4

In this case, logs are batched together, and only sent out when :func:`batch.commit <google.cloud.logging_v2.logger.Batch.commit>` is called.
To simplify things, you can also use :class:`Batch <google.cloud.logging_v2.logger.Batch>` as a context manager:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_log_batch_context]
    :end-before: [END logger_log_batch_context]
    :dedent: 4

Here, the logs will be automatically committed once the code exits the "with" block.

Retriving Log Entries
---------------------

Fetch entries for the default project.

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START client_list_entries_default]
    :end-before: [END client_list_entries_default]
    :dedent: 4

Entries returned by
:meth:`Client.list_entries <google.cloud.logging_v2.client.Client.list_entries>`
or
:meth:`Logger.list_entries <google.cloud.logging_v2.logger.Logger.list_entries>`
will be instances of one of the following classes:

- :class:`~google.cloud.logging_v2.entries.TextEntry`
- :class:`~google.cloud.logging_v2.entries.StructEntry`
- :class:`~google.cloud.logging_v2.entries.ProtobufEntry`

Filter entries retrieved using the `Advanced Logs Filters`_ syntax

.. _Advanced Logs Filters: https://cloud.google.com/logging/docs/view/advanced_filters

Fetch entries for the default project.

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START client_list_entries_filter]
    :end-before: [END client_list_entries_filter]
    :dedent: 4

Sort entries in descending timestamp order.

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START client_list_entries_order_by]
    :end-before: [END client_list_entries_order_by]
    :dedent: 4

Retrieve entries for a single logger, sorting in descending timestamp order:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_list_entries]
    :end-before: [END logger_list_entries]
    :dedent: 4

And as a practical example, retrieve all `GKE Admin Activity audit logs`_
from the past 24 hours:

.. _GKE Admin Activity audit logs: https://cloud.google.com/kubernetes-engine/docs/how-to/audit-logging#audit_logs_in_your_project

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logging_list_gke_audit_logs]
    :end-before: [END logging_list_gke_audit_logs]
    :dedent: 4


Deleting Log Entries
--------------------

You can delete all logs associated with a logger using the following call:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_delete]
    :end-before: [END logger_delete]
    :dedent: 8


Managing Log Metrics
--------------------

Metrics are counters of entries which match a given filter.  They can be
used within Cloud Monitoring to create charts and alerts.

List all metrics for a project:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START client_list_metrics]
    :end-before: [END client_list_metrics]
    :dedent: 4

Create a metric:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START metric_create]
    :end-before: [END metric_create]
    :dedent: 4

Refresh local information about a metric:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START metric_reload]
    :end-before: [END metric_reload]
    :dedent: 4

Update a metric:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START metric_update]
    :end-before: [END metric_update]
    :dedent: 4

Delete a metric:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START metric_delete]
    :end-before: [END metric_delete]
    :dedent: 4

Using Log Sinks
---------------

Sinks allow exporting entries which match a given filter to Cloud Storage
buckets, BigQuery datasets, or Cloud Pub/Sub topics.

Cloud Storage Sink
~~~~~~~~~~~~~~~~~~~~~~~

Make sure that the storage bucket you want to export logs too has
``cloud-logs@google.com`` as the owner. See
`Setting permissions for Cloud Storage`_.

.. _Setting permissions for Cloud Storage: https://cloud.google.com/logging/docs/export/configure_export_v2#errors_exporting_to_cloud_storage

Add ``cloud-logs@google.com`` as the owner of the bucket:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_bucket_permissions]
    :end-before: [END sink_bucket_permissions]
    :dedent: 4

Create a Cloud Storage sink:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_storage_create]
    :end-before: [END sink_storage_create]
    :dedent: 4


BigQuery Sink
~~~~~~~~~~~~~~~~~~

To export logs to BigQuery you must log into the Cloud Platform Console
and add ``cloud-logs@google.com`` to a dataset.

See: `Setting permissions for BigQuery`_

.. _Setting permissions for BigQuery: https://cloud.google.com/logging/docs/export/configure_export_v2#errors_exporting_to_bigquery

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_dataset_permissions]
    :end-before: [END sink_dataset_permissions]
    :dedent: 4

Create a BigQuery sink:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_bigquery_create]
    :end-before: [END sink_bigquery_create]
    :dedent: 4


Pub/Sub Sink
~~~~~~~~~~~~~~~~~

To export logs to BigQuery you must log into the Cloud Platform Console
and add ``cloud-logs@google.com`` to a topic.

See: `Setting permissions for Pub/Sub`_

.. _Setting permissions for Pub/Sub: https://cloud.google.com/logging/docs/export/configure_export_v2#errors_exporting_logs_to_cloud_pubsub

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_topic_permissions]
    :end-before: [END sink_topic_permissions]
    :dedent: 4

Create a Cloud Pub/Sub sink:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_pubsub_create]
    :end-before: [END sink_pubsub_create]
    :dedent: 4

Managing Sinks
~~~~~~~~~~~~~~

List all sinks for a project:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START client_list_sinks]
    :end-before: [END client_list_sinks]
    :dedent: 4

Refresh local information about a sink:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_reload]
    :end-before: [END sink_reload]
    :dedent: 4

Update a sink:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_update]
    :end-before: [END sink_update]
    :dedent: 4

Delete a sink:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_delete]
    :end-before: [END sink_delete]
    :dedent: 4


