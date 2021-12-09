Direct Library Usage
====================

Although the recommended way of using the :mod:`google-cloud-logging` library
is to integrate it with the :doc:`Python logging standard library</std-lib-integration>`,
you can also use the library to interact with the Googel Cloud Logging API 
directly.

In addition to writing logs, using the library in this way allows you to manage 
:doc:`logs</entries>`, :doc:`sinks</sink>`, :doc:`metrics</metric>`, and other resources.

Creating a Client
-----------------
http vs grpc
create logger
loggers will have associated resource
can attach labels to logger

Writing Log Entries
-------------------

Retriving Log Entries
---------------------

Fetch entries for the default project.

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START client_list_entries_default]
    :end-before: [END client_list_entries_default]
    :dedent: 4

Entries returned by
:meth:`Client.list_entries <google.cloud.logging.client.Client.list_entries>`
or
:meth:`Logger.list_entries <google.cloud.logging.logger.Logger.list_entries>`
will be instances of one of the following classes:

- :class:`~google.cloud.logging.entries.TextEntry`
- :class:`~google.cloud.logging.entries.StructEntry`
- :class:`~google.cloud.logging.entries.ProtobufEntry`

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


