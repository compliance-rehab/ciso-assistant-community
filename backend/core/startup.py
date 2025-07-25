import os

from django.apps import AppConfig
from django.core.management import call_command
from django.db.models.signals import post_migrate
from structlog import get_logger

from ciso_assistant.settings import CISO_ASSISTANT_SUPERUSER_EMAIL
from core.utils import RoleCodename, UserGroupCodename

logger = get_logger(__name__)

READER_PERMISSIONS_LIST = [
    "view_appliedcontrol",
    "view_asset",
    "view_complianceassessment",
    "view_entity",
    "view_entityassessment",
    "view_evidence",
    "view_folder",
    "view_framework",
    "view_loadedlibrary",
    "view_policy",
    "view_perimeter",
    "view_referencecontrol",
    "view_representative",
    "view_requirementassessment",
    "view_requirementmapping",
    "view_requirementmappingset",
    "view_requirementnode",
    "view_riskacceptance",
    "view_riskassessment",
    "view_riskmatrix",
    "view_riskscenario",
    "view_solution",
    "view_storedlibrary",
    "view_threat",
    "view_vulnerability",
    "view_user",
    "view_usergroup",
    "view_ebiosrmstudy",
    "view_fearedevent",
    "view_roto",
    "view_stakeholder",
    "view_strategicscenario",
    "view_attackpath",
    "view_operationalscenario",
    "view_qualification",
    "view_globalsettings",
    "view_securityexception",
    "view_finding",
    "view_findingsassessment",
    "view_incident",
    "view_timelineentry",
    "view_tasknode",
    "view_tasktemplate",
    "view_businessimpactanalysis",
    "view_assetassessment",
    "view_escalationthreshold",
    "view_assetclass",
    # privacy,
    "view_processing",
    "view_processingnature",
    "view_purpose",
    "view_personaldata",
    "view_datasubject",
    "view_datarecipient",
    "view_datacontractor",
    "view_datatransfer",
    # campaigns,
    "view_campaign",
    # operating modes
    "view_elementaryaction",
    "view_operatingmode",
    "view_killchain",
]

APPROVER_PERMISSIONS_LIST = [
    "view_perimeter",
    "view_riskassessment",
    "view_appliedcontrol",
    "view_policy",
    "view_riskscenario",
    "view_riskacceptance",
    "approve_riskacceptance",
    "view_asset",
    "view_threat",
    "view_vulnerability",
    "view_referencecontrol",
    "view_folder",
    "view_usergroup",
    "view_riskmatrix",
    "view_complianceassessment",
    "view_requirementassessment",
    "view_requirementnode",
    "view_evidence",
    "view_framework",
    "view_storedlibrary",
    "view_loadedlibrary",
    "view_user",
    "view_requirementmappingset",
    "view_requirementmapping",
    "view_ebiosrmstudy",
    "view_fearedevent",
    "view_roto",
    "view_stakeholder",
    "view_strategicscenario",
    "view_attackpath",
    "view_operationalscenario",
    "view_qualification",
    "view_globalsettings",
    "view_securityexception",
    "view_finding",
    "view_findingsassessment",
    "view_incident",
    "view_timelineentry",
    "view_tasknode",
    "view_tasktemplate",
    "view_businessimpactanalysis",
    "view_assetassessment",
    "view_escalationthreshold",
    "view_assetclass",
    # campaigns,
    "view_campaign",
    # privacy,
    "view_processing",
    "view_processingnature",
    "view_purpose",
    "view_personaldata",
    "view_datasubject",
    "view_datarecipient",
    "view_datacontractor",
    "view_datatransfer",
    # operating modes
    "view_elementaryaction",
    "view_operatingmode",
    "view_killchain",
]

