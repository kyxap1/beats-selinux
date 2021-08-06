#!/bin/sh -e

DIRNAME=`dirname $0`
cd $DIRNAME
USAGE="$0 [ --update ]"
if [ `id -u` != 0 ]; then
echo 'You must be root to run this script'
exit 1
fi

if [ $# -eq 1 ]; then
	if [ "$1" = "--update" ] ; then
		time=`ls -l --time-style="+%x %X" packetbeat.te | awk '{ printf "%s %s", $6, $7 }'`
		rules=`ausearch --start $time -m avc --raw -se packetbeat`
		if [ x"$rules" != "x" ] ; then
			echo "Found avc's to update policy with"
			echo -e "$rules" | audit2allow -R
			echo "Do you want these changes added to policy [y/n]?"
			read ANS
			if [ "$ANS" = "y" -o "$ANS" = "Y" ] ; then
				echo "Updating policy"
				echo -e "$rules" | audit2allow -R >> packetbeat.te
				# Fall though and rebuild policy
			else
				exit 0
			fi
		else
			echo "No new avcs found"
			exit 0
		fi
	else
		echo -e $USAGE
		exit 1
	fi
elif [ $# -ge 2 ] ; then
	echo -e $USAGE
	exit 1
fi

echo "Building and Loading Policy"
set -x
make -f /usr/share/selinux/devel/Makefile packetbeat.pp || exit
/usr/sbin/semodule -i packetbeat.pp

# Generate a man page off the installed module
sepolicy manpage -p . -d packetbeat_t
# Fixing the file context on /usr/share/packetbeat/bin/packetbeat
/sbin/restorecon -F -R -v /usr/share/packetbeat/bin/packetbeat
# Fixing the file context on /etc/rc\.d/init\.d/packetbeat
/sbin/restorecon -F -R -v /etc/rc\.d/init\.d/packetbeat
# Fixing the file context on /lib/systemd/system/packetbeat.service
/sbin/restorecon -F -R -v /lib/systemd/system/packetbeat.service
# Fixing the file context on /var/log/packetbeat
/sbin/restorecon -F -R -v /var/log/packetbeat
# Fixing the file context on /var/lib/packetbeat
/sbin/restorecon -F -R -v /var/lib/packetbeat
# Generate a rpm package for the newly generated policy

pwd=$(pwd)
rpmbuild --define "_sourcedir ${pwd}" --define "_specdir ${pwd}" --define "_builddir ${pwd}" --define "_srcrpmdir ${pwd}" --define "_rpmdir ${pwd}" --define "_buildrootdir ${pwd}/.build"  -ba packetbeat_selinux.spec
