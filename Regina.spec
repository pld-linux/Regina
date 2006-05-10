# TODO:
#  - fix the method rxstarck is installed
#  - use bconds
#  - create subpackages

Summary:	Rexx interpreter
Summary(pl):	Interpreter jêzyka REXX
Name:		Regina
Version:	3.3
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/regina-rexx/%{name}-REXX-%{version}.tar.gz
# Source0-md5:	bdb85f57cbe3e7f9b45aea329cd7752e
Patch0:		%{name}-makefileinfix.patch
URL:		http://regina-rexx.sourceforge.net
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	mawk
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Provides:	libregina.so
Provides:	libregina.so(REXXSAA_API)
Provides:	libregina.so(regina_2.0)
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

%description -l pl
Regina jest interpreterem jêzyka REXX, który zosta³ ju¿ przeniesiony
na wiêkszo¶æ Unixowych platform (Linux, FreeBSD, Solaris, AIX, HP-UX,
itp.) a tak¿e OS/2, eCS, DOS, Win9x/Me/NT/2k/XP, Amiga, AROS, QNX4.x,
QNX6.x, BeOS, MacOS X, EPOC32, AtheOS, OpenVMS, SkyOS and OpenEdition.
Rexx jest jêzykiem programowania, który zosta³ zaprojektowany, by byæ
prostym w u¿yciu przez niedo¶wiadczonych programistów oraz
wystarczaj±co u¿ytecznym, by byæ u¿ywanym przez do¶wiadczonych.
Idealnie sprawdza siê jako jêzyk pisania makr dla innych aplikacji

Dwa g³ówne cele tego internretera, to
 - Stuprocentowa kompatybilno¶æ ze standardemi ANSI
 - dostêpno¶æ na jak najwiêkszej liczbie platform

%prep
%setup -q
%patch -p1

%build
./configure
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d/,%{_mandir}/man1}
%{__make} install \
    DESTDIR=$RPM_BUILD_ROOT
install $RPM_BUILD_ROOT%{_prefix}/etc/rc.d/init.d/rxstack $RPM_BUILD_ROOT/etc/rc.d/init.d/
install $RPM_BUILD_ROOT%{_prefix}/man/man1/regina.1 $RPM_BUILD_ROOT%{_mandir}/man1/
rm -f $RPM_BUILD_ROOT%{_prefix}/etc/rc.d/init.d/rxstack
rm -f $RPM_BUILD_ROOT%{_prefix}/man/man1/regina.1

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
/sbin/chkconfig --add rxstack
%service rxstack restart

%preun
if [ "$1" = "0" ]; then
        %service rxstack stop
        /sbin/chkconfig --del rxstack
fi

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING-LIB README* demo
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/rxstack
%attr(644,root,root) %{_includedir}/rexxsaa.h
%attr(755,root,root) %{_prefix}/lib/*
%attr(755,root,root) %{_datadir}/regina/*.rexx
%{_datadir}/regina/*.mtb
%{_mandir}/man1/regina.1*