ANALYST_PERMISSIONS_LIST = [
    "add_filteringlabel",
    "view_filteringlabel",
    "add_appliedcontrol",
    "add_asset",
    "add_complianceassessment",
    "add_evidence",
    "add_policy",
    "add_perimeter",
    "add_riskacceptance",
    "add_riskassessment",
    "add_riskscenario",
    "add_solution",
    "add_threat",
    "add_vulnerability",
    "change_appliedcontrol",
    "change_asset",
    "change_complianceassessment",
    "change_entity",
    "change_entityassessment",
    "change_evidence",
    "change_policy",
    "change_perimeter",
    "change_referencecontrol",
    "change_vulnerability",
    "change_representative",
    "change_requirementassessment",
    "change_riskacceptance",
    "change_riskassessment",
    "change_riskscenario",
    "change_solution",
    "change_threat",
    "delete_appliedcontrol",
    "delete_asset",
    "delete_complianceassessment",
    "delete_entity",
    "delete_entityassessment",
    "delete_evidence",
    "delete_policy",
    "delete_perimeter",
    "delete_referencecontrol",
    "delete_vulnerability",
    "delete_representative",
    "delete_riskacceptance",
    "delete_riskassessment",
    "delete_riskscenario",
    "delete_solution",
    "delete_threat",
    "view_appliedcontrol",
    "view_asset",
    "view_complianceassessment",
    "view_entity",
    "view_entityassessment",
    "view_evidence",
    "view_folder",
    "view_framework",
    "view_loadedlibrary",
    "view_policy",
    "view_perimeter",
    "view_referencecontrol",
    "view_vulnerability",
    "view_representative",
    "view_requirementassessment",
    "view_requirementmapping",
    "view_requirementmappingset",
    "view_requirementnode",
    "view_riskacceptance",
    "view_riskassessment",
    "view_riskmatrix",
    "view_riskscenario",
    "view_solution",
    "view_storedlibrary",
    "view_threat",
    "view_user",
    "view_usergroup",
    "add_ebiosrmstudy",
    "view_ebiosrmstudy",
    "change_ebiosrmstudy",
    "delete_ebiosrmstudy",
    "add_fearedevent",
    "view_fearedevent",
    "change_fearedevent",
    "delete_fearedevent",
    "add_roto",
    "view_roto",
    "change_roto",
    "delete_roto",
    "add_stakeholder",
    "view_stakeholder",
    "change_stakeholder",
    "delete_stakeholder",
    "add_strategicscenario",
    "view_strategicscenario",
    "change_strategicscenario",
    "delete_strategicscenario",
    "add_attackpath",
    "view_attackpath",
    "change_attackpath",
    "delete_attackpath",
    "add_operationalscenario",
    "view_operationalscenario",
    "change_operationalscenario",
    "delete_operationalscenario",
    "view_qualification",
    "view_globalsettings",
    "view_securityexception",
    "add_securityexception",
    "change_securityexception",
    "delete_securityexception",
    "add_finding",
    "view_finding",
    "change_finding",
    "delete_finding",
    "add_findingsassessment",
    "view_findingsassessment",
    "change_findingsassessment",
    "delete_findingsassessment",
    "add_incident",
    "view_incident",
    "change_incident",
    "delete_incident",
    "add_timelineentry",
    "view_timelineentry",
    "change_timelineentry",
    "delete_timelineentry",
    # tasks
    "add_tasktemplate",
    "view_tasktemplate",
    "change_tasktemplate",
    "delete_tasktemplate",
    "view_tasknode",
    "change_tasknode",
    "delete_tasknode",
    # resilience,
    "add_businessimpactanalysis",
    "view_businessimpactanalysis",
    "change_businessimpactanalysis",
    "delete_businessimpactanalysis",
    "add_escalationthreshold",
    "view_escalationthreshold",
    "change_escalationthreshold",
    "delete_escalationthreshold",
    "add_assetassessment",
    "view_assetassessment",
    "change_assetassessment",
    "delete_assetassessment",
    "view_assetclass",
    # campaigns,
    "view_campaign",
    # privacy,
    "add_processing",
    "change_processing",
    "view_processing",
    "delete_processing",
    "view_processingnature",
    "add_purpose",
    "change_purpose",
    "view_purpose",
    "delete_purpose",
    "add_personaldata",
    "change_personaldata",
    "view_personaldata",
    "delete_personaldata",
    "add_datasubject",
    "change_datasubject",
    "view_datasubject",
    "delete_datasubject",
    "add_datarecipient",
    "change_datarecipient",
    "view_datarecipient",
    "delete_datarecipient",
    "add_datacontractor",
    "change_datacontractor",
    "view_datacontractor",
    "delete_datacontractor",
    "add_datatransfer",
    "change_datatransfer",
    "view_datatransfer",
    "delete_datatransfer",
    # operating modes
    "view_elementaryaction",
    "add_elementaryaction",
    "change_elementaryaction",
    "delete_elementaryaction",
    "view_operatingmode",
    "add_operatingmode",
    "change_operatingmode",
    "delete_operatingmode",
    "view_killchain",
    "add_killchain",
    "change_killchain",
    "delete_killchain",
]

