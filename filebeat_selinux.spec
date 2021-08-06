# vim: sw=4:ts=4:et


%define relabel_files() \
restorecon -R /usr/share/filebeat/bin/filebeat; \
restorecon -R /etc/rc\.d/init\.d/filebeat; \
restorecon -R /lib/systemd/system/filebeat.service; \
restorecon -R /var/lib/filebeat; \
restorecon -R /var/log/filebeat; \

%define selinux_policyver 3.13.1-266

Name:   filebeat_selinux
Version:	1.0
Release:	1%{?dist}
Summary:	SELinux policy module for filebeat

Group:	System Environment/Base		
License:	GPLv2+	
URL:		https://localhost
Source0:	filebeat.pp
Source1:	filebeat.if
Source2:	filebeat_selinux.8


Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
Requires(post): filebeat
BuildArch: noarch

%description
This package installs and sets up the  SELinux policy security module for filebeat.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/filebeat_selinux.8
install -d %{buildroot}/etc/selinux/targeted/contexts/users/


%post
semodule -n -i %{_datadir}/selinux/packages/filebeat.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files

fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r filebeat
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       %relabel_files

    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/filebeat.pp
%{_datadir}/selinux/devel/include/contrib/filebeat.if
%{_mandir}/man8/filebeat_selinux.8.*


%changelog
* Fri Aug  6 2021 Selinux <selinux@local> 1.0-1
- Initial version

