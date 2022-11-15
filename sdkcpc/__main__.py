
import argparse
import click
from sdkcpc.information import info
from . import __version__
from .about import *
from .make import *
from .run import *
from .validations import *


@click.command()
@click.argument('issue')
@click.argument('section',
                type=click.Choice(['data', 'jira', 'bitbucket', 'meta', 'jenkins', 'teams'], case_sensitive=False))
@click.argument('operation', type=click.Choice(['create', 'update', 'finish', 'reject'], case_sensitive=False))
@click.option('--source-file', default="/tmp/application.yaml", required=False)
@click.option('--comment', '-c')
@click.option('--silent', '-s', is_flag=True)
def onboard(issue, section, operation, source_file, comment, silent):
    try:

        if not section == 'data':
            with open(source_file) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)

        if section == 'data':
            if operation == "create":
                app.onboard(issue, source_file)

            else:
                raise Exception(f"Operation {operation} not supported for {section} section.")

        elif section == 'jira':
            if operation == "create":
                app.create_jira_project(issue, data)
            elif operation == "finish":
                app.finish_onboard(issue, comment)
            elif operation == "reject":
                app.reject_onboard(issue, comment)
            else:
                raise Exception(f"Operation {operation} not supported for {section} section.")

        elif section == 'bitbucket':
            if operation == "create":
                app.create_bitbucket_project(issue, data)

            else:
                raise Exception(f"Operation {operation} not supported for {section} section.")

        elif section == 'meta':
            if operation == "create":
                app.create_meta_repository(issue, data)
                app.create_infra_meta_repository(issue, data)

            else:
                raise Exception(f"Operation {operation} not supported for {section} section.")


        elif section == 'jenkins':
            if operation == "create":
                app.create_jenkins_folder(issue, data)

            else:
                raise Exception(f"Operation {operation} not supported for {section} section.")

        elif section == 'teams':
            if operation == "create":
                app.create_team(issue, data)

            else:
                raise Exception(f"Operation {operation} not supported for {section} section.")


    except Exception as e:
        if not silent: app.reject_onboard(issue, str(e))
        raise e


def main():
    # Program arguments
    parser = argparse.ArgumentParser()
    parser.version = str(__version__)

    subparsers = parser.add_subparsers(help='commands', dest='command')

    # A new command
    project_parser = subparsers.add_parser('project', help='Create new basic project')
    deploy_parser = project_parser.add_mutually_exclusive_group()
    deploy_parser.add_argument('-m', '--make', action='store_false', help='make the DSK image of the project')
    deploy_parser.add_argument('-d', '--deploy', action='store_false', help='Make and Run the dsk image on the '                                                  'emulator or M4-Board')
    deploy_parser.add_argument('-v', '--validate', action='store_false', help='Validate project data')
    deploy_parser.add_argument('-i', '--info', action='store_false', help='Show information of project')
    # new_parser.add_argument('name_project', type=str)

    # A build command
    build_parser = subparsers.add_parser('make', help='make the DSK image of the project')
    build_parser.add_argument('-v', '--verbose', action='store_false', help='Show all info in compilation project')

    # A deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Make and Run the dsk image on the emulator or M4-Board')
    deploy_parser.add_argument('-v', '--verbose', action='store_false', help='Show all info in Make/Run project')
    deploy_parser = deploy_parser.add_mutually_exclusive_group()
    deploy_parser.add_argument('--rvm', action='store_true', help='Run in Retro Virtual Machine Software')
    deploy_parser.add_argument('--m4', action='store_true', help='Run in M4-Board')

    # A check command
    validate_parser = subparsers.add_parser('validate', help='Project data validation.')
    # validate_parser.add_argument('-v', '--verbose', action='store_false', help='Show all info to validate process')
    # config_parser.print_help()

    # AN info command
    subparsers.add_parser('info', help='Show information of project')

    # A new 8bp command
    # new_8bp_parser = subparsers.add_parser('new-8bp', help='Create new basic project 8bp')
    # new_8bp_parser.add_argument('name_project_8bp', type=str)

    # A run command
    run_parser = subparsers.add_parser('run', help='Run BAS File in DSK image')
    run_parser.add_argument('-v', '--verbose', action='store_false', help='Show all info in run project')
    run_parser = run_parser.add_mutually_exclusive_group()
    run_parser.add_argument('--rvm', action='store_true', help='Run in Retro Virtual Machine Software')
    run_parser.add_argument('--m4', action='store_true', help='Run in M4-Board')

    # A version command
    parser.add_argument('-v', '--version', action='version')
    parser.add_argument('-a', '--about', action='store_true', help='Shows information about Basic SDK')


    # If there are no arguments we exit with error
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)

    args = parser.parse_args()
    if args.about:
        about()

    if args.command == 'project':
        head()
        createNewProject()
    elif args.command == 'run':
        if args.rvm:
            rvm()
            sys.exit(0)
        if args.m4:
            print("[yellow]This option will be supported for the next version")
            sys.exit(0)
        print("\n[red bold]Missing parameter.\n")
    elif args.command == 'deploy':
        if args.rvm:
            if build():
                rvm()
                sys.exit(0)
        if args.m4:
            print("[yellow]This option will be supported for the next version")
            sys.exit(0)
        print("\n[red bold]Missing parameter.\n")
    elif args.command == 'info':
        info()
    elif args.command == "validate":
        validateAll()
    elif args.command == "make":
        build()


# def main(args):
#     return 0

if __name__ == '__main__':
    main()
