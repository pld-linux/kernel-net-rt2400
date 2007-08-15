#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
%bcond_with	grsec_kernel	# build for kernel-grsecurity
#
%if %{with kernel} && %{with dist_kernel} && %{with grsec_kernel}
%define	alt_kernel	grsecurity
%endif
#
%define		_modname	rt2400
%define		snap	cvs-2007081514
%define		_rel	1
Summary:	Linux driver for WLAN cards based on RT2400
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie RT2400
Name:		kernel%{_alt_kernel}-net-rt2400
Version:	1.2.2
Release:	%{_rel}
License:	GPL v2
Group:		Base/Kernel
# Source0:	http://dl.sourceforge.net/rt2400/%{name}-%{version}%{snap}.tar.gz
Source0:	http://rt2x00.serialmonkey.com/%{_modname}-cvs-daily.tar.gz
# Source0-md5:	4db66a1e38ec5268704eaf8a6dd82bdb
URL:		http://rt2x00.serialmonkey.com/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%{?with_dist_kernel:%requires_releq_kernel}
%{?with_dist_kernel:Requires(postun):   kernel}
BuildRequires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Linux driver for WLAN cards based on RT2400.

This package contains Linux module.

%description -l pl.UTF-8
Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie
RT2400.

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -q -n %{_modname}-%{snap}

%build
%build_kernel_modules -C Module -m rt2400 \
%ifarch sparc
	EXTRA_CFLAGS="-fno-schedule-insns"
	# workaround for (probably GCC) bug on sparc:
	# `unable to find a register to spill in class `FP_REGS''
%else
	# beware of evil '\'
%endif

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m Module/rt2400 -d kernel/drivers/net/wireless

%clean
rm -rf $RPM_BUILD_ROOT

%post 
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*.ko*
