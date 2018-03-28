# AWS Repo for scripts

## Script snappy

Demo project to manage AWS EC2 snapshots

### Configuring

snappy uses the configuration file created by the AWS cli e.g.

$ aws configure

### Running

$ pipenv run python snappy/snappy.py <command> <--project=<your-project-name>

*command* list, stop, start
*project* is optional
