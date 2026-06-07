#
# Conditional build:
%bcond_with	tests	# unit tests (need litestar, proxy.py, trustme, pytest-trio
			# and a local HTTP server - not packaged in PLD yet)
#
%define		module	curl_cffi
Summary:	Python binding for curl-impersonate via cffi
Summary(pl.UTF-8):	Wiązanie Pythona do curl-impersonate przez cffi
Name:		python3-curl-cffi
Version:	0.15.0
Release:	3
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/curl-cffi/
Source0:	https://files.pythonhosted.org/packages/source/c/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	108ff8b07bacb0c292471f31025b4c7b
Patch0:		curl-cffi-system-libcurl.patch
URL:		https://github.com/lexiforest/curl_cffi
BuildRequires:	curl-impersonate-devel
BuildRequires:	python3-build
BuildRequires:	python3-cffi >= 2.0.0
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-installer
BuildRequires:	python3-setuptools
BuildRequires:	python3-wheel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with tests}
BuildRequires:	python3-pytest
%endif
Requires:	python3-certifi
Requires:	python3-cffi >= 2.0.0
Requires:	python3-rich
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
curl_cffi is a Python binding for curl-impersonate built with cffi. It
can impersonate the TLS/JA3 and HTTP/2 fingerprints of real browsers,
and offers a requests/httpx-like API for both synchronous and
asynchronous use.

%description -l pl.UTF-8
curl_cffi to wiązanie Pythona do curl-impersonate zbudowane przy
użyciu cffi. Potrafi podszywać się pod odciski TLS/JA3 oraz HTTP/2
prawdziwych przeglądarek i udostępnia API w stylu requests/httpx do
użytku synchronicznego oraz asynchronicznego.

%prep
%setup -q -n %{module}-%{version}
%patch -P0 -p1

%build
export CURL_IMPERSONATE_LIBDIR="%{_libdir}"
export CURL_IMPERSONATE_INCLUDEDIR="%{_includedir}/curl-impersonate"
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests/unittest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_bindir}/curl-cffi
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/py.typed
%{py3_sitedir}/%{module}/_wrapper*.so
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/%{module}/cli
%{py3_sitedir}/%{module}/requests
%{py3_sitedir}/%{module}-%{version}.dist-info
