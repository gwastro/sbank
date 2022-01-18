%define srcname sbank
%define version 1.0.0
%define release 1

# -- src.rpm metadata -------

Name:      python-%{srcname}
Version:   %{version}
Release:   %{release}%{?dist}
Summary:   A stochastic gravitational-wave template bank placement library
License:   GPLv2+
Url:       https://github.com/gwastro/sbank
Source0:   %pypi_source

Packager:  Duncan Macleod <duncan.macleod@ligo.org>
Vendor:    Duncan Macleod <duncan.macleod@ligo.org>

Prefix:    %{_prefix}

# -- requirements -----------

# rpmbuild dependencies
BuildRequires: python-srpm-macros
BuildRequires: python-rpm-macros
BuildRequires: python3-rpm-macros

# build dependencies
BuildRequires: gcc
BuildRequires: liblal-devel
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-Cython
BuildRequires: python%{python3_pkgversion}-numpy
BuildRequires: python%{python3_pkgversion}-setuptools >= 30.3.0

# runtime dependencies (required for %check and help2man)
BuildRequires: help2man
BuildRequires: lalapps
BuildRequires: python%{python3_pkgversion}-glue
BuildRequires: python%{python3_pkgversion}-h5py
BuildRequires: python%{python3_pkgversion}-lal
BuildRequires: python%{python3_pkgversion}-lalsimulation
BuildRequires: python%{python3_pkgversion}-ligo-lw-bin
BuildRequires: python%{python3_pkgversion}-matplotlib
BuildRequires: python%{python3_pkgversion}-scipy
BuildRequires: python%{python3_pkgversion}-six

# testing dependencies (required for %check)
%if 0%{?rhel} == 0 || 0%{?rhel} >= 9
BuildRequires: python%{python3_pkgversion}-pytest >= 3.9.1
%endif

# -- src rpm ----------------

%description
Sbank is a library for generating a template bank for compact binary searches
covering a given region of mass and spin parameter space.
The program can support all waveform approximants available in the
lalsimulation suite. Currently implemented waveforms can be found with
`sbank --help` and others added with only minor additions.

Sbank has been developed collaboratively by a diverse group of LIGO scientists
starting in 2012, and has been split off from the larger `lalsuite` package as
a standalone module in 2021.
Sbank has been used to generate template banks for the separate GstLAL, MBTA,
PyCBC and SPIIR analysis codes.
Sbank also offers support for generating precessing and/or higher-order mode
template banks.

# -- packages ---------------

%package -n %{srcname}
Summary: Command-line utilities for Sbank
BuildArch: noarch
Requires: lalapps
Requires: python%{python3_pkgversion}-%{srcname} = %{version}-%{release}
Requires: python%{python3_pkgversion}-glue
Requires: python%{python3_pkgversion}-h5py
Requires: python%{python3_pkgversion}-lal
Requires: python%{python3_pkgversion}-lalsimulation
Requires: python%{python3_pkgversion}-ligo-lw-bin
Requires: python%{python3_pkgversion}-matplotlib
Requires: python%{python3_pkgversion}-numpy
Requires: python%{python3_pkgversion}-scipy
Requires: python%{python3_pkgversion}-six
%description -n %{srcname}
Sbank provides a library for generating template banks of compact binary
mergers for gravitational-wave searches using the "stochastic" placement
algorithm.
The package provides the command-line utilities.

%package -n python%{python3_pkgversion}-%{srcname}
Summary: Python %{python3_version} library for Sbank
Requires: python%{python3_pkgversion}-glue
Requires: python%{python3_pkgversion}-lal
Requires: python%{python3_pkgversion}-lalsimulation
Requires: python%{python3_pkgversion}-numpy
Requires: python%{python3_pkgversion}-six
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
%description -n python%{python3_pkgversion}-%{srcname}
Sbank provides a library for generating template banks of compact binary
mergers for gravitational-wave searches using the "stochastic" placement
algorithm.
The package provides the Python %{python3_version} library.

# -- build steps ------------

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%check
mkdir -p _tests
cd _tests
export PATH="%{buildroot}%{_bindir}:${PATH}"
export PYTHONPATH="%{buildroot}%{python3_sitearch}:%{buildroot}%{python3_sitelib}:${PYTHONPATH}"
%if 0%{?rhel} == 0 || 0%{?rhel} >= 9
%{__python3} -m pytest --color=yes --pyargs %{srcname}
%endif
sbank --help

%install
%py3_install
# generate man pages with elp2man
mkdir -p %{buildroot}%{_mandir}/man1
export PYTHONPATH="%{buildroot}%{python3_sitearch}:%{buildroot}%{python3_sitelib}:${PYTHONPATH}"
ls %{buildroot}%{_bindir}/ | xargs --verbose -I @ \
help2man \
	--output %{buildroot}%{_mandir}/man1/@.1 \
	--no-info \
	--no-discard-stderr \
	--section 1 \
	--source %{srcname} \
	--version-string %{version} \
	%{buildroot}%{_bindir}/@

%clean
rm -rf $RPM_BUILD_ROOT

# -- files ------------------

%files -n %{srcname}
%license COPYING
%doc README.md
%{_bindir}/*
%{_mandir}/man1/*

%files -n python%{python3_pkgversion}-%{srcname}
%license COPYING
%doc README.md
%{python3_sitearch}/*

# -- changelog --------------

%changelog
* Fri May 21 2021 Duncan Macleod <duncan.macleod@ligo.org> - 0.0.2-1
- first build for 0.0.2
