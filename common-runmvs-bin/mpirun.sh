#!/bin/sh

argv=( "$@")
. /common/runmvs/bin/mpirun.args


if ldd $progname | grep -q hpmpi ; then
	 mpirun.hpmpi "${argv[@]}"
elif ldd $progname | grep -q libibverbs ; then
	 mpirun.mvapich "${argv[@]}"
else
	mpirun "${argv[@]}"
fi
