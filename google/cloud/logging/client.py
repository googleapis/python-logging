# Copyright 2016 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Client for interacting with the Google Stackdriver Logging API."""

import logging
import os

try:
    from google.cloud.logging import _gapic
except ImportError:  # pragma: NO COVER
    _HAVE_GRPC = False
    _gapic = None
else:
    _HAVE_GRPC = True

import google.api_core.client_options
from google.cloud.client import ClientWithProject
from google.cloud.environment_vars import DISABLE_GRPC
from google.cloud.logging._helpers import _add_defaults_to_filter
from google.cloud.logging._helpers import retrieve_metadata_server
from google.cloud.logging._http import Connection
from google.cloud.logging._http import _LoggingAPI as JSONLoggingAPI
from google.cloud.logging._http import _MetricsAPI as JSONMetricsAPI
from google.cloud.logging._http import _SinksAPI as JSONSinksAPI
from google.cloud.logging.handlers import CloudLoggingHandler
from google.cloud.logging.handlers import AppEngineHandler
from google.cloud.logging.handlers import ContainerEngineHandler
from google.cloud.logging.handlers import setup_logging
from google.cloud.logging.handlers.handlers import EXCLUDED_LOGGER_DEFAULTS

from google.cloud.logging.logger import Logger
from google.cloud.logging.metric import Metric
from google.cloud.logging.sink import Sink


_DISABLE_GRPC = os.getenv(DISABLE_GRPC, False)
_USE_GRPC = _HAVE_GRPC and not _DISABLE_GRPC

_APPENGINE_FLEXIBLE_ENV_VM = "GAE_APPENGINE_HOSTNAME"
"""Environment variable set in App Engine when vm:true is set."""

_APPENGINE_INSTANCE_ID = "GAE_INSTANCE"
"""Environment variable set in App Engine standard and flexible environment."""

_GKE_CLUSTER_NAME = "instance/attributes/cluster-name"
"""Attribute in metadata server when in GKE environment."""


