%define LANG it
%define extra_version 0.5.0
%define fextra %name-extra-%{extra_version}

Summary: Italian manual pages
Name:    man-pages-%LANG
Version: 2.80
Release: %mkrel 3
License: GPL
URL:     ftp://ftp.pluto.it/pub/pluto/ildp/man/
Source:  ftp://ftp.pluto.it/pub/pluto/ildp/man/%name-%version.tar.gz
Source1:  %fextra.tar.bz2
Patch0: man-pages-it-2.80-installdir.patch
Group:   System/Internationalization
BuildRoot: %_tmppath/%name-%version-%release-buildroot
BuildRequires: man => 1.5j-8mdk
Requires: locales-%LANG, man => 1.5j-8mdk
Autoreq: false
BuildArch: noarch
Obsoletes: man-%LANG, manpages-%LANG
Provides:  man-%LANG, manpages-%LANG
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

LANG=%LANG DESTDIR=$RPM_BUILD_ROOT /usr/sbin/makewhatis $RPM_BUILD_ROOT/%_mandir/%LANG

mkdir -p $RPM_BUILD_ROOT/etc/cron.weekly
cat > $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron << EOF
#!/bin/bash
LANG=%LANG /usr/sbin/makewhatis %_mandir/%LANG
exit 0
EOF
chmod a+x $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron

mkdir -p  $RPM_BUILD_ROOT/var/cache/man/%LANG

touch $RPM_BUILD_ROOT/var/cache/man/%LNG/whatis

# these are provided by vim7:
rm -f $RPM_BUILD_ROOT/%_mandir/%LANG/man1/{view.,rview.,vim}*


%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%LANG, if there isn't any man page
   ## directory /%_mandir/%LANG
   if [ ! -d %_mandir/%LANG ] ; then
       /bin/rm -rf /var/catman/%LANG
   fi
fi

%post
%create_ghostfile /var/cache/man/%LNG/whatis root root 644

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,man,755)
%doc CHANGELOG HOWTOHELP readme
%dir %_mandir/%LANG
%dir /var/cache/man/%LANG
%ghost %config(noreplace) /var/cache/man/%LNG/whatis
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%LANG.cron
%_mandir/%LANG/man*
