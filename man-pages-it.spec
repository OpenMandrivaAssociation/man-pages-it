%define LNG it
%define extra_version 0.5.0
%define fextra %name-extra-%{extra_version}

Summary: Italian manual pages
Name:    man-pages-%LNG
Version: 2.80
Release: %mkrel 4
License: GPL
URL:     ftp://ftp.pluto.it/pub/pluto/ildp/man/
Source:  ftp://ftp.pluto.it/pub/pluto/ildp/man/%name-%version.tar.gz
Source1:  %fextra.tar.bz2
Patch0: man-pages-it-2.80-installdir.patch
Group:   System/Internationalization
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: man => 1.5j-8mdk
Requires: locales-%LNG, man => 1.5j-8mdk
Autoreq: false
BuildArch: noarch
Obsoletes: man-%LNG, manpages-%LNG
Provides:  man-%LNG, manpages-%LNG
Conflicts: linkchecker < 2.3, vim-common < 7.0-2mdk


%description 
Italian translations of Linux manual pages: this package includes not
only those from the LDP, but also translations of other popular
man-pages.

BEWARE: some pages are dated!


%prep
%setup -q -a1
%patch0 -p0

%build

%install
rm -fr %buildroot

make install prefix=%buildroot%_prefix
make install prefix=%buildroot -C %fextra

LANG=%LNG DESTDIR=%{buildroot} %{_sbindir}/makewhatis %{buildroot}/%_mandir/%LNG

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron << EOF
#!/bin/bash
LANG=%LNG %{_sbindir}/makewhatis %_mandir/%LNG
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron

mkdir -p  %{buildroot}/var/cache/man/%LNG

touch %{buildroot}/var/cache/man/%LNG/whatis

# these are provided by vim7:
rm -f %{buildroot}/%_mandir/%LNG/man1/{view.,rview.,vim}*


%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%LNG, if there isn't any man page
   ## directory /%_mandir/%LNG
   if [ ! -d %_mandir/%LNG ] ; then
       /bin/rm -rf /var/catman/%LNG
   fi
fi

%post
%create_ghostfile /var/cache/man/%LNG/whatis root root 644

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,man,755)
%doc CHANGELOG HOWTOHELP readme
%dir %_mandir/%LNG
%dir /var/cache/man/%LNG
%ghost %config(noreplace) /var/cache/man/%LNG/whatis
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron
%_mandir/%LNG/man*
%_mandir/%LNG/whatis
