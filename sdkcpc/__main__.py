
import argparse
from .about import *
from .compile import *
from .run import *
from .validate import *


def main():
    # Program arguments
    parser = argparse.ArgumentParser()
    parser.version = developer_info()

    subparsers = parser.add_subparsers(help='commands', dest='command')

    # AN about command
    subparsers.add_parser('about', help='Shows information about Basic SDK')

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
    validate_parser.add_argument('-v', '--verbose', action='store_false', help='Show all info to validate process')
    # config_parser.print_help()

    # AN info command
    subparsers.add_parser('info', help='Show information of project')

    # A new command
    new_parser = subparsers.add_parser('new', help='Create new basic project')
    new_parser.add_argument('name_project', type=str)

    # A new 8bp command
    new_8bp_parser = subparsers.add_parser('new-8bp', help='Create new basic project 8bp')
    new_8bp_parser.add_argument('name_project_8bp', type=str)

    # A run command
    run_parser = subparsers.add_parser('run', help='Run BAS File in DSK image')
    run_parser.add_argument('-v', '--verbose', action='store_false', help='Show all info in run project')
    run_parser = run_parser.add_mutually_exclusive_group()
    run_parser.add_argument('--rvm', action='store_true', help='Run in Retro Virtual Machine Software')
    run_parser.add_argument('--m4', action='store_true', help='Run in M4-Board')

    # A version command
    parser.add_argument('-v', '--version', action='version')

    # If there are no arguments we exit with error
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)

    args = parser.parse_args()

    if args.command == 'new':
        createNewProject(args.name_project, "BASIC")
    elif args.command == 'new-8bp':
        createNewProject(args.name_project_8bp, "8BP")
    elif args.command == 'run':
        validate_project(args.verbose)
        if args.rvm:
            rvm()
            sys.exit(0)
        if args.m4:
            print("[yellow]This option will be supported for the next version")
            sys.exit(0)
        print("\n[red bold]Missing parameter.\n")
    elif args.command == 'deploy':
        if args.rvm:
            validate_project(args.verbose)
            if build():
                rvm()
                sys.exit(0)
        if args.m4:
            print("[yellow]This option will be supported for the next version")
            sys.exit(0)
        print("\n[red bold]Missing parameter.\n")
    elif args.command == 'info':
        validate_project(True)
        info()
    elif args.command == "validate":
        validate_makefile_project(args.verbose)
    elif args.command == "make":
        validate_project(args.verbose)
        build()
    elif args.command == "about":
        about()


# def main(args):
#     return 0

if __name__ == '__main__':
    main()
