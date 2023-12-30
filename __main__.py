import pulumi
import pulumi_oci as oci
import os

# Initialize pulumi config
config = pulumi.Config()


# Create Virtual Cloud Network
vcn = oci.core.Vcn("instance_vcn",
                        cidr_blocks=[config.get('vcn_cidr_block')],
                        compartment_id=config.require('compartment_ocid'),
                        display_name=config.get('vcn_display_name'),
                        dns_label=config.get('vcn_dns_label'),
                        )

# Create Internet Gateway
oci_internet_gateway = oci.core.InternetGateway("ociInternetGateway",
                                                 compartment_id=config.require('compartment_ocid'),
                                                 vcn_id=vcn.id,
                                                 display_name=config.get('internetgateway_name'))

# Create outbound routing table
instance_node_route_table = oci.core.RouteTable("ociRouteTable",
                                                compartment_id=config.require('compartment_ocid'),
                                                vcn_id=vcn.id,
                                                route_rules=[oci.core.RouteTableRouteRuleArgs(
                                                    network_entity_id=oci_internet_gateway.id,
                                                    destination="0.0.0.0/0",
                                                    destination_type="CIDR_BLOCK",
                                                    description=config.get('instance_node_routetable_description')
                                                )])

# Create subnet
node_subnet = oci.core.Subnet("node_subnet",
                              cidr_block=config.get('instance_nodesubnet_cidr'),
                              compartment_id=config.require('compartment_ocid'),
                              vcn_id=vcn.id,
                              display_name=config.get('instance_nodesubnet_displayname'),
                              route_table_id=instance_node_route_table.id,)


# Fetch Availability Domain
get_ad_name = oci.identity.get_availability_domain(compartment_id=config.require('compartment_ocid'),ad_number=config.get('availability_domain_number'))

# Read the public key from a local path
ssh_pub_key=open(os.path.expanduser("~/.ssh/" + config.require('ssh_pubkey_name')),"r").read()

# Create the Instance
oci_instance = oci.core.Instance("oci_instance",
                                         agent_config=oci.core.InstanceAgentConfigArgs(
                                             plugins_configs=[
                                                 oci.core.InstanceAgentConfigPluginsConfigArgs(
                                                     desired_state=config.require('oci_agent_osmgmtsvc'),
                                                     name="OS Management Service Agent",
                                                 ),
                                                 oci.core.InstanceAgentConfigPluginsConfigArgs(
                                                     desired_state=config.require('oci_agent_customlogs'),
                                                     name="Custom Logs Monitoring",
                                                 ),
                                                 oci.core.InstanceAgentConfigPluginsConfigArgs(
                                                     desired_state=config.require('oci_agent_comptinstance'),
                                                     name="Compute Instance Run Command",
                                                 ),
                                                 oci.core.InstanceAgentConfigPluginsConfigArgs(
                                                     desired_state=config.require('oci_agent_comptinstancemonitoring'),
                                                     name="Compute Instance Monitoring",
                                                 ),
                                             ],
                                         ),
                                         availability_domain=get_ad_name.__dict__['name'],
                                         compartment_id=config.require('compartment_ocid'),
                                         create_vnic_details=oci.core.InstanceCreateVnicDetailsArgs(
                                             display_name=config.require('instance_name'),
                                             subnet_id=node_subnet.id,
                                             private_ip=config.require('vcn_private_ip'),
                                         ),
                                         display_name=config.require('instance_name'),
                                         metadata={
                                             "ssh_authorized_keys": ssh_pub_key,
                                         },
                                         shape=config.require('instance_node_shape'),
                                         shape_config=oci.core.InstanceShapeConfigArgs(
                                             memory_in_gbs=config.require('instance_node_memory_in_gbs'),
                                             ocpus=config.require('instance_node_ocpus'),
                                         ),
                                         source_details=oci.core.InstanceSourceDetailsArgs(
                                             boot_volume_size_in_gbs=config.require('instance_bootvolume_size_gb'),
                                             source_id=config.require('instance_node_operating_system_ocid'),
                                             source_type="image",
                                         ),)

pulumi.export("Instance Hostname" ,oci_instance.display_name)
pulumi.export("Instance PublicIP" ,oci_instance.public_ip)
