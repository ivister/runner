#!/usr/bin/python3.6

from subprocess import call, run, PIPE
import argparse
import sys
from time import sleep


def get_args():
    """
    :return:
    """
    parser = argparse.ArgumentParser(description="Builder")
    parser.add_argument('-o', '--outfile', dest='outfile',
                        action='store')
    parser.add_argument('-d', '--dockerfile', dest='dockerfile_path',
                        action='store', required=True)
    parser.add_argument('-t', '--tag', dest='tag',
                        action='store', required=True)
    parser.add_argument('--rm', dest='rm', action='store_true')
    return parser.parse_args()


def main():
    """
    """
    return_code = 0
    args = get_args()
    build_command = ["docker", "build", args.dockerfile_path, "--tag", args.tag]
    build = run(build_command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    print("Build Section: \"%s\"\n" % " ".join(build_command))
    print("\tOUTPUT:\n%s" % build.stdout)
    print("\tERRORS:\n%s" % build.stderr)
    return_code = build.returncode

    if not return_code == 0:
        sys.exit(return_code)

    cont_name = (build.stdout.split()[-1])

    if args.outfile:
        save_command = ["docker", "save", "-o", args.outfile, cont_name]
        save = run(save_command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        print("Save Section: \"%s\"\n" % " ".join(save_command))
        print("\tOUTPUT:\n%s" % save.stdout)
        print("\tERRORS:\n%s" % save.stderr)
        return_code = save.returncode

    if not return_code == 0:
        sys.exit(return_code)

    if args.rm:
        remove_command = ["docker", "rmi", cont_name]
        remove = run(remove_command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        print("Remove Section: \"%s\"\n" % " ".join(remove_command))
        print("\tOUTPUT:\n%s" % remove.stdout)
        print("\tERRORS:\n%s" % remove.stderr)
        return_code = remove.returncode

    sys.exit(return_code)


if __name__ == '__main__':
    main()