DOMAIN_MANAGER_PERMISSIONS_LIST = [
    "add_filteringlabel",
    "view_filteringlabel",
    "add_appliedcontrol",
    "add_asset",
    "add_complianceassessment",
    "add_entity",
    "add_entityassessment",
    "add_evidence",
    "add_folder",
    "add_policy",
    "add_perimeter",
    "add_riskacceptance",
    "add_riskassessment",
    "add_riskmatrix",
    "add_riskscenario",
    "add_solution",
    "add_threat",
    "change_appliedcontrol",
    "change_asset",
    "change_complianceassessment",
    "change_entity",
    "change_entityassessment",
    "change_evidence",
    "change_folder",
    "change_policy",
    "change_perimeter",
    "change_referencecontrol",
    "change_representative",
    "change_requirementassessment",
    "change_riskacceptance",
    "change_riskassessment",
    "change_riskmatrix",
    "change_riskscenario",
    "change_solution",
    "change_threat",
    "delete_appliedcontrol",
    "delete_asset",
    "delete_complianceassessment",
    "delete_entity",
    "delete_entityassessment",
    "delete_evidence",
    "delete_folder",
    "delete_policy",
    "delete_perimeter",
    "delete_referencecontrol",
    "delete_representative",
    "delete_riskacceptance",
    "delete_riskassessment",
    "delete_riskmatrix",
    "add_vulnerability",
    "view_vulnerability",
    "change_vulnerability",
    "delete_vulnerability",
    "delete_riskscenario",
    "delete_solution",
    "delete_threat",
    "view_appliedcontrol",
    "view_asset",
    "view_complianceassessment",
    "view_entity",
    "view_entityassessment",
    "view_evidence",
    "view_folder",
    "view_framework",
    "view_loadedlibrary",
    "view_policy",
    "view_perimeter",
    "view_referencecontrol",
    "view_representative",
    "view_requirementassessment",
    "view_requirementmapping",
    "view_requirementmappingset",
    "view_requirementnode",
    "view_riskacceptance",
    "view_riskassessment",
    "view_riskmatrix",
    "view_riskscenario",
    "view_solution",
    "view_storedlibrary",
    "view_threat",
    "view_user",
    "view_usergroup",
    "add_ebiosrmstudy",
    "view_ebiosrmstudy",
    "change_ebiosrmstudy",
    "delete_ebiosrmstudy",
    "add_fearedevent",
    "view_fearedevent",
    "change_fearedevent",
    "delete_fearedevent",
    "add_roto",
    "view_roto",
    "change_roto",
    "delete_roto",
    "add_stakeholder",
    "view_stakeholder",
    "change_stakeholder",
    "delete_stakeholder",
    "add_strategicscenario",
    "view_strategicscenario",
    "change_strategicscenario",
    "delete_strategicscenario",
    "add_attackpath",
    "view_attackpath",
    "change_attackpath",
    "delete_attackpath",
    "add_operationalscenario",
    "view_operationalscenario",
    "change_operationalscenario",
    "delete_operationalscenario",
    "view_qualification",
    "view_globalsettings",
    "view_securityexception",
    "add_securityexception",
    "change_securityexception",
    "delete_securityexception",
    "add_finding",
    "view_finding",
    "change_finding",
    "delete_finding",
    "add_findingsassessment",
    "view_findingsassessment",
    "change_findingsassessment",
    "delete_findingsassessment",
    "add_incident",
    "view_incident",
    "change_incident",
    "delete_incident",
    "add_timelineentry",
    "view_timelineentry",
    "change_timelineentry",
    "delete_timelineentry",
    # tasks
    "add_tasktemplate",
    "view_tasktemplate",
    "change_tasktemplate",
    "delete_tasktemplate",
    "view_tasknode",
    "change_tasknode",
    "delete_tasknode",
    # resilience,
    "add_businessimpactanalysis",
    "view_businessimpactanalysis",
    "change_businessimpactanalysis",
    "delete_businessimpactanalysis",
    "add_escalationthreshold",
    "view_escalationthreshold",
    "change_escalationthreshold",
    "delete_escalationthreshold",
    "add_assetassessment",
    "view_assetassessment",
    "change_assetassessment",
    "delete_assetassessment",
    "view_assetclass",
    # campaigns,
    "add_campaign",
    "view_campaign",
    "change_campaign",
    "delete_campaign",
    # privacy,
    "add_processing",
    "change_processing",
    "view_processing",
    "delete_processing",
    "view_processingnature",
    "add_purpose",
    "change_purpose",
    "view_purpose",
    "delete_purpose",
    "add_personaldata",
    "change_personaldata",
    "view_personaldata",
    "delete_personaldata",
    "add_datasubject",
    "change_datasubject",
    "view_datasubject",
    "delete_datasubject",
    "add_datarecipient",
    "change_datarecipient",
    "view_datarecipient",
    "delete_datarecipient",
    "add_datacontractor",
    "change_datacontractor",
    "view_datacontractor",
    "delete_datacontractor",
    "add_datatransfer",
    "change_datatransfer",
    "view_datatransfer",
    "delete_datatransfer",
    # operating modes
    "view_elementaryaction",
    "add_elementaryaction",
    "change_elementaryaction",
    "delete_elementaryaction",
    "view_operatingmode",
    "add_operatingmode",
    "change_operatingmode",
    "delete_operatingmode",
    "view_killchain",
    "add_killchain",
    "change_killchain",
    "delete_killchain",
]

