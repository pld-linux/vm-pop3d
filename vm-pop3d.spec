# Conditional build:
%bcond_without	pam		 # build without pam support
%bcond_without	virtual		 # build without virtual users support
%bcond_with	ip_based_virtual # enable IP-based virtual passwd files and spool directories
%bcond_with	debug		 # enable debugging messages and logging
#
Summary:	POP3 daemon
Summary(pl):	Serwer POP3
Name:		vm-pop3d
Version:	1.1.6
Release:	4
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/mail/pop/%{name}-%{version}.tar.gz
# Source0-md5:	0399cc06f5329a6eaebec05d959a6ec1
Source1:	%{name}.inetd
Source2:	%{name}.init
Patch0:		%{name}-ac.patch
URL:		http://www.reedmedia.net/software/virtualmail-pop3d/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_pam:BuildRequires:	pam-devel}
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
virtualmail-pop3d supports alternative password files and mail spool
directories; it can be used for setting up virtual email accounts
-- mailboxes without real Unix owners for each. This will allow you
to have multiple email accounts with the same name on one system.

%description -l pl
virtualmail-pop3d obs³uguje alternatywne pliki z has³ami i katalogi
pocztowe. Mo¿e byæ u¿ywany do ustawiania wirtualnych kont pocztowych -
skrzynek bez prawdziwych uniksowych u¿ytkowników dla ka¿dej z nich.
To pozwala mieæ w jednym systemie wiele kont pocztowych o tej samej
nazwie.

%package common
Summary:	POP3 daemon - common files
Summary(pl):	Serwer POP3 - wspólne pliki
Group:		Networking/Daemons
%{?with_pam:Requires:	pam >= 0.77.3}
Obsoletes:	imap-pop
Obsoletes:	pop3daemon
Obsoletes:	pop3proxy
Obsoletes:	qpopper
Obsoletes:	qpopper6
Obsoletes:	solid-pop3d
Obsoletes:	solid-pop3d-ssl

%description common
virtualmail-pop3d supports alternative password files and mail spool
directories; it can be used for setting up virtual email accounts
-- mailboxes without real Unix owners for each. This will allow you
to have multiple email accounts with the same name on one system.

This is common package for standalone and inetd versions.

%description common -l pl
virtualmail-pop3d obs³uguje alternatywne pliki z has³ami i katalogi
pocztowe. Mo¿e byæ u¿ywany do ustawiania wirtualnych kont pocztowych -
skrzynek bez prawdziwych uniksowych u¿ytkowników dla ka¿dej z nich.
To pozwala mieæ w jednym systemie wiele kont pocztowych o tej samej
nazwie.

To jest wspólny pakiet dla wersji samodzielnej i inetd.

%package standalone
Summary:	POP3 daemon - standalone version
Summary(pl):	Serwer POP3 - wersja samodzielna
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}
Requires:	rc-scripts
Provides:	%{name} = %{version}-%{release}
Obsoletes:	vm-pop3d-inetd

%description standalone
virtualmail-pop3d supports alternative password files and mail spool
directories; it can be used for setting up virtual email accounts
-- mailboxes without real Unix owners for each. This will allow you
to have multiple email accounts with the same name on one system.

This is standalone version of vm-pop3d.

%description standalone -l pl
virtualmail-pop3d obs³uguje alternatywne pliki z has³ami i katalogi
pocztowe. Mo¿e byæ u¿ywany do ustawiania wirtualnych kont pocztowych -
skrzynek bez prawdziwych uniksowych u¿ytkowników dla ka¿dej z nich.
To pozwala mieæ w jednym systemie wiele kont pocztowych o tej samej
nazwie.

To jest samodzielna wersja vm-pop3d.

%package inetd
Summary:	POP3 daemon - inetd version
Summary(pl):	Serwer POP3 - wersja inetd
Group:		Networking/Daemons
Requires:	%{name}-common = %{version}
Requires:	rc-inetd
Provides:	%{name} = %{version}-%{release}
Obsoletes:	vm-pop3d-standalone

%description inetd
virtualmail-pop3d supports alternative password files and mail spool
directories; it can be used for setting up virtual email accounts
-- mailboxes without real Unix owners for each. This will allow you
to have multiple email accounts with the same name on one system.

This is inetd version of vm-pop3d.

%description inetd -l pl
virtualmail-pop3d obs³uguje alternatywne pliki z has³ami i katalogi
pocztowe. Mo¿e byæ u¿ywany do ustawiania wirtualnych kont pocztowych -
skrzynek bez prawdziwych uniksowych u¿ytkowników dla ka¿dej z nich.
To pozwala mieæ w jednym systemie wiele kont pocztowych o tej samej
nazwie.

To jest vm-pop3d w wersji inetd.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	%{!?with_pam:--disable-pam} \
	%{!?with_virtual:--disable-virtual} \
	%{?with_ip_based_virtual:--enable-ip-based-virtual} \
	%{?with_debug:--enable-debug}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig/rc-inetd} \
	%{?with_pam:$RPM_BUILD_ROOT/etc/pam.d}

%{__make} install \
	ROOT=$RPM_BUILD_ROOT

%{?with_pam:cp -f vm-pop3d.pamd $RPM_BUILD_ROOT/etc/pam.d/vm-pop3d}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/vm-pop3d
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/vm-pop3d

%clean
rm -rf $RPM_BUILD_ROOT

%post inetd
%service -q rc-inetd reload

%postun inetd
if [ "$1" = "0" ]; then
	%service -q rc-inetd reload
fi

%post standalone
/sbin/chkconfig --add vm-pop3d
%service vm-pop3d restart "vm-pop3d daemon"

%preun standalone
if [ "$1" = "0" ]; then
	%service vm-pop3d stop
	/sbin/chkconfig --del vm-pop3d
fi

%files common
%defattr(644,root,root,755)
%doc AUTHORS CHANGES FAQ README TODO
%{?with_pam:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/vm-pop3d}
%attr(755,root,root) %{_sbindir}/vm-pop3d
%{_mandir}/man8/*

%files inetd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/vm-pop3d

%files standalone
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/vm-pop3d
