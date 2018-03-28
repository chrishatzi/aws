import boto3
import click

session = boto3.Session(profile_name='default')
ec2 = session.resource('ec2')

'''
@click.group()
@click.option('--debug', default=False, help='turn debug on')
def cli(debug):
    pass

@cli.command()
def list_volumes():
    "List Volumes"
'''

'''
Helper function that returns a list of instances based on an optional filter
'''
def get_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters = filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def instances():
    'Commands for instances'

'''
This command stops EC2 instances optionally filtering them by the
a tag named 'Project'
'''
@instances.command('start')
@click.option('--project', default=None,
    help='Only instances for project (tag Project:<name>)')
def start_instances(project):
    'Start EC2 instances'

    instances = get_instances(project)

    for i in instances:
        print('Starting {0}...'.format(i.id))
        i.start()

    return

'''
This command stops EC2 instances optionally filtering them by the
a tag named 'Project'
'''
@instances.command('stop')
@click.option('--project', default=None,
    help='Only instances for project (tag Project:<name>)')
def stop_instances(project):
    'Stop EC2 instances'

    instances = get_instances(project)

    for i in instances:
        print('Stopping {0}...'.format(i.id))
        i.stop()

    return

'''
This command lists out the EC2 instances optionally filtering them by the
a tag named 'Project'
'''
@instances.command('list')
@click.option('--project', default=None,
    help='Only instances for project (tag Project:<name>)')
def list_instances(project):
    'List EC2 instances'

    instances = get_instances(project)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or [] }

        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>'))))

    return

if __name__ == '__main__':
    instances()