ADMINISTRATOR_PERMISSIONS_LIST = [
    "add_user",
    "view_user",
    "change_user",
    "delete_user",
    "add_usergroup",
    "view_usergroup",
    "change_usergroup",
    "delete_usergroup",
    "add_event",
    "view_event",
    "change_event",
    "delete_event",
    "add_asset",
    "view_asset",
    "change_asset",
    "delete_asset",
    "add_assetclass",
    "view_assetclass",
    "change_assetclass",
    "delete_assetclass",
    "add_threat",
    "view_threat",
    "change_threat",
    "delete_threat",
    "add_referencecontrol",
    "view_referencecontrol",
    "change_referencecontrol",
    "delete_referencecontrol",
    "add_vulnerability",
    "view_vulnerability",
    "change_vulnerability",
    "delete_vulnerability",
    "add_folder",
    "change_folder",
    "view_folder",
    "delete_folder",
    "add_perimeter",
    "change_perimeter",
    "delete_perimeter",
    "view_perimeter",
    "add_riskassessment",
    "view_riskassessment",
    "change_riskassessment",
    "delete_riskassessment",
    "add_appliedcontrol",
    "view_appliedcontrol",
    "change_appliedcontrol",
    "delete_appliedcontrol",
    "add_policy",
    "view_policy",
    "change_policy",
    "delete_policy",
    "add_riskscenario",
    "view_riskscenario",
    "change_riskscenario",
    "delete_riskscenario",
    "add_riskacceptance",
    "view_riskacceptance",
    "change_riskacceptance",
    "delete_riskacceptance",
    "approve_riskacceptance",
    "add_riskmatrix",
    "view_riskmatrix",
    "change_riskmatrix",
    "delete_riskmatrix",
    "add_complianceassessment",
    "view_complianceassessment",
    "change_complianceassessment",
    "delete_complianceassessment",
    "view_requirementassessment",
    "change_requirementassessment",
    "add_evidence",
    "view_evidence",
    "change_evidence",
    "delete_evidence",
    "add_framework",
    "view_framework",
    "delete_framework",
    "view_requirementnode",
    "view_storedlibrary",
    "add_storedlibrary",
    "delete_storedlibrary",
    "view_loadedlibrary",
    "add_loadedlibrary",
    "delete_loadedlibrary",
    "backup",
    "restore",
    "view_globalsettings",
    "change_globalsettings",
    "view_ssosettings",
    "change_ssosettings",
    "view_requirementmappingset",
    "add_requirementmappingset",
    "delete_requirementmappingset",
    "view_requirementmapping",
    "add_entity",
    "change_entity",
    "view_entity",
    "delete_entity",
    "add_representative",
    "change_representative",
    "view_representative",
    "delete_representative",
    "add_solution",
    "change_solution",
    "view_solution",
    "delete_solution",
    "add_entityassessment",
    "change_entityassessment",
    "view_entityassessment",
    "delete_entityassessment",
    "add_filteringlabel",
    "view_filteringlabel",
    "change_filteringlabel",
    "delete_filteringlabel",
    "add_ebiosrmstudy",
    "view_ebiosrmstudy",
    "change_ebiosrmstudy",
    "delete_ebiosrmstudy",
    "add_fearedevent",
    "view_fearedevent",
    "change_fearedevent",
    "delete_fearedevent",
    "add_roto",
    "view_roto",
    "change_roto",
    "delete_roto",
    "add_stakeholder",
    "view_stakeholder",
    "change_stakeholder",
    "delete_stakeholder",
    "add_strategicscenario",
    "view_strategicscenario",
    "change_strategicscenario",
    "delete_strategicscenario",
    "add_attackpath",
    "view_attackpath",
    "change_attackpath",
    "delete_attackpath",
    "add_operationalscenario",
    "view_operationalscenario",
    "change_operationalscenario",
    "delete_operationalscenario",
    "view_elementaryaction",
    "add_elementaryaction",
    "change_elementaryaction",
    "delete_elementaryaction",
    "view_operatingmode",
    "add_operatingmode",
    "change_operatingmode",
    "delete_operatingmode",
    "view_killchain",
    "add_killchain",
    "change_killchain",
    "delete_killchain",
    # qualifications,
    "view_qualification",
    "add_qualification",
    "change_qualification",
    "delete_qualification",
    "view_securityexception",
    "add_securityexception",
    "change_securityexception",
    "delete_securityexception",
    "add_finding",
    "view_finding",
    "change_finding",
    "delete_finding",
    "add_findingsassessment",
    "view_findingsassessment",
    "change_findingsassessment",
    "delete_findingsassessment",
    # privacy,
    "add_processing",
    "change_processing",
    "view_processing",
    "delete_processing",
    "view_processingnature",
    "add_purpose",
    "change_purpose",
    "view_purpose",
    "delete_purpose",
    "add_personaldata",
    "change_personaldata",
    "view_personaldata",
    "delete_personaldata",
    "add_datasubject",
    "change_datasubject",
    "view_datasubject",
    "delete_datasubject",
    "add_datarecipient",
    "change_datarecipient",
    "view_datarecipient",
    "delete_datarecipient",
    "add_datacontractor",
    "change_datacontractor",
    "view_datacontractor",
    "delete_datacontractor",
    "add_datatransfer",
    "change_datatransfer",
    "view_datatransfer",
    "delete_datatransfer",
    # incidents,
    "add_incident",
    "view_incident",
    "change_incident",
    "delete_incident",
    "add_timelineentry",
    "view_timelineentry",
    "change_timelineentry",
    "delete_timelineentry",
    # tasks,
    "add_tasktemplate",
    "view_tasktemplate",
    "change_tasktemplate",
    "delete_tasktemplate",
    "view_tasknode",
    "change_tasknode",
    "delete_tasknode",
    "view_logentry",
    # resilience,
    "add_businessimpactanalysis",
    "view_businessimpactanalysis",
    "change_businessimpactanalysis",
    "delete_businessimpactanalysis",
    "add_escalationthreshold",
    "view_escalationthreshold",
    "change_escalationthreshold",
    "delete_escalationthreshold",
    "add_assetassessment",
    "view_assetassessment",
    "change_assetassessment",
    "delete_assetassessment",
    # campaigns,
    "add_campaign",
    "view_campaign",
    "change_campaign",
    "delete_campaign",
]

