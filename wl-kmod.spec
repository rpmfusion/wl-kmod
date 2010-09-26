# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
#define buildforkernels newest

Name:		wl-kmod
Version:	5.60.48.36
Release:	2%{?dist}
Summary:	Kernel module for broadcom wireless devices
Group:		System Environment/Kernel
License:	Redistributable, no modification permitted
URL:		http://www.broadcom.com/support/802.11/linux_sta.php
Source0:	http://www.broadcom.com/docs/linux_sta/hybrid-portsrc-x86_32-v5.60.48.36.tar.gz
Source1:	http://www.broadcom.com/docs/linux_sta/hybrid-portsrc-x86_64-v5.60.48.36.tar.gz
Source11:	broadcom-wl-kmodtool-excludekernel-filterfile
Patch0:         broadcom-wl-5.60.48.36-license.patch
Patch1:		broadcom-wl-5.60.48.36-2.6.33-kernel.patch
Patch2:		broadcom-wl-5.60.48.36-multicast-kernel.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	%{_bindir}/kmodtool

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i686 x86_64
# ppc disabled because broadcom only provides x86 and x86_64 bits

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
These packages contain Broadcom's IEEE 802.11a/b/g/n hybrid Linux device
driver for use with Broadcom's BCM4311-, BCM4312-, BCM4321-, and BCM4322
based hardware.

NOTE: You must read the LICENSE.txt file in the docs directory before using
this software.

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
%patch0 -p1 -b .license
%patch1 -p0 -b .kernel
%patch2 -p0 -b .multicast
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
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
 install -m 644 *.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
 popd
done

chmod 0755 $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/*/%{kmodinstdir_postfix}/* || :
%{?akmod_install}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Sep 26 2010 Chris Nolan <chris@cenolan.com> - 5.60.48.36-2
- added 2.6.33 kernel patch
- added multicast patch

* Sun Sep 19 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.18
- rebuild for new kernel

* Sun Sep 19 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.17
- rebuild for new kernel

* Sat Sep 11 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.16
- rebuild for new kernel

* Fri Sep 10 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.15
- rebuild for new kernel

* Sat Aug 28 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.14
- rebuild for new kernel

* Fri Aug 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.13
- rebuild for new kernel

* Wed Aug 11 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.12
- rebuild for new kernel

* Sun Aug 08 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.11
- rebuild for new kernel

* Tue Jul 27 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.10
- rebuild for new kernel

* Wed Jul 07 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.9
- rebuild for new kernel

* Fri Jun 18 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.8
- rebuild for new kernel

* Fri May 28 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.7
- rebuild for new kernel

* Thu May 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.6
- rebuild for new kernel

* Mon May 17 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.5
- rebuild for new kernel

* Fri May 07 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.4
- rebuild for new kernel

* Tue May 04 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.3
- rebuild for new kernel

* Thu Apr 29 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.2
- rebuild for new kernel

* Sun Apr 25 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-1.1
- rebuild for new kernel

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