class Client(ClientWithProject):
    """Client to bundle configuration needed for API requests.

    :type project: str
    :param project: the project which the client acts on behalf of.
                    If not passed, falls back to the default inferred
                    from the environment.

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        client. If not passed (and if no ``_http`` object is
                        passed), falls back to the default inferred from the
                        environment.

    :type _http: :class:`~requests.Session`
    :param _http: (Optional) HTTP object to make requests. Can be any object
                  that defines ``request()`` with the same interface as
                  :meth:`requests.Session.request`. If not passed, an
                  ``_http`` object is created that is bound to the
                  ``credentials`` for the current object.
                  This parameter should be considered private, and could
                  change in the future.

    :type _use_grpc: bool
    :param _use_grpc: (Optional) Explicitly specifies whether
                      to use the gRPC transport or HTTP. If unset,
                      falls back to the ``GOOGLE_CLOUD_DISABLE_GRPC``
                      environment variable
                      This parameter should be considered private, and could
                      change in the future.

    :type client_info:
        :class:`google.api_core.client_info.ClientInfo` or
        :class:`google.api_core.gapic_v1.client_info.ClientInfo`
    :param client_info:
        The client info used to send a user-agent string along with API
        requests. If ``None``, then default info will be used. Generally,
        you only need to set this if you're developing your own library
        or partner tool.
    :type client_options: :class:`~google.api_core.client_options.ClientOptions`
        or :class:`dict`
    :param client_options: (Optional) Client options used to set user options
        on the client. API Endpoint should be set through client_options.
    """

    _logging_api = None
    _sinks_api = None
    _metrics_api = None

    SCOPE = (
        "https://www.googleapis.com/auth/logging.read",
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/logging.admin",
        "https://www.googleapis.com/auth/cloud-platform",
    )
    """The scopes required for authenticating as a Logging consumer."""

    def __init__(
        self,
        project=None,
        credentials=None,
        _http=None,
        _use_grpc=None,
        client_info=None,
        client_options=None,
    ):
        super(Client, self).__init__(
            project=project,
            credentials=credentials,
            _http=_http,
            client_options=client_options,
        )

        kw_args = {"client_info": client_info}
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint
                kw_args["api_endpoint"] = api_endpoint

        self._connection = Connection(self, **kw_args)

        self._client_info = client_info
        if _use_grpc is None:
            self._use_grpc = _USE_GRPC
        else:
            self._use_grpc = _use_grpc

    @property
    def logging_api(self):
        """Helper for logging-related API calls.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.logs
        """
        if self._logging_api is None:
            if self._use_grpc:
                self._logging_api = _gapic.make_logging_api(self)
            else:
                self._logging_api = JSONLoggingAPI(self)
        return self._logging_api

    @property
    def sinks_api(self):
        """Helper for log sink-related API calls.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.sinks
        """
        if self._sinks_api is None:
            if self._use_grpc:
                self._sinks_api = _gapic.make_sinks_api(self)
            else:
                self._sinks_api = JSONSinksAPI(self)
        return self._sinks_api

    @property
    def metrics_api(self):
        """Helper for log metric-related API calls.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.metrics
        """
        if self._metrics_api is None:
            if self._use_grpc:
                self._metrics_api = _gapic.make_metrics_api(self)
            else:
                self._metrics_api = JSONMetricsAPI(self)
        return self._metrics_api

    def logger(self, name):
        """Creates a logger bound to the current client.

        :type name: str
        :param name: the name of the logger to be constructed.

        :rtype: :class:`google.cloud.logging.logger.Logger`
        :returns: Logger created with the current client.
        """
        return Logger(name, client=self)

    def list_entries(
        self,
        projects=None,
        filter_=None,
        order_by=None,
        page_size=None,
        page_token=None,
    ):
        """Return a page of log entries.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/list

        :type projects: list of strings
        :param projects: project IDs to include. If not passed,
                            defaults to the project bound to the client.

        :type filter_: str
        :param filter_:
            a filter expression. See
            https://cloud.google.com/logging/docs/view/advanced_filters
            By default, a 24 hour filter is applied.

        :type order_by: str
        :param order_by: One of :data:`~google.cloud.logging.ASCENDING`
                         or :data:`~google.cloud.logging.DESCENDING`.

        :type page_size: int
        :param page_size:
            Optional. The maximum number of entries in each page of results
            from this request. Non-positive values are ignored. Defaults
            to a sensible value set by the API.

        :type page_token: str
        :param page_token:
            Optional. If present, return the next batch of entries, using
            the value, which must correspond to the ``nextPageToken`` value
            returned in the previous response.  Deprecated: use the ``pages``
            property of the returned iterator instead of manually passing
            the token.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns: Iterator of :class:`~google.cloud.logging.entries._BaseEntry`
                  accessible to the current client.
        """
        if projects is None:
            projects = [self.project]

        filter_ = _add_defaults_to_filter(filter_)

        return self.logging_api.list_entries(
            projects=projects,
            filter_=filter_,
            order_by=order_by,
            page_size=page_size,
            page_token=page_token,
        )

    def sink(self, name, filter_=None, destination=None):
        """Creates a sink bound to the current client.

        :type name: str
        :param name: the name of the sink to be constructed.

        :type filter_: str
        :param filter_: (optional) the advanced logs filter expression
                        defining the entries exported by the sink.  If not
                        passed, the instance should already exist, to be
                        refreshed via :meth:`Sink.reload`.

        :type destination: str
        :param destination: destination URI for the entries exported by
                            the sink.  If not passed, the instance should
                            already exist, to be refreshed via
                            :meth:`Sink.reload`.

        :rtype: :class:`google.cloud.logging.sink.Sink`
        :returns: Sink created with the current client.
        """
        return Sink(name, filter_, destination, client=self)

    def list_sinks(self, page_size=None, page_token=None):
        """List sinks for the project associated with this client.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.sinks/list

        :type page_size: int
        :param page_size:
            Optional. The maximum number of sinks in each page of results from
            this request. Non-positive values are ignored. Defaults to a
            sensible value set by the API.

        :type page_token: str
        :param page_token:
            Optional. If present, return the next batch of sinks, using the
            value, which must correspond to the ``nextPageToken`` value
            returned in the previous response.  Deprecated: use the ``pages``
            property of the returned iterator instead of manually passing the
            token.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns: Iterator of
                  :class:`~google.cloud.logging.sink.Sink`
                  accessible to the current client.
        """
        return self.sinks_api.list_sinks(self.project, page_size, page_token)

    def metric(self, name, filter_=None, description=""):
        """Creates a metric bound to the current client.

        :type name: str
        :param name: the name of the metric to be constructed.

        :type filter_: str
        :param filter_: the advanced logs filter expression defining the
                        entries tracked by the metric.  If not
                        passed, the instance should already exist, to be
                        refreshed via :meth:`Metric.reload`.

        :type description: str
        :param description: the description of the metric to be constructed.
                            If not passed, the instance should already exist,
                            to be refreshed via :meth:`Metric.reload`.

        :rtype: :class:`google.cloud.logging.metric.Metric`
        :returns: Metric created with the current client.
        """
        return Metric(name, filter_, client=self, description=description)

    def list_metrics(self, page_size=None, page_token=None):
        """List metrics for the project associated with this client.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.metrics/list

        :type page_size: int
        :param page_size:
            Optional. The maximum number of metrics in each page of results
            from this request. Non-positive values are ignored. Defaults to a
            sensible value set by the API.

        :type page_token: str
        :param page_token:
            Optional. If present, return the next batch of metrics, using the
            value, which must correspond to the ``nextPageToken`` value
            returned in the previous response.  Deprecated: use the ``pages``
            property of the returned iterator instead of manually passing the
            token.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns: Iterator of :class:`~google.cloud.logging.metric.Metric`
                  accessible to the current client.
        """
        return self.metrics_api.list_metrics(self.project, page_size, page_token)

    def get_default_handler(self, **kw):
        """Return the default logging handler based on the local environment.

        :type kw: dict
        :param kw: keyword args passed to handler constructor

        :rtype: :class:`logging.Handler`
        :returns: The default log handler based on the environment
        """
        gke_cluster_name = retrieve_metadata_server(_GKE_CLUSTER_NAME)

        if (
            _APPENGINE_FLEXIBLE_ENV_VM in os.environ
            or _APPENGINE_INSTANCE_ID in os.environ
        ):
            return AppEngineHandler(self, **kw)
        elif gke_cluster_name is not None:
            return ContainerEngineHandler(**kw)
        else:
            return CloudLoggingHandler(self, **kw)

    def setup_logging(
        self, log_level=logging.INFO, excluded_loggers=EXCLUDED_LOGGER_DEFAULTS, **kw
    ):
        """Attach default Stackdriver logging handler to the root logger.

        This method uses the default log handler, obtained by
        :meth:`~get_default_handler`, and attaches it to the root Python
        logger, so that a call such as ``logging.warn``, as well as all child
        loggers, will report to Stackdriver logging.

        :type log_level: int
        :param log_level: (Optional) Python logging log level. Defaults to
                          :const:`logging.INFO`.

        :type excluded_loggers: tuple
        :param excluded_loggers: (Optional) The loggers to not attach the
                                 handler to. This will always include the
                                 loggers in the path of the logging client
                                 itself.

        :type kw: dict
        :param kw: keyword args passed to handler constructor
        """
        handler = self.get_default_handler(**kw)
        setup_logging(handler, log_level=log_level, excluded_loggers=excluded_loggers)
