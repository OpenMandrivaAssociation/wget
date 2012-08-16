Summary:	A utility for retrieving files using the HTTP or FTP protocols
Name:		wget
Version:	1.14
Release:	1
Group:		Networking/WWW
License:	GPLv3
URL:		http://www.gnu.org/directory/GNU/wget.html
Source0:	ftp://ftp.gnu.org/pub/gnu/wget/%{name}-%{version}.tar.xz
Source1:	%{SOURCE0}.sig
# The following patch is needed for authenticated sites where login can have '@':
Patch7:		wget-1.10-url_password.patch
Patch9:		wget-1.11-logstdout.patch
# needed by urpmi, inspired by http://matthewm.boedicker.org/code/src/wget_force_clobber.patch
Patch13:	wget-1.13.3-add-force-clobber-option.patch
Provides:	webclient
Provides:	webfetch
BuildRequires:	gettext
BuildRequires:	openssl-devel
BuildRequires:	texinfo
BuildRequires:	idn-devel
BuildRequires:	perl(HTTP::Daemon)

%description
GNU Wget is a file retrieval utility which can use either the HTTP or FTP
protocols. Wget features include the ability to work in the background
while you're logged out, recursive retrieval of directories, file name
wildcard matching, remote file timestamp storage and comparison, use of
Rest with FTP servers and Range with HTTP servers to retrieve files over
slow or unstable connections, support for Proxy servers, and
configurability.

%prep

%setup -q
%patch7 -p0 -b .url_password
%patch9 -p1 -b .logstdout
%patch13 -p1 -b .force-clobber

%build
%configure2_5x \
	--enable-ipv6 \
	--disable-rpath \
	--with-ssl=openssl

%make

# all tests must pass (but where are they?)
%check
make check

%install
%makeinstall_std

install -m755 util/rmold.pl %{buildroot}%{_bindir}/rmold

%find_lang %{name}

%if %{mdvver} < 201200
%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info
%endif

%files -f %{name}.lang
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/wgetrc
%doc AUTHORS ChangeLog MAILING-LIST NEWS README
%{_bindir}/*
%{_infodir}/*
%{_mandir}/man1/wget.1*
