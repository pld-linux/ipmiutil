Summary:	IPMI Management Utilities
Name:		ipmiutil
Version:	1.5.8
Release:	0.10
License:	BSD
Group:		Applications/System
Source0:	http://dl.sourceforge.net/ipmiutil/%{name}-%{version}.tar.gz
# Source0-md5:	04754de22f71a6bbd534d5dd6a595034
Patch0:		ipmiutil-am.patch
URL:		http://ipmiutil.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	freeipmi-devel
Requires:	freeipmi-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	mibsdir	/usr/share/snmp/mibs

%description
The ipmiutil component package provides utilities to view the SEL
(showsel), perform a hardware reset (hwreset), and set up the Platform
Event Filter entry to allow BMC LAN alerts from OS Critical Stop
messages (pefconfig). It requires an IPMI driver (ipmidrvr) package in
order to talk to the BMC/firmware interface.

An IPMI driver can be provided by either the Intel IPMI driver
(/dev/imb) or the valinux IPMI driver (/dev/ipmikcs).

%package mibs
Summary:	MIB database
Group:		Applications/System
#License:	AS-IS
Requires:	net-snmp-mibs

%description mibs
This package contains MIB files from Intel:
- Alert on LAN MIB
- MIB file for PET events

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_mandir}/man8,%{mibsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install doc/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
install doc/*.mib $RPM_BUILD_ROOT%{mibsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO ChangeLog doc/UserGuide doc/checksel
%attr(755,root,root) %{_sbindir}/wdt
%attr(755,root,root) %{_sbindir}/icmd
%attr(755,root,root) %{_sbindir}/showsel
%attr(755,root,root) %{_sbindir}/tmconfig
%attr(755,root,root) %{_sbindir}/alarms
%attr(755,root,root) %{_sbindir}/pefconfig
%attr(755,root,root) %{_sbindir}/sensor
%attr(755,root,root) %{_sbindir}/fruconfig
%attr(755,root,root) %{_sbindir}/hwreset
%{_mandir}/man8/*

%files mibs
%defattr(644,root,root,755)
%{mibsdir}/bmclanaol.mib
%{mibsdir}/bmclanpet.mib
