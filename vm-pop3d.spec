Summary:	POP3 daemon
Summary(pl):	Serwer POP3
Name:		vm-pop3d
Version:	1.1.5
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/mail/pop/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Source2:	%{name}.init
URL:		http://www.reedmedia.net/software/virtual-pop3d
%{?!_without_pam:BuildRequires:	pam-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
virtualmail-pop3d supports alternative password files and mail spool
directories; it can be used for setting up virtual email accounts
-- mailboxes without real Unix owners for each. This will allow you 
to have multiple email accounts with the same name on one system.


%package common
Summary:	POP3 daemon
Summary(pl):	Serwer POP3
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
%{?!_without_pam:Requires:	pam >= 0.67}

%description common
virtualmail-pop3d supports alternative password files and mail spool
directories; it can be used for setting up virtual email accounts
-- mailboxes without real Unix owners for each. This will allow you 
to have multiple email accounts with the same name on one system.


%package standalone
Summary:	POP3 daemon
Summary(pl):	Serwer POP3
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
PreReq:		%{name}-common = %{version}
PreReq:		rc-scripts
PreReq:		/sbin/chkconfig
Provides:	%{name} = %{version}-%{release}

%description standalone
virtualmail-pop3d supports alternative password files and mail spool
directories; it can be used for setting up virtual email accounts
-- mailboxes without real Unix owners for each. This will allow you 
to have multiple email accounts with the same name on one system.


%package inetd
Summary:	POP3 daemon
Summary(pl):	Serwer POP3
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
PreReq:		%{name}-common = %{version}
PreReq:		rc-inetd
Provides:	%{name} = %{version}-%{release}

%description inetd
virtualmail-pop3d supports alternative password files and mail spool
directories; it can be used for setting up virtual email accounts
-- mailboxes without real Unix owners for each. This will allow you 
to have multiple email accounts with the same name on one system.


%prep
%setup -q

%build
%configure2_13 \
	%{?_without_pam:--disable-pam} \
	%{?_without_virtual:--disable-virtual} \
	%{?_with_ip_based_virtual:--enable-ip-based-virtual}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} ROOT=$RPM_BUILD_ROOT install

install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
%{?!_without_pam:install -d $RPM_BUILD_ROOT%{_sysconfdir}/pam.d}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd

%{?!_without_pam:cp -f vm-pop3d.pamd $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/vm-pop3d}
cp -f %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd/vm-pop3d
cp -f %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/vm-pop3d

gzip -9nf AUTHORS CHANGES COPYING FAQ README TODO

%clean
rm -rf $RPM_BUILD_ROOT

%post inetd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun inetd
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
fi

%post standalone
/sbin/chkconfig --add vm-pop3d
if [ -f /var/lock/subsys/vm-pop3d ]; then
	/etc/rc.d/init.d/vm-pop3d restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/vm-pop3d start\" to start vm-pop3d daemon."
fi

%preun standalone
if [ "$1" = "0" -a -f /var/lock/subsys/vm-pop3d ]; then
	/etc/rc.d/init.d/vm-pop3d stop 1>&2
fi
/sbin/chkconfig --del vm-pop3d


%files common
%defattr(644,root,root,755)
%doc *.gz
%{?!_without_pam:%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/vm-pop3d}
%attr(0755,root,root) %{_sbindir}/vm-pop3d
%{_mandir}/man8/*

%files inetd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/vm-pop3d

%files standalone
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/vm-pop3d
