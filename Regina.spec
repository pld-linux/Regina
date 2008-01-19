# TODO:
#  - use bconds (???)
Summary:	Rexx interpreter
Summary(de.UTF-8):	Ein Interpreter für REXX
Summary(pl.UTF-8):	Interpreter języka REXX
Name:		Regina
Version:	3.4
Release:	1
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/regina-rexx/%{name}-REXX-%{version}.tar.gz
# Source0-md5:	3300e28b39134211a45aedb0e760cd44
Source1:	%{name}.init
Patch0:		%{name}-gci_convert.patch
URL:		http://regina-rexx.sourceforge.net
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Provides:	rexx
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Regina is a Rexx interpreter that has been ported to most Unix
platforms (Linux, FreeBSD, Solaris, AIX, HP-UX, etc.) and also to
OS/2, eCS, DOS, Win9x/Me/NT/2k/XP, Amiga, AROS, QNX4.x, QNX6.x BeOS,
MacOS X, EPOC32, AtheOS, OpenVMS, SkyOS and OpenEdition. Rexx is a
programming language that was designed to be easy to use for
inexperienced programmers yet powerful enough for experienced users.
It is also a language ideally suited as a macro language for other
applications.

There are two major goals for Regina:
- become 100% compliant with the ANSI Standard.
- be available on as many platforms as possible

%description -l de.UTF-8
Regina ist ein Rexx Interpreter der für die meisten Unix Platformen
übersetzt worden ist (Linux, FreeBSD, Solaris, AIX, HP-UX, usw.) und
auser dem auch für OS/2, eCS, DOS, Win9x/Me/NT/2k/XP, Amiga, Aros,
QNX4.x, QNX6.x, BeOS, MacOS X, EPOC32, AtheOS, OpenVMS, SkyOS und
OpenEdition. Rexx ist eine Programiersprache die für unerfahrene
Programierer entwickelt wurde aber Stark genug für erfahrene
Programierer ist. Es ist ebenfalls eine Sprache die sich ideal als
Makrosprache für andere Applikationen eignet.

Regina hat zwei Hauptziele:
- es soll 100% kompatibel mit dem ANSI Standard sein
- es soll auf so vielen Platformen wie nur möglich laufen

%description -l pl.UTF-8
Regina jest interpreterem języka REXX, który został już
przeniesiony na większość Unixowych platform (Linux, FreeBSD,
Solaris, AIX, HP-UX, itp.) a także OS/2, eCS, DOS, Win9x/Me/NT/2k/XP,
Amiga, AROS, QNX4.x, QNX6.x, BeOS, MacOS X, EPOC32, AtheOS, OpenVMS,
SkyOS and OpenEdition. Rexx jest językiem programowania, który
został zaprojektowany, by być prostym w użyciu przez
niedoświadczonych programistów oraz wystarczająco użytecznym, by
być używanym przez doświadczonych. Idealnie sprawdza się jako
język pisania makr dla innych aplikacji

Dwa główne cele tego interpretera, to
- Stuprocentowa kompatybilność ze standardem ANSI
- dostępność na jak największej liczbie platform

%package libs
Summary:	Libraries for Regina
Summary(de.UTF-8):	Regina Libraries
Summary(pl.UTF-8):	Biblioteki interpretera Regina
Group:		Libraries

%description libs
Regina libraries.

%description libs -l de.UTF-8
Regina Libraries.

%description libs -l pl.UTF-8
Biblioteki dla interpretera Regina.

%package devel
Summary:	Header files for Regina
Summary(de.UTF-8):	Header Dateien für Regina
Summary(pl.UTF-8):	Pliki nagłówkowe interpretera Regina
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for Regina.

%description devel -l de.UTF-8
Header Dateien für Regina.

%description devel -l pl.UTF-8
Pliki nagłówkowe interpretera Regina.

%package static
Summary:	Static Regina library
Summary(de.UTF-8):	Statische Regina Libraries
Summary(pl.UTF-8):	Statyczna biblioteka Regina
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Regina library.

%description static -l de.UTF-8
Statische Regina Libraries.

%description static -l pl.UTF-8
Statyczna biblioteka Regina.

%prep
%setup -q
%patch0 -p0

# unnecessary libs
sed -i -e 's/nsl nsl_s socket//' configure
# set soname
sed -i -e 's/\$(ABI) -shared/$(ABI) -Wl,-soname=${SHLPRE}${SHLFILE}${SHLPST}.\\$(ABI) -shared/' configure

%build
%configure
%{__make} -j 1 \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_mandir}/man1}

%{__make} install -j 1 \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rxstack
install regina.1 $RPM_BUILD_ROOT%{_mandir}/man1
rm -f $RPM_BUILD_ROOT%{_prefix}/etc/rc.d/init.d/rxstack
rm -f $RPM_BUILD_ROOT%{_prefix}/man1/regina.1

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add rxstack
%service rxstack restart

%preun
if [ "$1" = "0" ] ; then
	%service rxstack stop
	/sbin/chkconfig --del rxstack
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING-LIB README* demo
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/rxstack
%dir %{_datadir}/regina
%attr(755,root,root) %{_datadir}/regina/*.rexx
%{_datadir}/regina/*.mtb
%{_mandir}/man1/regina.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libregina.so.*.*
%attr(755,root,root) %{_libdir}/librxtest*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libregina.so
%{_includedir}/rexxsaa.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libregina.a
