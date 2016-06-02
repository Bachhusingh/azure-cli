#pylint: skip-file
# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator 0.16.0.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.pipeline import ClientRawResponse
from msrestazure.azure_exceptions import CloudError
from msrestazure.azure_operation import AzureOperationPoller
import uuid

from .. import models


class VMOperations(object):
    """VMOperations operations.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An objec model deserializer.
    """

    def __init__(self, client, config, serializer, deserializer):

        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer

        self.config = config

    def create_or_update(
            self, resource_group_name, deployment_name, admin_username, name, content_version=None, admin_password=None, authentication_type="password", availability_set_id=None, availability_set_type="none", dns_name_for_public_ip=None, dns_name_type="none", location=None, network_security_group_name=None, network_security_group_rule="RDP", network_security_group_type="new", os_disk_name="osdiskimage", os_disk_uri=None, os_offer="WindowsServer", os_publisher="MicrosoftWindowsServer", os_sku="2012-R2-Datacenter", os_type="Win2012R2Datacenter", os_version="latest", private_ip_address=None, private_ip_address_allocation="dynamic", public_ip_address_allocation="dynamic", public_ip_address_name=None, public_ip_address_type="new", size="Standard_A2", ssh_dest_key_path=None, ssh_key_value=None, storage_account_name=None, storage_account_type="new", storage_container_name="vhds", storage_redundancy_type="Standard_LRS", subnet_ip_address_prefix="10.0.0.0/24", subnet_name=None, virtual_network_ip_address_prefix="10.0.0.0/16", virtual_network_name=None, virtual_network_type="new", custom_headers={}, raw=False, **operation_config):
        """
        Create or update a virtual machine.

        :param resource_group_name: The name of the resource group. The name
         is case insensitive.
        :type resource_group_name: str
        :param deployment_name: The name of the deployment.
        :type deployment_name: str
        :param admin_username: Username for the Virtual Machine.
        :type admin_username: str
        :param name: The VM name.
        :type name: str
        :param content_version: If included it must match the ContentVersion
         in the template.
        :type content_version: str
        :param admin_password: Password for the Virtual Machine.  Required if
         SSH (Linux only) is not specified.
        :type admin_password: str
        :param authentication_type: Password or SSH Public Key
         authentication. Possible values include: 'password', 'ssh'
        :type authentication_type: str
        :param availability_set_id: Existing availability set for the VM.
        :type availability_set_id: str
        :param availability_set_type: Flag to add the VM to an existing
         availability set. Possible values include: 'none', 'existing'
        :type availability_set_type: str
        :param dns_name_for_public_ip: Globally unique DNS Name for the
         Public IP used to access the Virtual Machine.  Requires a new public
         IP to be created by setting Public IP Address Type to New.
        :type dns_name_for_public_ip: str
        :param dns_name_type: Associate VMs with a public IP address to a DNS
         name. Possible values include: 'none', 'new'
        :type dns_name_type: str
        :param location: Location for VM resources.
        :type location: str
        :param network_security_group_name: Name of the network security
         group.
        :type network_security_group_name: str
        :param network_security_group_rule: The type of rule to add to a new
         network security group. Possible values include: 'RDP', 'SSH'
        :type network_security_group_rule: str
        :param network_security_group_type: Whether to use a network security
         group or not. Possible values include: 'new', 'existing', 'none'
        :type network_security_group_type: str
        :param os_disk_name: Name of new VM OS disk.
        :type os_disk_name: str
        :param os_disk_uri: URI for a custom VHD image.
        :type os_disk_uri: str
        :param os_offer: The OS Offer to install.
        :type os_offer: str
        :param os_publisher: The OS publisher of the OS image.
        :type os_publisher: str
        :param os_sku: The OS SKU to install.
        :type os_sku: str
        :param os_type: Common OS choices.  Choose 'Custom' to specify an
         image with the osPublisher, osOffer, osSKU, and osVersion
         parameters. Possible values include: 'Win2012R2Datacenter',
         'Win2012Datacenter', 'Win2008R2SP1', 'Custom'
        :type os_type: str
        :param os_version: The OS version to install.
        :type os_version: str
        :param private_ip_address: The private IP address to use with Private
         IP Address Allocation type Static.
        :type private_ip_address: str
        :param private_ip_address_allocation: Private IP address allocation
         method. Possible values include: 'dynamic', 'static'
        :type private_ip_address_allocation: str
        :param public_ip_address_allocation: Public IP address allocation
         method. Possible values include: 'dynamic', 'static'
        :type public_ip_address_allocation: str
        :param public_ip_address_name: Name of public IP address to use.
        :type public_ip_address_name: str
        :param public_ip_address_type: Use a public IP Address for the VM
         Nic. Possible values include: 'none', 'new', 'existing'
        :type public_ip_address_type: str
        :param size: The VM Size that should be created.  See
         https://azure.microsoft.com/en-us/pricing/details/virtual-machines/
         for size info.
        :type size: str
        :param ssh_dest_key_path: Destination file path on VM for SSH key.
        :type ssh_dest_key_path: str
        :param ssh_key_value: SSH key file data.
        :type ssh_key_value: str
        :param storage_account_name: Name of storage account for the VM OS
         disk.
        :type storage_account_name: str
        :param storage_account_type: Whether to use an existing storage
         account or create a new one. Possible values include: 'new',
         'existing'
        :type storage_account_type: str
        :param storage_container_name: Name of storage container for the VM
         OS disk.
        :type storage_container_name: str
        :param storage_redundancy_type: The VM storage type (Standard_LRS,
         Standard_GRS, Standard_RAGRS).
        :type storage_redundancy_type: str
        :param subnet_ip_address_prefix: The subnet address prefix in CIDR
         format.
        :type subnet_ip_address_prefix: str
        :param subnet_name: The subnet name.
        :type subnet_name: str
        :param virtual_network_ip_address_prefix: The virtual network IP
         address prefix in CIDR format.
        :type virtual_network_ip_address_prefix: str
        :param virtual_network_name: Name of virtual network to add VM to.
        :type virtual_network_name: str
        :param virtual_network_type: Whether to use an existing VNet or
         create a new one. Possible values include: 'new', 'existing'
        :type virtual_network_type: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :rtype:
         :class:`AzureOperationPoller<msrestazure.azure_operation.AzureOperationPoller>`
         instance that returns :class:`DeploymentExtended
         <mynamespace.models.DeploymentExtended>`
        :rtype: :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>`
         if raw=true
        """
        parameters = models.DeploymentVM(content_version=content_version, admin_password=admin_password, admin_username=admin_username, authentication_type=authentication_type, availability_set_id=availability_set_id, availability_set_type=availability_set_type, dns_name_for_public_ip=dns_name_for_public_ip, dns_name_type=dns_name_type, location=location, name=name, network_security_group_name=network_security_group_name, network_security_group_rule=network_security_group_rule, network_security_group_type=network_security_group_type, os_disk_name=os_disk_name, os_disk_uri=os_disk_uri, os_offer=os_offer, os_publisher=os_publisher, os_sku=os_sku, os_type=os_type, os_version=os_version, private_ip_address=private_ip_address, private_ip_address_allocation=private_ip_address_allocation, public_ip_address_allocation=public_ip_address_allocation, public_ip_address_name=public_ip_address_name, public_ip_address_type=public_ip_address_type, size=size, ssh_dest_key_path=ssh_dest_key_path, ssh_key_value=ssh_key_value, storage_account_name=storage_account_name, storage_account_type=storage_account_type, storage_container_name=storage_container_name, storage_redundancy_type=storage_redundancy_type, subnet_ip_address_prefix=subnet_ip_address_prefix, subnet_name=subnet_name, virtual_network_ip_address_prefix=virtual_network_ip_address_prefix, virtual_network_name=virtual_network_name, virtual_network_type=virtual_network_type)

        # Construct URL
        url = '/subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/{deploymentName}'
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', max_length=64, min_length=1, pattern='^[-\w\._]+$'),
            'deploymentName': self._serialize.url("deployment_name", deployment_name, 'str', max_length=64, min_length=1, pattern='^[-\w\._]+$'),
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.config.api_version", self.config.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct body
        body_content = self._serialize.body(parameters, 'DeploymentVM')

        # Construct and send request
        def long_running_send():

            request = self._client.put(url, query_parameters)
            return self._client.send(
                request, header_parameters, body_content, **operation_config)

        def get_long_running_status(status_link, headers={}):

            request = self._client.get(status_link)
            request.headers.update(headers)
            return self._client.send(
                request, header_parameters, **operation_config)

        def get_long_running_output(response):

            if response.status_code not in [200, 201]:
                exp = CloudError(response)
                exp.request_id = response.headers.get('x-ms-request-id')
                raise exp

            deserialized = None

            if response.status_code == 200:
                deserialized = self._deserialize('DeploymentExtended', response)
            if response.status_code == 201:
                deserialized = self._deserialize('DeploymentExtended', response)

            if raw:
                client_raw_response = ClientRawResponse(deserialized, response)
                return client_raw_response

            return deserialized

        if raw:
            response = long_running_send()
            return get_long_running_output(response)

        long_running_operation_timeout = operation_config.get(
            'long_running_operation_timeout',
            self.config.long_running_operation_timeout)
        return AzureOperationPoller(
            long_running_send, get_long_running_output,
            get_long_running_status, long_running_operation_timeout)
