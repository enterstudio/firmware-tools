###################################################################
#
# WARNING
#
# These are all automatically replaced by the release script.
# START = Do not edit manually
%define major 1
%define minor 2
%define sub 1
%define extralevel %{nil}
%define release_name firmware-tools
%define release_version %{major}.%{minor}.%{sub}%{extralevel}
#
# END = Do not edit manually
#
###################################################################

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

# SUSE 10 has a crazy distutils.cfg that specifies prefix=/usr/local
# have to override that.
%define suse_prefix %{nil}
%if %(test -e /etc/SuSE-release && echo 1 || echo 0)
%define suse_prefix --prefix=/usr
%endif

# Compat for RHEL3 build
%if %(test "%{dist}" == ".el3" && echo 1 || echo 0)
# add in required ABI (hardcode because /usr/bin/python not available at this point)
Requires:       python-abi = 2.2
# needed for RHEL3 build, python-devel doesnt seem to Require: python in RHEL3
BuildRequires:  python
# override sitelib because this messes up on x86_64
%define python_sitelib /usr/lib/python2.2/site-packages/
%endif

Name:           firmware-tools 
Version:        %{release_version} 
Release:        1%{?dist}
Summary:        Scripts and tools to manage firmware and BIOS updates

Group:          Applications/System
# License is actually GPL/OSL dual license (GPL Compatible), but rpmlint complains
License:        GPL style
URL:            http://linux.dell.com/libsmbios/download/ 
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# This package is noarch for everything except RHEL3. Have to build arch
# specific pkgs for RHEL3
%if %(test "%{dist}" != ".el3" && echo 1 || echo 0)
BuildArch:      noarch
%endif

BuildRequires:  python-devel

Obsoletes: bios_update_tools
Provides:  bios_update_tools
Provides: firmware_inventory(pci)

%description
The firmware-tools project provides tools to inventory hardware and a plugin
architecture so that different OEM vendors can provide different inventory
components. It is intended to tie to the package system to enable seamless
installation of updated firmware via your package manager, as well as provide
a framework for BIOS and firmware updates.


%prep
%setup -q


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/firmware/firmware.d/
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT %{suse_prefix}

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING-GPL COPYING-OSL README
%{python_sitelib}/*
%attr(0755,root,root) %{_bindir}/*
%config(noreplace) %{_sysconfdir}/firmware/firmware.conf
%{_sysconfdir}/firmware/
%{_sysconfdir}/firmware/firmware.d/


%changelog
* Wed Mar 14 2007 Michael E Brown <michael_e_brown at dell.com> - 1.2.0-1
- create and own %{_sysconfdir}/firmware/firmware.d/ for plugins.
* Mon Mar 12 2007 Michael E Brown <michael_e_brown at dell.com> - 1.2.0-1
- Fedora-compliant packaging changes.
