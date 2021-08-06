# vim: sw=4:ts=4:et


%define relabel_files() \
restorecon -R /usr/share/packetbeat/bin/packetbeat; \
restorecon -R /etc/rc\.d/init\.d/packetbeat; \
restorecon -R /lib/systemd/system/packetbeat.service; \
restorecon -R /var/log/packetbeat; \
restorecon -R /var/lib/packetbeat; \

%define selinux_policyver 3.13.1-266

Name:   packetbeat_selinux
Version:	1.0
Release:	1%{?dist}
Summary:	SELinux policy module for packetbeat

Group:	System Environment/Base
License:	GPLv2+
URL:		https://selinux.org
Source0:	packetbeat.pp
Source1:	packetbeat.if
Source2:	packetbeat_selinux.8


Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
Requires(post): packetbeat
BuildArch: noarch

%description
This package installs and sets up the  SELinux policy security module for packetbeat.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/packetbeat_selinux.8
install -d %{buildroot}/etc/selinux/targeted/contexts/users/


%post
semodule -n -i %{_datadir}/selinux/packages/packetbeat.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files

fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r packetbeat
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       %relabel_files

    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/packetbeat.pp
%{_datadir}/selinux/devel/include/contrib/packetbeat.if
%{_mandir}/man8/packetbeat_selinux.8.*


%changelog
* Thu Aug  5 2021 Selinux <selinux@selinux.org> 1.0-1
- Initial version
