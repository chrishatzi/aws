import boto3
import click

session = boto3.Session(profile_name='default')
ec2 = session.resource('ec2')

@click.group()
def cli():
    pass

@cli.group('snapshots')
def snapshots():
    '''Commands for snapshots'''

'''
This command lists out snapshots for the EC2 volumes optionally filtering
them by the a tag named 'Project'
'''
@snapshots.command('list')
@click.option('--project', default=None,
    help='Only snapshots for project (tag Project:<name>)')
def list_volumes(project):
    '''List EC2 snapshots'''

    instances = get_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(', '.join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime('%c'))))

    return

@cli.group('volumes')
def volumes():
    '''Commands for volumes'''

'''
This command lists out the EC2 instances optionally filtering them by the
a tag named 'Project'
'''
@volumes.command('list')
@click.option('--project', default=None,
    help='Only volumes for project (tag Project:<name>)')
def list_volumes(project):
    '''List EC2 volumes'''

    instances = get_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(', '.join((
                v.id,
                i.id,
                v.state,
                str(v.size) + 'GiB',
                v.encrypted and "Encrypted" or "Not Encrypted")))

    return

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

@cli.group()
def instances():
    '''Commands for instances'''

'''
This command stops EC2 instances optionally filtering them by the
a tag named 'Project'
'''
@instances.command('start')
@click.option('--project', default=None,
    help='Only instances for project (tag Project:<name>)')
def start_instances(project):
    '''Start EC2 instances'''

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
    '''Stop EC2 instances'''

    instances = get_instances(project)

    for i in instances:
        print('Stopping {0}...'.format(i.id))
        i.stop()

    return

'''
This command creates a snapshot of an EC2 volume optionally filtering them
by the a tag named 'Project'
'''
@instances.command('snapshot')
@click.option('--project', default=None,
    help='Only instances for project (tag Project:<name>)')
def create_snapshots(project):
    '''Create snapshots for EC2 instances'''

    instances = get_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print('Creating snapshot of {0}'.format(v.id))

    return

if __name__ == '__main__':
    cli()
