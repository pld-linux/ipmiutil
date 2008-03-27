Summary:	IPMI Management Utilities
Summary(pl.UTF-8):	Narzędzia zarządzające IPMI
Name:		ipmiutil
Version:	2.0.9
Release:	0.1
License:	BSD
Group:		Applications/System
Source0:	http://dl.sourceforge.net/ipmiutil/%{name}-%{version}.tar.gz
# Source0-md5:	2a29d97e9e2c2349d51e85cc390cbdce
Patch0:		%{name}-am.patch
Patch1:		%{name}-make-jN.patch
URL:		http://ipmiutil.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
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

rm -f lib/lib*.a*

%build
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

install doc/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
install doc/*.mib $RPM_BUILD_ROOT%{mibsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README TODO doc/UserGuide doc/checksel
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*

%files mibs
%defattr(644,root,root,755)
%{mibsdir}/bmclanaol.mib
%{mibsdir}/bmclanpet.mib
