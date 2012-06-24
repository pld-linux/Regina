# TODO:
#  - use bconds
Summary:	Rexx interpreter
Summary(de):	Ein Interpreter f�r REXX
Summary(pl):	Interpreter j�zyka REXX
Name:		Regina
Version:	3.3
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/regina-rexx/%{name}-REXX-%{version}.tar.gz
# Source0-md5:	bdb85f57cbe3e7f9b45aea329cd7752e
Source1:	%{name}.init
Patch0:		%{name}-makefileinfix.patch
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

%description -l de
Regina ist ein Rexx Interpreter der f�r die meisten Unix Platformen
�bersetzt worden ist (Linux, FreeBSD, Solaris, AIX, HP-UX, usw.) und
auser dem auch f�r OS/2, eCS, DOS, Win9x/Me/NT/2k/XP, Amiga, Aros,
QNX4.x, QNX6.x, BeOS, MacOS X, EPOC32, AtheOS, OpenVMS, SkyOS und
OpenEdition. Rexx ist eine Programiersprache die f�r unerfahrene
Programierer entwickelt wurde aber Stark genug f�r erfahrene
Programierer ist. Es ist ebenfalls eine Sprache die sich ideal als
Makrosprache f�r andere Applikationen eignet.

Regina hat zwei Hauptziele:
- es soll 100% kompatibel mit dem ANSI Standard sein
- es soll auf so vielen Platformen wie nur m�glich laufen

%description -l pl
Regina jest interpreterem j�zyka REXX, kt�ry zosta� ju� przeniesiony
na wi�kszo�� Unixowych platform (Linux, FreeBSD, Solaris, AIX, HP-UX,
itp.) a tak�e OS/2, eCS, DOS, Win9x/Me/NT/2k/XP, Amiga, AROS, QNX4.x,
QNX6.x, BeOS, MacOS X, EPOC32, AtheOS, OpenVMS, SkyOS and OpenEdition.
Rexx jest j�zykiem programowania, kt�ry zosta� zaprojektowany, by by�
prostym w u�yciu przez niedo�wiadczonych programist�w oraz
wystarczaj�co u�ytecznym, by by� u�ywanym przez do�wiadczonych.
Idealnie sprawdza si� jako j�zyk pisania makr dla innych aplikacji

Dwa g��wne cele tego interpretera, to
- Stuprocentowa kompatybilno�� ze standardem ANSI
- dost�pno�� na jak najwi�kszej liczbie platform

%package libs
Summary:	Libraries for Regina
Summary(de):	Regina Libraries
Summary(pl):	Biblioteki interpretera Regina
Group:		Libraries

%description libs
Regina libraries.

%description libs -l de
Regina Libraries.

%description libs -l pl
Biblioteki dla interpretera Regina.

%package devel
Summary:	Header files for Regina
Summary(de):	Header Dateien f�r Regina
Summary(pl):	Pliki nag��wkowe interpretera Regina
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for Regina.

%description devel -l de
Header Dateien f�r Regina.

%description devel -l pl
Pliki nag��wkowe interpretera Regina.

%package static
Summary:	Static Regina library
Summary(de):	Statische Regina Libraries
Summary(pl):	Statyczna biblioteka Regina
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Regina library.

%description static -l pl
Statyczna biblioteka Regina.

%prep
%setup -q
%patch0 -p1

# hacks for weak tests for gcc
sed -i -e 's/gcc)/*gcc)/;s/= "gcc"/= "%{__cc}"/' configure
# unnecessary libs
sed -i -e 's/nsl nsl_s socket//' configure
# set soname
sed -i -e 's/\$(ABI) -shared/$(ABI) -Wl,-soname=${SHLPRE}${SHLFILE}${SHLPST}.\\$(ABI) -shared/' configure

%build
cp -f /usr/share/automake/config.* .
%configure2_13
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_mandir}/man1}

%{__make} install \
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
%attr(755,root,root) %{_libdir}/libtest*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libregina.so
%{_includedir}/rexxsaa.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libregina.a
