Summary:	IPMI Management Utilities
Summary(pl.UTF-8):	Narzędzia zarządzające IPMI
Name:		ipmiutil
Version:	2.2.0
Release:	1
License:	BSD
Group:		Applications/System
Source0:	http://dl.sourceforge.net/ipmiutil/%{name}-%{version}.tar.gz
# Source0-md5:	382be2356375081e777b3b6e4d51afe0
Patch0:		%{name}-am.patch
Patch1:		%{name}-make-jN.patch
Patch2:		%{name}-am2.patch
URL:		http://ipmiutil.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		mibsdir		/usr/share/snmp/mibs

%description
The ipmiutil component package provides utilities to view the SEL
(showsel), perform a hardware reset (hwreset), and set up the Platform
Event Filter entry to allow BMC LAN alerts from OS Critical Stop
messages (pefconfig). It requires an IPMI driver (ipmidrvr) package in
order to talk to the BMC/firmware interface.

An IPMI driver can be provided by either the Intel IPMI driver
(/dev/imb) or the valinux IPMI driver (/dev/ipmikcs).

%description -l pl.UTF-8
Pakiet ipmiutil dostarcza narzędzia do oglądania SEL (showsel),
wykonywania sprzętowego resetu (hwreset) i ustawiania wpisu Platform
Event Filter, aby włączyć alarmy BMC LAN pochodzące od komunikatów OS
Critical Stop (pefconfig). Wymaga pakietu ze sterownikiem IPMI
(ipmidrvr) do porozumiewania się z interfejsem BMC/firmware.

Sterownik IPMI może być dostarczony przez sterownik Intel IPMI
(/dev/imb), albo przez sterownik valinux IPMI (/dev/ipmikcs).

%package mibs
Summary:	MIB database
Summary(pl.UTF-8):	Baza danych MIB
Group:		Applications/System
Requires:	net-snmp-mibs

%description mibs
This package contains MIB files from Intel:
- Alert on LAN MIB
- MIB file for PET events

%description mibs -l pl.UTF-8
Ten pakiet zawiera pliki MIB od Intela:
- alarmy dla LAN MIB
- plik MIB dla zdarzeń PET

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

rm lib/lib*.a*

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make} -C lib \
	CC="%{__cc}"
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_mandir}/man8,%{mibsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C doc install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_datadir}/ipmiutil/*.mib $RPM_BUILD_ROOT%{mibsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README TODO doc/UserGuide doc/checksel
%attr(755,root,root) %{_sbindir}/alarms
%attr(755,root,root) %{_sbindir}/bmcconfig
%attr(755,root,root) %{_sbindir}/bmchealth
%attr(755,root,root) %{_sbindir}/events
%attr(755,root,root) %{_sbindir}/fruconfig
%attr(755,root,root) %{_sbindir}/getevent
%attr(755,root,root) %{_sbindir}/hwreset
%attr(755,root,root) %{_sbindir}/icmd
%attr(755,root,root) %{_sbindir}/idiscover
%attr(755,root,root) %{_sbindir}/ipmiutil
%attr(755,root,root) %{_sbindir}/isolconsole
%attr(755,root,root) %{_sbindir}/pefconfig
%attr(755,root,root) %{_sbindir}/sensor
%attr(755,root,root) %{_sbindir}/showsel
%attr(755,root,root) %{_sbindir}/tmconfig
%attr(755,root,root) %{_sbindir}/wdt
%{_mandir}/man8/alarms.8*
%{_mandir}/man8/bmcconfig.8*
%{_mandir}/man8/bmchealth.8*
%{_mandir}/man8/events.8*
%{_mandir}/man8/fruconfig.8*
%{_mandir}/man8/getevent.8*
%{_mandir}/man8/hwreset.8*
%{_mandir}/man8/icmd.8*
%{_mandir}/man8/idiscover.8*
%{_mandir}/man8/ipmiutil.8*
%{_mandir}/man8/isolconsole.8*
%{_mandir}/man8/pefconfig.8*
%{_mandir}/man8/sensor.8*
%{_mandir}/man8/showsel.8*
%{_mandir}/man8/tmconfig.8*
%{_mandir}/man8/wdt.8*

%files mibs
%defattr(644,root,root,755)
%{mibsdir}/bmclanaol.mib
%{mibsdir}/bmclanpet.mib
