# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
#%define buildforkernels newest

Name:		wl-kmod
Version:	5.10.27.12
Release:	1%{?dist}.2
Summary:	Kernel module for broadcom wireless devices
Group:		System Environment/Kernel
License:	Redistributable, no modification permitted
URL:		http://www.broadcom.com/support/802.11/linux_sta.php
Source0:	http://www.broadcom.com/docs/linux_sta/hybrid-portsrc-x86-32_5_10_27_12.tar.gz
Source1:	http://www.broadcom.com/docs/linux_sta/hybrid-portsrc-x86-64_5_10_27_12.tar.gz
Source11:	broadcom-wl-kmodtool-excludekernel-filterfile
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	%{_bindir}/kmodtool

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i586 i686 x86_64
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
