Summary: 	A utility for retrieving files using the HTTP or FTP protocols
Name: 		wget
Version: 	1.12
Release: 	%mkrel 4
Group: 		Networking/WWW
License: 	GPLv3
URL: 		http://www.gnu.org/directory/GNU/wget.html
Source0:	ftp://ftp.gnu.org/pub/gnu/wget/%{name}-%{version}.tar.gz
Source1:	%{SOURCE0}.sig
Patch3:		wget-1.8-no-solaris-md5.h.patch
Patch4:		wget-1.11-etc.patch
# The following patch is needed for authenticated sites where login can have '@':
Patch7:		wget-1.10-url_password.patch
Patch9:		wget-1.11-logstdout.patch
Patch10:	wget-1.10-referer-opt-typo.patch
Patch11:	wget-1.9.1-fix-fr-translation.patch
# needed by urpmi, inspired by http://matthewm.boedicker.org/code/src/wget_force_clobber.patch
Patch13:	wget-1.11-add-force-clobber-option.patch
Provides: 	webclient webfetch
BuildRequires:	gettext
BuildRequires:	openssl-devel
BuildRequires:	texinfo
BuildRequires:	idn-devel
#gw if patched:
#BuildRequires:  autoconf2.5
Requires(pre):	info-install
Requires(post):	info-install
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot


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
%patch3 -p0 -b .md5
%patch4 -p1 -b .etc
%patch7 -p0 -b .url_password
%patch9 -p1 -b .logstdout
%patch10 -p0 -b .typo
%patch11 -p0 -b .frtypo
%patch13 -p1 -b .force-clobber

%build
#aclocal
./autogen.sh

%configure2_5x \
	--enable-ipv6 \
	--disable-rpath

%make

# all tests must pass (but where are they?)
%check
make check

%install
rm -rf %{buildroot}

%makeinstall_std

install -m755 util/rmold.pl %{buildroot}/%{_bindir}/rmold

%find_lang %{name}

%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%clean
rm -fr %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/wgetrc
%doc AUTHORS ChangeLog MAILING-LIST NEWS README
%{_bindir}/*
%{_infodir}/*
%{_mandir}/man1/wget.1*
