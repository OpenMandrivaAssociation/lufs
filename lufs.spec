# *** OPTIONS ***
# --with-plf : builds the Gnutella filesystem as well
# --with-debug : confiugres with --enable-debug

%define name    	lufs
%define version 	0.9.7
%define _release 	8

%define	major		2
%define	gnetmajor	1
%define libname		%mklibname %name %major
%define libgnetname	%mklibname %{name}-gnet %gnetmajor

# exclude gntella filesystem from Mandrake package
%define with_plf 0
%define with_gnetfs 0
%{?_without_plf:	%{expand: %%global with_plf 0}}
%{?_with_plf:		%{expand: %%global with_plf 1}}
%if %with_plf
%define release %{_release}plf
%global with_gnetfs 1
%else
%define release  %mkrel %{_release}
%endif

# provide debug option for developers
%define with_debug 0
%{?_without_debug:	%{expand: %%global with_debug 0}}
%{?_with_debug:		%{expand: %%global with_debug 1}}

Summary:	Linux Userland File System
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File tools
URL:		http://lufs.sourceforge.net
Source0:	%{name}-%{version}.tar.bz2
Patch0:		lufs-0.9.7_gnetfs_config.in.patch.bz2
Patch1:		lufs-0.9.7_dont_run_ldconfig.patch.bz2
Patch2:		lufs-0.9.7-no-gnome.patch.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	automake1.9
# for sshfs detection
BuildRequires:	openssh-clients
Requires:	%{libname} = %{version}-%{release}
PreReq:		rpm-helper
%define _requires_exceptions devel(

%description
LUFS is a hybrid userspace filesystem framework supporting many filesystems:
sshfs, ftpfs, localfs, locasefs, gvfs, etc.  Lots of other "exotic" filesystems
are in the planning phase: socketfs, httpfs, freenetfs and others.

#general packages
%package -n %libname
Summary:	Filesystem modules for lufs
Group:		System/Libraries
%description -n %libname
This package contains the modules for the diferent filesystems, in particular:
sshfs, ftpfs, localfs, locasefs

%package -n %libname-devel
Summary:	Development files for the lufs
Group:		Development/C
Requires: 	%{libname} >= %{version}
Provides: 	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes: 	%name-devel
%description -n %libname-devel
This package development files for the diferent filesystems, in particular:
sshfs, ftpfs, localfs, locasefs, gvfs

%package -n %libgvfsname
Summary:	GNOME VFS filesystem module for lufs
Group:		System/Libraries
%description -n %libgvfsname
This package contains the gnome-vfs module for lufs.

%package -n %libgnetname
Summary:	Gnutela filesystem module for lufs
Group:		System/Libraries
%description -n %libgnetname
This package contains the Gnutella module for lufs.

%package -n %libgnetname-devel
Summary:	Development files for the lufs
Group:		Development/C
Requires:	%libgnetname = %version-%release
Provides:	lib%name-gnet-devel = %version-%release
%description -n %libgnetname-devel
This package development files for Gnutella support in lufs.

%prep
%setup -q
%patch0 -p1 -b .detect-gnutella
%patch1 -p1 -b .no-ldconfig
%patch2 -p1 -b .no-gnome

libtoolize --force --copy
ACLOCAL=aclocal-1.9 AUTOMAKE=automake-1.9 autoreconf --force --install

%build
%configure2_5x \
	--disable-kernel-support \
%if %with_gnetfs
 --enable-gnetfs \
%endif
%if %with_debug
 --enable-debug
%endif

%{make}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std 

##
## fix symlinks
##
(cd %{buildroot}%{_sysconfdir} && %__ln_s -f ../%{_bindir}/auto* .)
(cd %{buildroot}/sbin && %__ln_s -f ../%{_bindir}/lufsd ./mount.lufs)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog Contributors NEWS README THANKS TODO
/sbin/*
%{_bindir}/auto.ftpfs
%{_bindir}/auto.sshfs
%{_bindir}/lussh
%{_bindir}/lufsd
%{_bindir}/lufsmnt
%{_bindir}/lufsmount
%{_bindir}/lufsumount
%{_sysconfdir}/auto.ftpfs
%{_sysconfdir}/auto.sshfs
%config(noreplace) %{_sysconfdir}/lufsd.conf
%{_mandir}/man1/*

%files -n %libname
%defattr(-,root,root)
%{_libdir}/*ftp*.so.*
%{_libdir}/*ftp*.so
%{_libdir}/*localfs*.so.*
%{_libdir}/*localfs*.so
%{_libdir}/*locasefs*.so.*
%{_libdir}/*locasefs*.so
%{_libdir}/*ssh*.so.*
%{_libdir}/*ssh*.so

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files -n %libname-devel
%defattr(-,root,root)
%{_libdir}/*ftp*.la
%{_libdir}/*localfs*.la
%{_libdir}/*locasefs*.la
%{_libdir}/*ssh*.la
%{_includedir}/lufs

%if %with_gnetfs

%files -n %libgnetname
%defattr(-,root,root)
%{_libdir}/*gnetfs*.so.*
%{_libdir}/*gnetfs*.so

%post -n %libgnetname -p /sbin/ldconfig
%postun -n %libgnetname -p /sbin/ldconfig

%files -n %libgnetname-devel
%defattr(-,root,root)
%{_libdir}/*gnetfs*.la

%endif

