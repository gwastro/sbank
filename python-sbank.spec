%define srcname sbank
%define version 1.0.5
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

# build dependencies
BuildRequires: gcc
BuildRequires: liblal-devel
BuildRequires: python3-devel
BuildRequires: python3-Cython
BuildRequires: python3dist(numpy)
BuildRequires: python3dist(setuptools) >= 30.3.0

# runtime dependencies (required for %check and help2man)
BuildRequires: help2man
BuildRequires: lalapps
BuildRequires: python3-lal
BuildRequires: python3-lalsimulation
BuildRequires: python3-ligo-lw-bin
BuildRequires: python3dist(h5py)
BuildRequires: python3dist(lscsoft-glue)
BuildRequires: python3dist(matplotlib)
BuildRequires: python3dist(scipy)
BuildRequires: python3dist(six)

# testing dependencies (required for %check)
%if 0%{?rhel} == 0 || 0%{?rhel} >= 9
BuildRequires: python3dist(pytest) >= 3.9.1
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
Requires: python3-%{srcname} = %{version}-%{release}
Requires: python3-lal
Requires: python3-lalsimulation
Requires: python3-ligo-lw-bin
Requires: python3dist(h5py)
Requires: python3dist(lscsoft-glue)
Requires: python3dist(matplotlib)
Requires: python3dist(numpy)
Requires: python3dist(scipy)
Requires: python3dist(six)
%description -n %{srcname}
Sbank provides a library for generating template banks of compact binary
mergers for gravitational-wave searches using the "stochastic" placement
algorithm.
The package provides the command-line utilities.

%package -n python3-%{srcname}
Summary: Python %{python3_version} library for Sbank
Requires: python3-lal
Requires: python3-lalsimulation
Requires: python3dist(lscsoft-glue)
Requires: python3dist(numpy)
Requires: python3dist(six)
%description -n python3-%{srcname}
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
# generate man pages with help2man
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

# -- files ------------------

%files -n %{srcname}
%license COPYING
%doc README.md
%{_bindir}/*
%{_mandir}/man1/*

%files -n python3-%{srcname}
%license COPYING
%doc README.md
%{python3_sitearch}/*

# -- changelog --------------

%changelog
* Fri May 21 2021 Duncan Macleod <duncan.macleod@ligo.org> - 0.0.2-1
- first build for 0.0.2
