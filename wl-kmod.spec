# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
#global buildforkernels newest

Name:       wl-kmod
Version:    5.100.82.112
Release:    11%{?dist}.6
Summary:    Kernel module for Broadcom wireless devices
Group:      System Environment/Kernel
License:    Redistributable, no modification permitted
URL:        http://www.broadcom.com/support/802.11/linux_sta.php
Source0:    http://www.broadcom.com/docs/linux_sta/hybrid-portsrc_x86_32-v5_100_82_112.tar.gz
Source1:    http://www.broadcom.com/docs/linux_sta/hybrid-portsrc_x86_64-v5_100_82_112.tar.gz
Source11:   broadcom-wl-kmodtool-excludekernel-filterfile
Patch0:     broadcom-wl-5.100.82.112-license.patch
Patch1:     broadcom-wl-5.100.82.112-kernel-3.2.patch
Patch2:     broadcom-wl-5.100.82.112-kernel-3.4.patch
Patch3:     broadcom-wl-5.100.82.112-cfg80211.patch
Patch4:     broadcom-wl-5.100.82.112-kernel-3.6.patch
Patch5:     broadcom-wl-5.100.82.112-recent_kernel_semaphore.patch
Patch6:     broadcom-wl-5.100.82.112-recent_kernel_ioctl.patch
Patch7:     broadcom-wl-5.100.82.112-wext_workaround.patch
Patch8:     broadcom-wl-5.100.82.112-kernel-3.8.patch
Patch9:     broadcom-wl-5.100.82.112-kernel-3.9.patch
Patch10:    broadcom-wl-5.100.82.112-kernel-3.10.patch

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
BCM4322-, BCM43224-, and BCM43225-, BCM43227- and BCM43228-based hardware.

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
%patch1  -p1 -b .kernel-3.2
%patch2  -p1 -b .kernel-3.4
%patch3  -p1 -b .cfg80211
%patch4  -p1 -b .kernel-3.6
%patch5  -p1 -b .recent_kernel_semaphore
%patch6  -p1 -b .recent_kernel_ioctl
%patch7  -p1 -b .wext_workaround.patch
%patch8  -p1 -b .kernel-3.8
%patch9  -p1 -b .kernel-3.9
%patch10 -p1 -b .kernel-3.10
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
* Fri Aug 16 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-11.6
- Rebuilt for kernel
- Added patch to build for kernel >= 3.10

* Tue Jul 23 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-10.8
- Rebuilt for kernel

* Mon Jul 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-10.7
- Rebuilt for kernel

* Sat Jul 06 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-10.6
- Rebuilt for kernel

* Sun Jun 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-10.5
- Rebuilt for kernel

* Mon Jun 17 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-10.4
- Rebuilt for kernel

* Wed Jun 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-10.3
- Rebuilt for kernel

* Sat May 25 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-10.2
- Rebuilt for kernel

* Wed May 22 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-10.1
- Rebuilt for kernel

* Tue May 14 2013 Nicolas Vieville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-10
- Added patch to build for kernel >= 3.9

* Tue May 14 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-9.12
- Rebuilt for kernel

* Fri May 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-9.11
- Rebuilt for kernel

* Wed May 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-9.10
- Rebuilt for kernel

* Sun Apr 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-9.9
Rebuilt for kernel

* Thu Apr 25 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-9.8
- Rebuilt for kernel

* Thu Apr 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-9.7
- Rebuilt for kernel

* Sat Apr 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-9.6
- Rebuilt for kernel

* Wed Apr 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-9.5
- Rebuilt for kernel

* Tue Apr 02 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-9.4
- Rebuilt for kernel

* Fri Mar 22 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-9.3
- Rebuilt for kernel

* Mon Mar 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-9.2
- Rebuilt for kernel

* Fri Mar 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-9.1
- Rebuilt for kernel

* Mon Mar 11 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-8.1
- Rebuilt for kernel

* Fri Mar 08 2013 Nicolas Vieville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-9
- Modified patch to build for kernel >= 3.8 rfbz#2715

* Fri Mar 01 2013 Nicolas Vieville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-8
- Added patch to build for kernel >= 3.8

* Thu Feb 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-7.16
- Rebuilt for kernel

* Tue Feb 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-7.15
- Rebuilt for kernel

* Thu Feb 21 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-7.14
- Rebuilt for kernel

* Sat Feb 16 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-7.13
- Rebuilt for kernel

* Sat Feb 16 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-7.12
- Rebuilt for kernel

* Wed Feb 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-7.11
- Rebuilt for kernel

* Tue Feb 05 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-7.10
- Rebuilt for kernel

* Wed Jan 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-7.9
- Rebuilt for updated kernel

* Fri Jan 25 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-7.8
- Rebuilt for updated kernel

* Thu Jan 17 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-7.7
- Rebuilt for updated kernel

* Mon Jan 14 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-7.6
- Rebuilt for updated kernel

* Sun Jan 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-7.5
- Rebuilt for updated kernel

* Thu Jan 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-7.4
- Rebuilt for f18 final kernel

* Fri Dec 21 2012 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-7.3
- Rebuilt for current f18 kernel

* Sun Nov 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-7.2
- Rebuilt for current f18 kernel

* Sun Nov 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-7.1
- Rebuilt for Fedora 18 Beta kernel

* Wed Nov 21 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-7
- Added patch to choose API at build time (WEXT or CFG80211) to workaround #2548 #2562
- Others patches cleaned-up

* Sat Oct 20 2012 Nicolas Vieville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-6
- Added patch to include semaphore.h in wl_iw.h
- Added patch from Archlinux to disable too many "ERROR @wl_cfg80211_get_station..." messages
  in /var/log/messages since activation of CFG80211 API

* Wed Oct 17 2012 Nicolas Vieville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-5.1
- Cleaned up patch for kernel >= 3.6

* Tue Oct 16 2012 Nicolas Vieville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-5
- Added patch to build for kernel >= 3.6

* Wed Oct 10 2012 Nicolas Vieville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-4
- Added patch to build with CFG80211 API as default for F-17

* Sun Jun 24 2012 Nicolas Vieville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-3.1
- spec file cleanup

* Fri Jun 08 2012 Nicolas Vieville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-3
- Added patch to build for kernel >= 3.4

* Thu Apr 19 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-2.1
- Rebuilt for Rawhide

* Tue Feb 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-2.1
- Rebuild for UsrMove

* Mon Jan 09 2012 Nicolas Vieville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-2
- Added patch to build for kernel >= 3.2

* Mon Nov 07 2011 Nicolas Vieville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-1
- Updated version to 5.100.82.112

* Sat Nov 05 2011 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.38-1.1
- Rebuilt for F-16

* Fri Nov 04 2011 Nicolas Vieville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.38-1
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
