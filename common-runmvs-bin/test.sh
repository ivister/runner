#!/usr/bin/env bash
fil='aaa'
# ARGS
        docker_image=''
        docker_command=''
# HELP
#mpirun [mpirun_options...] <progname> [options...]
#  mpirun_options:
#    -dockerimage <file>
#            File with packed docker image (from docker save command)
#    -dockercommand <command>
#            Command that will execute then task will start
while [ 1 -le $# ] ; do
  arg=$1
  #echo $arg
  #echo $#
  shift
  case $arg in
    -dockerimage | -di  )
        docker_image=$1
        if ! [ -x $1 ] ; then
            echo -dockerimage: '"'$docker_image'"' is an invalid argument.  Exiting.
           exit 1
        fi
        shift
        ;;
    -dockercommand | -dc  )
        docker_command=$1
        if [ -z $1 ] ; then
            echo -dockercommand: '"'$docker_image'"' is an invalid argument.  Exiting.
           exit 1
        fi
        shift
        ;;
  esac
done


# MPIRUN
if ! [ -z "$docker_image" ] && ! [ -z "$docker_command" ] ; then
cat <<EOF >> $fil

[Docker]
docker_image_file=`RelToAbs $docker_image`
docker_command="$docker_command"

EOF
fi