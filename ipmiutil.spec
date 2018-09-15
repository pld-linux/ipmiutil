# TODO: finish systemd support
#
# Conditonal build:
%bcond_without	gpl	# build with GPL code (md2.h, ipmi_ioctls.h)
#
Summary:	IPMI Management Utilities
Summary(pl.UTF-8):	Narzędzia zarządzające IPMI
Name:		ipmiutil
Version:	3.1.2
Release:	2
%if %{with gpl}
License:	GPL v2+
%else
License:	BSD
%endif
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/ipmiutil/%{name}-%{version}.tar.gz
# Source0-md5:	ee90387f8a14dea3f867167865c7c968

Patch1:		%{name}-idiscover-ifaces_with_dot_in_name_support.patch
Patch2:		%{name}-libcrypto.patch
Patch3:		%{name}-symlink.patch
URL:		http://ipmiutil.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	openssl-devel
Suggests:	mibs-%{name}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		mibsdir		/usr/share/mibs

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

%package libs
Summary:	ipmiutil library
Summary(pl.UTF-8):	Biblioteka ipmiutil
Group:		Libraries

%description libs
This package contains libipmiutil library.

%description libs -l pl.UTF-8
Ten pakiet zawiera bibliotekę libipmiutil.

%package devel
Summary:	Header files and examples for ipmiutil library
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja do biblioteki ipmiutil
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains header files and examples for developing
own programs which use libipmiutil.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe i przykłady umożliwiające
tworzenie własnych programów wykorzystujących bibliotekę
ipmiutil.

%package static
Summary:	Static ipmiutil library
Summary(pl.UTF-8):	Statyczna biblioteka ipmiutil
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static libipmiutil library.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczną bibliotekę libipmiutil.

%package -n mibs-%{name}
Summary:	MIB database from IPMI Management Utilities
Summary(pl.UTF-8):	Baza danych MIB z narzędzi zarządzających IPMI
Group:		Applications/System
Requires:	mibs-dirs
Requires:	mibs-net-snmp
Obsoletes:	ipmiutil-mibs

%description -n mibs-%{name}
This package contains MIB file from Intel:
- MIB file for PET events

%description -n mibs-%{name} -l pl.UTF-8
Ten pakiet zawiera plik MIB od Intela:
- plik MIB dla zdarzeń PET

%prep
%setup -q

%patch1 -p1
%patch2 -p1
%patch3 -p1

%{__rm} lib/lib*.a*

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_gpl:--enable-gpl} \
	--enable-shared \
	--enable-static

%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{mibsdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	sysvinit=$RPM_BUILD_ROOT/etc/rc.d/init.d \
	sysdto=$RPM_BUILD_ROOT%{systemdunitdir}

%{__mv} $RPM_BUILD_ROOT%{_datadir}/ipmiutil/*.mib $RPM_BUILD_ROOT%{mibsdir}

install -d $RPM_BUILD_ROOT%{_includedir}
install util/ipmicmd.h $RPM_BUILD_ROOT%{_includedir}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install util/{ipmi_sample.c,ipmi_sample_evt.c,isensor.c,ievents.c,isensor.h,ievents.h,Makefile} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README TODO doc/UserGuide scripts/{checksel,*.sh}
%attr(755,root,root) %{_bindir}/idiscover
%attr(755,root,root) %{_bindir}/ievents
%attr(755,root,root) %{_bindir}/ipmiutil
%attr(755,root,root) %{_sbindir}/ialarms
%attr(755,root,root) %{_sbindir}/icmd
%attr(755,root,root) %{_sbindir}/iconfig
%attr(755,root,root) %{_sbindir}/ifirewall
%attr(755,root,root) %{_sbindir}/ifru
%attr(755,root,root) %{_sbindir}/ifwum
%attr(755,root,root) %{_sbindir}/igetevent
%attr(755,root,root) %{_sbindir}/ihealth
%attr(755,root,root) %{_sbindir}/ihpm
%attr(755,root,root) %{_sbindir}/ilan
%attr(755,root,root) %{_sbindir}/ipicmg
%attr(755,root,root) %{_sbindir}/ipmi_port
%attr(755,root,root) %{_sbindir}/ireset
%attr(755,root,root) %{_sbindir}/isel
%attr(755,root,root) %{_sbindir}/iseltime
%attr(755,root,root) %{_sbindir}/isensor
%attr(755,root,root) %{_sbindir}/iserial
%attr(755,root,root) %{_sbindir}/isol
%attr(755,root,root) %{_sbindir}/iuser
%attr(755,root,root) %{_sbindir}/iwdt
%attr(754,root,root) /etc/rc.d/init.d/ipmi_info
%attr(754,root,root) /etc/rc.d/init.d/ipmi_port
%attr(754,root,root) /etc/rc.d/init.d/ipmiutil_asy
%attr(754,root,root) /etc/rc.d/init.d/ipmiutil_evt
%attr(754,root,root) /etc/rc.d/init.d/ipmiutil_wdt
%{systemdunitdir}/ipmi_port.service
%{systemdunitdir}/ipmiutil_asy.service
%{systemdunitdir}/ipmiutil_evt.service
%{systemdunitdir}/ipmiutil_wdt.service
%{_datadir}/%{name}
%{_mandir}/man8/ialarms.8*
%{_mandir}/man8/icmd.8*
%{_mandir}/man8/iconfig.8*
%{_mandir}/man8/idcmi.8*
%{_mandir}/man8/idelloem.8*
%{_mandir}/man8/idiscover.8*
%{_mandir}/man8/iekanalyzer.8*
%{_mandir}/man8/ievents.8*
%{_mandir}/man8/ifirewall.8*
%{_mandir}/man8/ifru.8*
%{_mandir}/man8/ifwum.8*
%{_mandir}/man8/igetevent.8*
%{_mandir}/man8/ihealth.8*
%{_mandir}/man8/ihpm.8*
%{_mandir}/man8/ilan.8*
%{_mandir}/man8/ipicmg.8*
%{_mandir}/man8/ipmi_port.8*
%{_mandir}/man8/ipmiutil.8*
%{_mandir}/man8/ireset.8*
%{_mandir}/man8/isel.8*
%{_mandir}/man8/iseltime.8*
%{_mandir}/man8/isensor.8*
%{_mandir}/man8/iserial.8*
%{_mandir}/man8/ismcoem.8*
%{_mandir}/man8/isol.8*
%{_mandir}/man8/isunoem.8*
%{_mandir}/man8/itsol.8*
%{_mandir}/man8/iuser.8*
%{_mandir}/man8/iwdt.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libipmiutil.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libipmiutil.so
%{_includedir}/ipmicmd.h
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libipmiutil.a

%files -n mibs-%{name}
%defattr(644,root,root,755)
%{mibsdir}/bmclanpet.mib
