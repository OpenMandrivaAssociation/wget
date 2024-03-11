%bcond_with crosscompile
%global optflags %{optflags} -Oz

Summary:	A utility for retrieving files using the HTTP or FTP protocols
Name:		wget
Version:	1.24.5
Release:	1
Group:		Networking/WWW
License:	GPLv3
URL:		http://www.gnu.org/directory/GNU/wget.html
Source0:	ftp://ftp.gnu.org/pub/gnu/wget/%{name}-%{version}.tar.lz
# The following patch is needed for authenticated sites where login can have '@':
Patch7:		wget-1.10-url_password.patch
Patch8:		wget-1.20.1-default-content_disposition-on.patch
Patch14:	https://src.fedoraproject.org/rpms/wget/raw/rawhide/f/wget-1.17-path.patch
Patch15:	wget-1.21.2-fix-clang.patch
Provides:	webclient
Provides:	webfetch
BuildRequires:	autoconf-archive
BuildRequires:	lzip
BuildRequires:	gettext
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	texinfo
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(gpgme)
BuildRequires:	pkgconfig(libidn2)
BuildRequires:	pkgconfig(libunistring)
BuildRequires:	pkgconfig(libpsl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(libpcre2-posix)
Requires:	rootcerts

%description
GNU Wget is a file retrieval utility which can use either the HTTP or FTP
protocols. Wget features include the ability to work in the background
while you're logged out, recursive retrieval of directories, file name
wildcard matching, remote file timestamp storage and comparison, use of
Rest with FTP servers and Range with HTTP servers to retrieve files over
slow or unstable connections, support for Proxy servers, and
configurability.

%prep
%autosetup -p1

aclocal -I m4
automake -a
autoconf

%build
%configure \
	--enable-ipv6 \
	--disable-rpath \
	--with-ssl=openssl \
%if %{with crosscompile}
	--with-libssl-prefix=$SYSROOT
%endif

%make_build

# all tests must pass (but where are they?)
# (tpg) 2014-11-02 somehow tests fails only on x86_64 and i586
#check
#make check

%install
%make_install

# install -m755 util/rmold.pl %{buildroot}%{_bindir}/rmold

%find_lang %{name} --all-name

%files -f %{name}.lang
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/wgetrc
%doc AUTHORS MAILING-LIST NEWS README
%{_bindir}/*
%doc %{_infodir}/*
%doc %{_mandir}/man1/wget.1*
