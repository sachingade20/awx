from awx.main.models import Job
import pytest

import json


@pytest.mark.django_db
def test_orphan_unified_job_creation(instance, inventory):
    job = Job.objects.create(job_template=None, inventory=inventory, name='hi world')
    job2 = job.copy_unified_job()
    assert job2.job_template is None
    assert job2.inventory == inventory
    assert job2.name == 'hi world'
    assert job.job_type == job2.job_type
    assert job2.launch_type == 'relaunch'


@pytest.mark.django_db
def test_job_notification_data(inventory):
    encrypted_str = "$encrypted$"
    job = Job.objects.create(
        job_template=None, inventory=inventory, name='hi world',
        extra_vars=json.dumps({"SSN": "123-45-6789"}),
        survey_passwords={"SSN": encrypted_str}
    )
    notification_data = job.notification_data(block=0)
    assert json.loads(notification_data['extra_vars'])['SSN'] == encrypted_str