THIRD_PARTY_RESPONDENT_PERMISSIONS_LIST = [
    "view_complianceassessment",
    "view_requirementassessment",
    "change_requirementassessment",
    "view_evidence",
    "add_evidence",
    "change_evidence",
    "delete_evidence",
    "view_folder",
]


def startup(sender: AppConfig, **kwargs):
    """
    Implement CISO Assistant 1.0 default Roles and User Groups during migrate
    This makes sure root folder and global groups are defined before any other object is created
    Create superuser if CISO_ASSISTANT_SUPERUSER_EMAIL defined
    """
    from django.contrib.auth.models import Permission

    from core.models import Qualification, AssetClass
    from iam.models import Folder, Role, RoleAssignment, User, UserGroup
    from tprm.models import Entity
    from privacy.models import ProcessingNature
    from global_settings.models import GlobalSettings

    print("startup handler: initialize database")

    reader_permissions = Permission.objects.filter(codename__in=READER_PERMISSIONS_LIST)

    approver_permissions = Permission.objects.filter(
        codename__in=APPROVER_PERMISSIONS_LIST
    )

    analyst_permissions = Permission.objects.filter(
        codename__in=ANALYST_PERMISSIONS_LIST
    )

    domain_manager_permissions = Permission.objects.filter(
        codename__in=DOMAIN_MANAGER_PERMISSIONS_LIST
    )

    administrator_permissions = Permission.objects.filter(
        codename__in=ADMINISTRATOR_PERMISSIONS_LIST
    )

    # if root folder does not exist, then create it
    if not Folder.objects.filter(content_type=Folder.ContentType.ROOT).exists():
        Folder.objects.create(
            name="Global", content_type=Folder.ContentType.ROOT, builtin=True
        )
    # if main entity does not exist, then create it
    if not Entity.get_main_entity():
        main = Entity.objects.create(
            name="Main", folder=Folder.get_root_folder(), builtin=True
        )
        main.owned_folders.add(Folder.get_root_folder())
    # update builtin roles to facilitate migrations
    reader, created = Role.objects.get_or_create(name="BI-RL-AUD", builtin=True)
    reader.permissions.set(reader_permissions)
    approver, created = Role.objects.get_or_create(name="BI-RL-APP", builtin=True)
    approver.permissions.set(approver_permissions)
    analyst, created = Role.objects.get_or_create(name="BI-RL-ANA", builtin=True)
    analyst.permissions.set(analyst_permissions)
    domain_manager, created = Role.objects.get_or_create(name="BI-RL-DMA", builtin=True)
    domain_manager.permissions.set(domain_manager_permissions)
    administrator, created = Role.objects.get_or_create(name="BI-RL-ADM", builtin=True)
    administrator.permissions.set(administrator_permissions)
    # if global administrators user group does not exist, then create it
    if not UserGroup.objects.filter(
        name="BI-UG-ADM", folder=Folder.get_root_folder()
    ).exists():
        administrators = UserGroup.objects.create(
            name="BI-UG-ADM", folder=Folder.get_root_folder(), builtin=True
        )
        ra1 = RoleAssignment.objects.create(
            user_group=administrators,
            role=Role.objects.get(name="BI-RL-ADM"),
            is_recursive=True,
            builtin=True,
            folder=Folder.get_root_folder(),
        )
        ra1.perimeter_folders.add(administrators.folder)
    # if global readers user group does not exist, then create it
    if not UserGroup.objects.filter(
        name="BI-UG-GAD", folder=Folder.get_root_folder()
    ).exists():
        global_readers = UserGroup.objects.create(
            name="BI-UG-GAD",
            folder=Folder.objects.get(content_type=Folder.ContentType.ROOT),
            builtin=True,
        )
        ra2 = RoleAssignment.objects.create(
            user_group=global_readers,
            role=Role.objects.get(name="BI-RL-AUD"),
            is_recursive=True,
            builtin=True,
            folder=Folder.get_root_folder(),
        )
        ra2.perimeter_folders.add(global_readers.folder)
    if not UserGroup.objects.filter(
        name=UserGroupCodename.ANALYST.value, folder=Folder.get_root_folder()
    ).exists():
        analysts = UserGroup.objects.create(
            name=UserGroupCodename.ANALYST.value,
            folder=Folder.get_root_folder(),
            builtin=True,
        )
        ra2 = RoleAssignment.objects.create(
            user_group=analysts,
            role=Role.objects.get(name=RoleCodename.ANALYST.value),
            is_recursive=True,
            builtin=True,
            folder=Folder.get_root_folder(),
        )
        ra2.perimeter_folders.add(analysts.folder)
    # if global approvers user group does not exist, then create it
    if not UserGroup.objects.filter(
        name="BI-UG-GAP", folder=Folder.get_root_folder()
    ).exists():
        global_approvers = UserGroup.objects.create(
            name="BI-UG-GAP",
            folder=Folder.objects.get(content_type=Folder.ContentType.ROOT),
            builtin=True,
        )
        ra2 = RoleAssignment.objects.create(
            user_group=global_approvers,
            role=Role.objects.get(name="BI-RL-APP"),
            is_recursive=True,
            builtin=True,
            folder=Folder.get_root_folder(),
        )
        ra2.perimeter_folders.add(global_approvers.folder)

    third_party_respondent_permissions = Permission.objects.filter(
        codename__in=THIRD_PARTY_RESPONDENT_PERMISSIONS_LIST
    )
    third_party_respondent, created = Role.objects.get_or_create(
        name=RoleCodename.THIRD_PARTY_RESPONDENT.value, builtin=True
    )
    third_party_respondent.permissions.set(third_party_respondent_permissions)

    # Create default Qualifications
    try:
        Qualification.create_default_qualifications()
    except Exception as e:
        logger.error("Error creating default qualifications", exc_info=e)

    # Create default Processing natures
    try:
        ProcessingNature.create_default_values()
    except Exception as e:
        logger.error("Error creating default ProcessingNature", exc_info=e)

    # Create default AssetClass
    try:
        AssetClass.create_default_values()
    except Exception as e:
        logger.error("Error creating default AssetClass", exc_info=e)

    call_command("storelibraries")

    # if superuser defined and does not exist, then create it
    if (
        CISO_ASSISTANT_SUPERUSER_EMAIL
        and not User.objects.filter(email=CISO_ASSISTANT_SUPERUSER_EMAIL).exists()
    ):
        try:
            User.objects.create_superuser(
                email=CISO_ASSISTANT_SUPERUSER_EMAIL, is_superuser=True
            )
        except Exception as e:
            logger.error("Error creating superuser", exc_info=e)

    # add administrators group to superusers (for resiliency)
    administrators = UserGroup.objects.get(
        name="BI-UG-ADM", folder=Folder.get_root_folder()
    )
    for u in User.objects.filter(is_superuser=True):
        u.user_groups.add(administrators)

    # reset global setings in case of an issue
    default_settings = {
        "security_objective_scale": "1-4",
        "ebios_radar_max": 6,
        "ebios_radar_green_zone_radius": 0.2,
        "ebios_radar_yellow_zone_radius": 0.9,
        "ebios_radar_red_zone_radius": 2.5,
        "notifications_enable_mailing": False,
        "interface_agg_scenario_matrix": False,
    }
    try:
        settings, _ = GlobalSettings.objects.get_or_create(name="general")
        current_value = settings.value or {}

        ebios_radar_max = current_value.get("ebios_radar_max")

        if ebios_radar_max is None or ebios_radar_max == 0:
            # This cannot be None or 0, revert to default values
            logger.warning(
                "ebios radar settings are invalid (None or 0). Reverting to default settings."
            )
            updated_value = {**current_value, **default_settings}
            settings.value = updated_value
            settings.save()
            logger.info(
                "Global settings have been reset to defaults due to invalid ebios_radar_max."
            )
    except Exception as e:
        logger.error(f"Failed to reset global settings: {e}")


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Core"

    def ready(self):
        # avoid post_migrate handler if we are in the main, as it interferes with restore
        if not os.environ.get("RUN_MAIN"):
            post_migrate.connect(startup, sender=self)
