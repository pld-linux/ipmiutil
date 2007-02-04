Summary:	IPMI Management Utilities
Summary(pl):	Narzêdzia zarz±dzaj±ce IPMI
Name:		ipmiutil
Version:	1.8.2
Release:	1
License:	BSD
Group:		Applications/System
Source0:	http://dl.sourceforge.net/ipmiutil/%{name}-%{version}.tar.gz
# Source0-md5:	b630bbc9de3d9938051d8b555acdff45
Patch0:		%{name}-am.patch
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

%description -l pl
Pakiet ipmiutil dostarcza narzêdzia do ogl±dania SEL (showsel),
wykonywania sprzêtowego resetu (hwreset) i ustawiania wpisu Platform
Event Filter, aby w³±czyæ alarmy BMC LAN pochodz±ce od komunikatów OS
Critical Stop (pefconfig). Wymaga pakietu ze sterownikiem IPMI
(ipmidrvr) do porozumiewania siê z interfejsem BMC/firmware.

Sterownik IPMI mo¿e byæ dostarczony przez sterownik Intel IPMI
(/dev/imb), albo przez sterownik valinux IPMI (/dev/ipmikcs).

%package mibs
Summary:	MIB database
Summary(pl):	Baza danych MIB
Group:		Applications/System
Requires:	net-snmp-mibs

%description mibs
This package contains MIB files from Intel:
- Alert on LAN MIB
- MIB file for PET events

%description mibs -l pl
Ten pakiet zawiera pliki MIB od Intela:
- alarmy dla LAN MIB
- plik MIB dla zdarzeñ PET

%prep
%setup -q
%patch0 -p1

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
