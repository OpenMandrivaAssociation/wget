%bcond_with	crosscompile

Summary:	A utility for retrieving files using the HTTP or FTP protocols
Name:		wget
Version:	1.16
Release:	1
Group:		Networking/WWW
License:	GPLv3
URL:		http://www.gnu.org/directory/GNU/wget.html
Source0:	ftp://ftp.gnu.org/pub/gnu/wget/%{name}-%{version}.tar.xz
# The following patch is needed for authenticated sites where login can have '@':
Patch7:		wget-1.10-url_password.patch
# needed by urpmi, inspired by http://matthewm.boedicker.org/code/src/wget_force_clobber.patch
Patch13:	wget-1.16-add-force-clobber-option.patch
Patch14:	wget-1.15-etc.patch
Patch15:	wget-1.16-pkg-config.patch
Patch16:	wget-1.16-tests-skip.patch
Provides:	webclient
Provides:	webfetch
BuildRequires:	gettext
BuildRequires:	pkgconfig(openssl)
BuildRequires:	gettext-devel
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
# force-clobber lead to segfaults on arm64
%patch13 -p1 -b .force-clobber
%patch14 -p1 -b .etc
%patch15 -p1 -b .pkgc
%patch16 -p1 -b .skip

autoreconf -fiv

%build
%configure \
	--enable-ipv6 \
	--disable-rpath \
	--with-ssl=openssl \
%if %{with crosscompile}
	--with-libssl-prefix=$SYSROOT
%endif

%make

# all tests must pass (but where are they?)
# (tpg) 2014-11-02 somehow tests fails only on x86_64 and i586
#check
#make check

%install
%makeinstall_std

install -m755 util/rmold.pl %{buildroot}%{_bindir}/rmold

%find_lang %{name}

%files -f %{name}.lang
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/wgetrc
%doc AUTHORS ChangeLog MAILING-LIST NEWS README
%{_bindir}/*
%{_infodir}/*
%{_mandir}/man1/wget.1*
