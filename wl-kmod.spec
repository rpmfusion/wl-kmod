# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%global buildforkernels newest

Name:       wl-kmod
Version:    6.30.223.248
Release:    3%{?dist}.2
Summary:    Kernel module for Broadcom wireless devices
Group:      System Environment/Kernel
License:    Redistributable, no modification permitted
URL:        http://www.broadcom.com/support/802.11/linux_sta.php
Source0:    http://www.broadcom.com/docs/linux_sta/hybrid-v35-nodebug-pcoem-6_30_223_248.tar.gz
Source1:    http://www.broadcom.com/docs/linux_sta/hybrid-v35_64-nodebug-pcoem-6_30_223_248.tar.gz
Source11:   wl-kmod-kmodtool-excludekernel-filterfile
Patch0:     wl-kmod-001_license.patch
Patch1:     wl-kmod-002_wext_workaround.patch
Patch2:     wl-kmod-003_kernel_3.8.patch
Patch3:     wl-kmod-004_kernel_3.15.patch
Patch4:     wl-kmod-005_kernel_3.16.patch
Patch5:     wl-kmod-006_kernel_3.17.patch

BuildRequires:  %{_bindir}/kmodtool

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i686 x86_64
# ppc disabled because broadcom only provides x86 and x86_64 bits

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
These packages contain Broadcom's IEEE 802.11a/b/g/n hybrid Linux device 
driver for use with Broadcom's BCM4311-, BCM4312-, BCM4313-, BCM4321-, 
BCM4322-, BCM43142-, BCM43224-, BCM43225-, BCM43227-, BCM43228-, 
BCM4331-, BCM4360 and -BCM4352- based hardware.

NOTE: You must read the LICENSE.txt file in the docs directory before using
this software. You should read the fedora.readme file in the docs directory 
in order to know how to  configure this software if you encounter problems 
while boot sequence or with the CFG80211 API (revert to the WEXT API).

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T
mkdir %{name}-%{version}-src
pushd %{name}-%{version}-src
%ifarch %{ix86}
 tar xzf %{SOURCE0}
%else
 tar xzf %{SOURCE1}
%endif
%patch0  -p1 -b .license
%patch1  -p1 -b .wext_workaround.patch
%patch2  -p1 -b .kernel-3.8
%patch3  -p1 -b .kernel-3.15
%patch4  -p1 -b .kernel-3.16
%patch5  -p1 -b .kernel-3.17
popd

