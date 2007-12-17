Summary: 	A utility for retrieving files using the HTTP or FTP protocols
Name: 		wget
Version: 	1.10.2
Release: 	%mkrel 6
Group: 		Networking/WWW
License: 	GPL
URL: 		http://www.gnu.org/directory/GNU/wget.html
Source0:	ftp://prep.ai.mit.edu/pub/gnu/%{name}-%{version}.tar.bz2
# alt: ftp://ftp.gnu.org/gnu/wget/
Patch0: 	wget-1.10.2-passive_ftp.patch
Patch1: 	wget-1.10-print_percentage.patch
Patch3:		wget-1.8-no-solaris-md5.h.patch
Patch4:		wget-1.8.1-etc.patch
Patch7:		wget-1.10-url_password.patch
Patch9:		wget-1.10-logstdout.patch
Patch10:	wget-1.10-referer-opt-typo.patch
Patch11:	wget-1.9.1-fix-fr-translation.patch
Patch12:	wget-1.10.2-CVE-2006-6719.patch
# needed by urpmi, inspired by http://matthewm.boedicker.org/code/src/wget_force_clobber.patch
Patch13:	wget-1.10.2-add-force-clobber-option.patch
Provides: 	webclient webfetch
BuildRequires:	gettext
BuildRequires:	openssl-devel
BuildRequires:	texinfo
#gw if patched:
BuildRequires:  autoconf2.5
Requires(pre):	info-install
Requires(post):	info-install


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
%patch0 -p0 -b .passive_ftp
%patch1 -p0 -b .percentage
%patch3 -p1 -b .md5
%patch4 -p1 -b .etc
%patch7 -p0 -b .url_password
%patch9 -p0 -b .logstdout
%patch10 -p0 -b .typo
%patch11 -p0 -b .frtypo
%patch12 -p1 -b .secfix
%patch13 -p1 -b .force-clobber

%build
#aclocal
autoconf

%configure2_5x --enable-ipv6

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
%doc AUTHORS COPYING ChangeLog MAILING-LIST NEWS README TODO
%{_bindir}/*
%{_infodir}/*
%{_mandir}/man1/wget.1*


