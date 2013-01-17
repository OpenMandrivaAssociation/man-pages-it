%define LNG it
%define extra_version 0.5.0
%define fextra %name-extra-%{extra_version}

Summary: Italian manual pages
Name:    man-pages-%LNG
Version: 2.80
Release: 7
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

LANG=%LNG DESTDIR=%{buildroot} %{_bindir}/mandb %{buildroot}/%_mandir/%LNG

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron << EOF
#!/bin/bash
LANG=%LNG %{_bindir}/mandb %_mandir/%LNG
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
%{_mandir}/%{LNG}/cat*
%{_mandir}/%{LNG}/CACHEDIR.TAG*
%{_mandir}/%{LNG}/index.db*
#%_mandir/%LNG/whatis


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2.80-5mdv2011.0
+ Revision: 666371
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 2.80-4mdv2011.0
+ Revision: 609323
- rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 2.80-3mdv2011.0
+ Revision: 609305
- fix build
- fix typos
- fix build
- rebuild
- rebuilt for 2010.1

* Tue Oct 14 2008 Funda Wang <fwang@mandriva.org> 2.80-1mdv2009.1
+ Revision: 293462
- New version 2.80
- fix installdir

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 2.65-2mdv2009.0
+ Revision: 223189
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Oct 09 2007 Thierry Vignaud <tv@mandriva.org> 2.65-1mdv2008.1
+ Revision: 96136
- new release

* Wed Sep 05 2007 Thierry Vignaud <tv@mandriva.org> 2.43-1mdv2008.0
+ Revision: 80039
- new release


* Fri Nov 17 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.34-1mdv2007.0
+ Revision: 85366
- Import man-pages-it

* Fri Nov 17 2006 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.34-1mdv2007.1
- new release
- new URL
- kill uneeded prereq
- kill patch0 (no more needed)

* Thu May 11 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.3.4-2mdk
- use %%mkrel
- fix conflict with vim

* Thu Dec 11 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.3.4-1mdk
- new release