for kernel_version in %{?kernel_versions} ; do
 cp -a %{name}-%{version}-src _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}
 make -C ${kernel_version##*___} M=`pwd` modules
 popd
done

%install
rm -rf ${RPM_BUILD_ROOT}
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 install -m 0755 *.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 popd
done

chmod 0755 $RPM_BUILD_ROOT%{kmodinstdir_prefix}*%{kmodinstdir_postfix}/* || :
%{?akmod_install}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Oct 10 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-3.2
- Rebuilt for kernel

* Tue Oct 07 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-3.1
- Rebuilt for kernel

* Fri Oct 03 2014 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.248-3
- Added patch to build for kernel >= 3.17

* Fri Sep 19 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-2.2
- Rebuilt for kernel

* Thu Sep 18 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-2.1
- Rebuilt for kernel

* Wed Sep 10 2014 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.248-2
- Added patch to build for kernel >= 3.16

* Tue Sep 09 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-1.9
- Rebuilt for kernel

* Sat Aug 30 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-1.8
- Rebuilt for kernel

* Wed Aug 20 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-1.7
- Rebuilt for kernel

* Wed Aug 20 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-1.6
- Rebuilt for kernel

* Fri Aug 15 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-1.5
- Rebuilt for kernel

* Wed Aug 13 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-1.4
- Rebuilt for kernel

* Sat Aug 02 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-1.3
- Rebuilt for kernel

* Fri Aug 01 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-1.2
- Rebuilt for kernel

* Fri Jul 18 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-1.1
- Rebuilt for kernel

* Thu Jul 17 2014 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.248-1
- Upstream update to 6.30.223.248
- Patches cleaned-up and removed

* Thu Jul 17 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-6.2
- Rebuilt for kernel

* Fri Jul 11 2014 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.141-6.1
- Rebuild for akmod

* Tue Jul 08 2014 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.141-6
- Added late patch for __devinit since kernel 3.8
- Modified patch to build for kernel >= 3.15

* Tue Jul 08 2014 Leigh Scott <leigh123linux@googlemail.com> - 6.30.223.141-6
- Patch for 3.15 kernel

* Tue Jul 08 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.29
- Rebuilt for kernel

* Tue Jul 08 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.28
- Rebuilt for kernel

* Tue Jul 08 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.27
- Rebuilt for kernel

* Tue Jun 17 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.26
- Rebuilt for kernel

* Fri Jun 13 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.25
- Rebuilt for kernel

* Sun Jun 08 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.24
- Rebuilt for kernel

* Tue Jun 03 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.23
- Rebuilt for kernel

* Thu May 15 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.22
- Rebuilt for kernel

* Thu May 08 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.21
- Rebuilt for kernel

* Wed Apr 30 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.20
- Rebuilt for kernel

* Sat Apr 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.19
- Rebuilt for kernel

* Wed Apr 16 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.18
- Rebuilt for kernel

* Fri Apr 04 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.17
- Rebuilt for kernel

* Wed Apr 02 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.16
- Rebuilt for kernel

* Tue Mar 25 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.15
- Rebuilt for kernel

* Sun Mar 09 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.14
- Rebuilt for kernel

* Tue Mar 04 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.13
- Rebuilt for kernel

* Tue Feb 25 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.12
- Rebuilt for kernel

* Mon Feb 24 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.11
- Rebuilt for kernel

* Mon Feb 17 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.10
- Rebuilt for kernel

* Sat Feb 15 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.9
- Rebuilt for kernel

* Wed Feb 12 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.8
- Rebuilt for kernel

* Fri Feb 07 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.7
- Rebuilt for kernel

* Thu Jan 30 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.6
- Rebuilt for kernel

* Tue Jan 28 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.5
- Rebuilt for kernel

* Fri Jan 17 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.4
- Rebuilt for kernel

* Sun Jan 12 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.3
- Rebuilt for kernel

* Wed Dec 25 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.2
- Rebuilt for kernel

* Fri Dec 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5.1
- Rebuilt for kernel

* Tue Dec 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5
- Rebuilt for f20 final kernel

* Sat Dec 07 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-4
- Rebuilt for f20 final kernel

* Sun Dec 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-3
- Rebuilt for f20 final kernel

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-2
- Rebuilt

* Sat Sep 14 2013 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.141-1
- Upstream update to 6.30.223.141

* Wed Jul 03 2013 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-11
- Modified patch to build for kernel >= 3.10

* Fri Mar 08 2013 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-10
- Modified patch to build for kernel >= 3.8 rfbz#2715
- Modified patch to build for kernel >= 3.9

* Mon Mar 04 2013 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-9
- Added patch to build for kernel >= 3.9

* Fri Mar 01 2013 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-8
- Added patch to build for kernel >= 3.8

* Wed Nov 21 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-7
- Added patch to choose API at build time (WEXT or CFG80211) to workaround #2548 #2562
- Others patches cleaned-up

* Sat Oct 20 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-6
- Added patch to include semaphore.h in wl_iw.h
- Added patch from Archlinux to disable too many "ERROR @wl_cfg80211_get_station..." messages
  in /var/log/messages since activation of CFG80211 API

* Wed Oct 17 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-5.1
- Cleaned up patch for kernel >= 3.6

* Tue Oct 16 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-5
- Added patch to build for kernel >= 3.6

* Wed Oct 10 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-4.1
- Added patch to build with CFG80211 API as default for F-17

* Sun Jun 24 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-3.1
- spec file cleanup

* Fri Jun 08 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-3
- Added patch to build for kernel >= 3.4

* Thu Apr 19 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-2.1
- Rebuilt for Rawhide

* Tue Feb 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-2.1
- Rebuild for UsrMove

* Mon Jan 09 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-2
- Added patch to build for kernel >= 3.2

* Mon Nov 07 2011 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-1
- Updated version to 5.100.82.112

* Sat Nov 05 2011 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.38-1.1
- Rebuilt for F-16

* Fri Nov 04 2011 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.38-1
- Updated version to 5.100.82.38

* Wed Nov 02 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.60.48.36-2.12
- rebuild for updated kernel

* Sun Oct 30 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.60.48.36-2.11
- rebuild for updated kernel

* Wed Oct 19 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.60.48.36-2.10
- rebuild for updated kernel

* Fri Oct 07 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.60.48.36-2.9
- rebuild for updated kernel

* Sat Sep 03 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.60.48.36-2.8
- rebuild for updated kernel

* Wed Aug 17 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.60.48.36-2.7
- rebuild for updated kernel

* Sun Jul 31 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.60.48.36-2.6
- rebuild for updated kernel

* Tue Jul 12 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.60.48.36-2.5
- Rebuild for updated kernel

* Wed Jun 15 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-2.4
- rebuild for updated kernel

* Sat Jun 04 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-2.3
- rebuild for updated kernel

* Sat May 28 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-2.2
- rebuild for updated kernel

* Sat May 28 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-2.1
- rebuild for F15 release kernel

* Sun Sep 26 2010 Chris Nolan <chris@cenolan.com> - 5.60.48.36-2
- added patch for kernel > 2.6.33
- added multicast kernel patch
- added bogus debug_lockdep_rcu_enabled patch

* Mon Feb 22 2010 Chris Nolan <chris@cenolan.com> - 5.60.48.36-1
- Updated version to 5.60.48.36

* Tue Feb 09 2010 Chris Nolan <chris@cenolan.com> - 5.10.91.9.3-4
- added patch for linux kernel 2.6.32

* Sun Nov 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.91.9.3-3.7
- rebuild for new kernel, disable i586 builds

* Tue Nov 10 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.91.9.3-3.6
- rebuild for F12 release kernel

* Mon Nov 09 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.91.9.3-3.5
- rebuild for new kernels

* Fri Nov 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.91.9.3-3.4
- rebuild for new kernels

* Wed Nov 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.91.9.3-3.3
- rebuild for new kernels

* Sat Oct 24 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.91.9.3-3.2
- rebuild for new kernels

* Wed Oct 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.91.9.3-3.1
- rebuild for new kernels

* Sat Sep 19 2009 Chris Nolan <chris@cenolan.com> - 5.10.91.9.3-3
- fixed licence patch

* Sat Sep 19 2009 Chris Nolan <chris@cenolan.com> - 5.10.91.9.3-2
- new licence patch

* Sat Sep 19 2009 Chris Nolan <chris@cenolan.com> - 5.10.91.9.3-1
- updated to 5.10.91.9.3

* Sat Sep 19 2009 Chris Nolan <chris@cenolan.com> - 5.10.91.9-1
- updated to 5.10.91.9

* Fri Jun 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.9
- rebuild for final F11 kernel

* Thu May 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.8
- rebuild for new kernels

* Wed May 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.7
- rebuild for new kernels

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.6
- rebuild for new kernels

* Wed May 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.5
- rebuild for new kernels

* Tue May 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.4
- rebuild for new kernels

* Sat May 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.3
- rebuild for new kernels

* Sun Apr 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.2
- rebuild for new kernels

* Sun Apr 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.1
- rebuild for new kernels

* Sat Mar 28 2009 Chris Nolan <chris@cenolan.com> - 5.10.79.10-2
- repatched to load lib80211_crypt_tkip module - bug #466

* Sun Mar 08 2009 Chris Nolan <chris@cenolan.com> - 5.10.79.10-1
- update version to 5.10.79.10

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.14-1.2
- rebuild for latest Fedora kernel;

* Tue Feb 03 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.14-1.1
- rebuilt

* Sun Feb 01 2009 Chris Nolan <chris@cenolan.com> - 5.10.27.14-1
- update version to 5.10.27.14
- added patch to build against 2.6.29 kernel

* Sun Feb 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.12-1.4
- rebuild for latest Fedora kernel;

* Sun Jan 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.12-1.3
- rebuild for latest Fedora kernel;

* Sun Jan 18 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.12-1.2
- rebuild for latest Fedora kernel;

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.12-1.1
- rebuild for latest Fedora kernel;

* Sun Jan 04 2009 Chris Nolan <chris@cenolan.com> - 5.10.27.12-1
- Update version to 5.10.27.12
- Remove vlanmode and build patches

* Sun Jan 04 2009 Chris Nolan <chris@cenolan.com> - 5.10.27.11-1.2
- added patch for building on 2.6.29 kernel

* Sun Jan 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.11-1.1
- rebuild for latest Fedora kernel;

* Wed Dec 31 2008 Chris Nolan <chris@cenolan.com> 5.10.27.11-1
- Update version to 5.10.27.11

* Sun Dec 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.6-5.8
- rebuild for latest Fedora kernel;

* Sun Dec 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.6-5.7
- rebuild for latest Fedora kernel;

* Sun Dec 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.6-5.6
- rebuild for latest Fedora kernel;

* Sat Nov 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.6-5.5
- rebuild for latest Fedora kernel;

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.6-5.4
- rebuild for latest Fedora kernel;

* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.6-5.3
- rebuild for latest Fedora kernel;

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.6-5.2
- rebuild for latest Fedora kernel;

* Sun Nov 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.6-5.1
- rebuild for latest Fedora kernel;

* Sat Nov 08 2008 Chris Nolan <chris@cenolan.com> 5.10.27.6-5
- Fixed incorrect use of /usr/src/kernels/${kernel_version%%___*}

* Sun Nov 02 2008 Chris Nolan <chris@cenolan.com> 5.10.27.6-4
- Just a spec file tidy up, nothing new

* Thu Oct 30 2008 Chris Nolan <chris@cenolan.com> 5.10.27.6-3
- Moved userland package broadcom-wl into separate package

* Mon Oct 27 2008 Chris Nolan <chris@cenolan.com> 5.10.27.6-2
- Patch to fix vlanmode issue which prevents SSH connections when the driver is used.
- Changed kmod name to wl-kmod as per convention
- Added userland package broadcom-wl which provides kmod-wl-common which contains the required license doc

* Sat Oct 25 2008 Jarod Wilson <jarod@wilsonet.com> 5.10.27.6-1
- Initial build.
