# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.core import PipelineClient
from azure.core.configuration import Configuration
from azure.core.polling.base_polling import LocationPolling, StatusCheckPolling
from abc import abstractmethod

from ._poller import AAZNoPolling, AAZBasePolling
from azure.cli.core.cloud import CloudNameEnum as _CloudNameEnum

registered_clients = {}
CloudNameEnum = _CloudNameEnum  # redefine CloudNameEnum in aaz to decouple with cloud for aaz generated commands.

# pylint: disable=too-many-instance-attributes, too-few-public-methods, protected-access


def register_client(name):
    def decorator(cls):
        if name in registered_clients:
            assert registered_clients[name] == cls
        else:
            registered_clients[name] = cls
        return cls

    return decorator


class AAZClientConfiguration(Configuration):
    def __init__(self, credential, credential_scopes, **kwargs):
        if credential is None:
            raise ValueError("Parameter 'credential' must not be None.")
        if not credential_scopes:
            raise ValueError("Parameter 'credential_scopes' is required.")
        super().__init__(**kwargs)
        self.credential = credential
        self.credential_scopes = credential_scopes
        self._configure(**kwargs)

    def _configure(
            self,
            **kwargs
    ):
        from azure.core.pipeline.policies import UserAgentPolicy, HeadersPolicy, ProxyPolicy, \
            RetryPolicy, CustomHookPolicy, RedirectPolicy, SansIOHTTPPolicy
        from azure.cli.core.sdk.policies import SafeNetworkTraceLoggingPolicy
        from ._http_policy import AAZBearerTokenCredentialPolicy

        self.user_agent_policy = kwargs.get('user_agent_policy') or UserAgentPolicy(**kwargs)
        self.headers_policy = kwargs.get('headers_policy') or HeadersPolicy(**kwargs)
        self.proxy_policy = kwargs.get('proxy_policy') or ProxyPolicy(**kwargs)
        self.logging_policy = kwargs.get('logging_policy') or SafeNetworkTraceLoggingPolicy(**kwargs)
        self.http_logging_policy = kwargs.get('http_logging_policy') or SansIOHTTPPolicy()
        self.retry_policy = kwargs.get('retry_policy') or RetryPolicy(**kwargs)
        self.custom_hook_policy = kwargs.get('custom_hook_policy') or CustomHookPolicy(**kwargs)
        self.redirect_policy = kwargs.get('redirect_policy') or RedirectPolicy(**kwargs)
        self.authentication_policy = kwargs.get('authentication_policy')
        if self.credential and not self.authentication_policy:
            self.authentication_policy = AAZBearerTokenCredentialPolicy(
                self.credential, *self.credential_scopes, **kwargs)


class AAZBaseClient(PipelineClient):
    """Base Client"""

    def __init__(self, ctx, credential, **kwargs):
        super().__init__(
            base_url=self._build_base_url(ctx, **kwargs),
            config=self._build_configuration(ctx, credential, **kwargs),
            per_call_policies=self._build_per_call_policies(ctx, **kwargs)
        )

    @classmethod
    @abstractmethod
    def _build_base_url(cls, ctx, **kwargs):
        """Provide a complete url. Supports placeholder added"""
        # return "https://{KeyVaultName}" + ctx.cli_ctx.cloud.suffixes.keyvault_dns
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def _build_configuration(cls, ctx, credential, **kwargs):
        """Provide client configuration"""
        # return AAZClientConfiguration(
        #     credential=credential,
        #     credential_scopes=<credential_scopes>,
        #     **kwargs
        # )
        raise NotImplementedError()

    @classmethod
    def _build_per_call_policies(cls, ctx, **kwargs):  # pylint: disable=unused-argument
        return []

    def send_request(self, request, stream=False, **kwargs):  # pylint: disable=arguments-differ
        session = self._pipeline.run(request, stream=stream, **kwargs)
        return session

    def build_lro_polling(self, no_wait, initial_session, deserialization_callback, error_callback,
                          lro_options=None, path_format_arguments=None):
        from azure.core.polling.base_polling import OperationResourcePolling
        if no_wait == True:  # noqa: E712, pylint: disable=singleton-comparison
            polling = AAZNoPolling()
        else:
            polling = AAZBasePolling(
                lro_options=lro_options,
                lro_algorithms=[
                    OperationResourcePolling(lro_options=lro_options),
                    LocationPolling(),
                    StatusCheckPolling(),
                ],
                path_format_arguments=path_format_arguments,
                http_response_error_callback=error_callback,
            )

        polling.initialize(
            self,
            initial_response=initial_session,
            deserialization_callback=deserialization_callback
        )
        return polling


@register_client("MgmtClient")
class AAZMgmtClient(AAZBaseClient):
    """Management Client for Management Plane APIs"""

    @classmethod
    def _build_base_url(cls, ctx, **kwargs):
        return ctx.cli_ctx.cloud.endpoints.resource_manager

    @classmethod
    def _build_configuration(cls, ctx, credential, **kwargs):
        from azure.cli.core.auth.util import resource_to_scopes
        return AAZClientConfiguration(
            credential=credential,
            credential_scopes=resource_to_scopes(ctx.cli_ctx.cloud.endpoints.active_directory_resource_id),
            **kwargs
        )

    @classmethod
    def _build_per_call_policies(cls, ctx, **kwargs):
        from azure.mgmt.core.policies import ARMAutoResourceProviderRegistrationPolicy
        return [ARMAutoResourceProviderRegistrationPolicy()]

    def build_lro_polling(self, no_wait, initial_session, deserialization_callback, error_callback,
                          lro_options=None, path_format_arguments=None):
        from azure.mgmt.core.polling.arm_polling import AzureAsyncOperationPolling, BodyContentPolling
        if no_wait == True:  # noqa: E712, pylint: disable=singleton-comparison
            polling = AAZNoPolling()
        else:
            polling = AAZBasePolling(
                lro_options=lro_options,
                lro_algorithms=[
                    AzureAsyncOperationPolling(lro_options=lro_options),
                    LocationPolling(),
                    BodyContentPolling(),
                    StatusCheckPolling(),
                ],
                path_format_arguments=path_format_arguments,
                http_response_error_callback=error_callback,
            )

        polling.initialize(
            self,
            initial_response=initial_session,
            deserialization_callback=deserialization_callback
        )
        return polling
