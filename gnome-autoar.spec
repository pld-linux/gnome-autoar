#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	Automatic archives creating and extracting library
Summary(pl.UTF-8):	Biblioteka do automatycznego tworzenia i rozpakowywania archiwów
Name:		gnome-autoar
Version:	0.1
%define	snap	20141015
%define	gitref	0300e4b31253779541a6f078ca45bd7a3bd6e7db
Release:	0.%{snap}.1
License:	LGPL v2+
Group:		Libraries
Source0:	https://github.com/GNOME/gnome-autoar/archive/%{gitref}/%{name}-%{version}.tar.gz
# Source0-md5:	0257c1286311ce1e5c6a251491a6a7a4
Patch0:		%{name}-pc.patch
URL:		https://github.com/GNOME/gnome-autoar/
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.36
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gtk+3-devel >= 3.2
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	libarchive-devel >= 3.1.0
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.592
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	glib2 >= 1:2.36
Requires:	glib2 >= 1:2.36
Requires:	libarchive >= 3.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gnome-autoar provides functions, widgets, and gschemas for GNOME
applications which want to use archives as a convient method to
tranfer directories over the Internet.

%description -l pl.UTF-8
gnome-autoar udostępnia funkcje, widgety oraz gschema dla aplikacji
GNOME chcących używać archiwów jako wygodnej metody przesyłania
katalogów przez Internet.

%package devel
Summary:	Header files for gnome-autoar library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gnome-autoar
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.36
Requires:	libarchive-devel >= 3.1.0

%description devel
Header files for gnome-autoar library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gnome-autoar.

%package static
Summary:	Static gnome-autoar library
Summary(pl.UTF-8):	Statyczna biblioteka gnome-autoar
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static gnome-autoar library.

%description static -l pl.UTF-8
Statyczna biblioteka gnome-autoar.

%package gtk
Summary:	GTK+ widgets library for gnome-autoar
Summary(pl.UTF-8):	Biblioteka widgetów GTK+ dla biblioteki gnome-autoar
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+3 >= 3.2

%description gtk
gnome-autoar-gtk provides widgets for gnome-autoar library.

%description gtk -l pl.UTF-8
gnome-autoar-gtk udostępnia widgety dla biblioteki gnome-autoar.

%package gtk-devel
Summary:	Header files for gnome-autoar-gtk library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gnome-autoar-gtk
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-gtk = %{version}-%{release}
Requires:	gtk+3-devel >= 3.2

%description gtk-devel
Header files for gnome-autoar-gtk library.

%description gtk-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gnome-autoar-gtk.

%package gtk-static
Summary:	Static gnome-autoar-gtk library
Summary(pl.UTF-8):	Statyczna biblioteka gnome-autoar-gtk
Group:		X11/Development/Libraries
Requires:	%{name}-gtk-devel = %{version}-%{release}

%description gtk-static
Static gnome-autoar-gtk library.

%description gtk-static -l pl.UTF-8
Statyczna biblioteka gnome-autoar-gtk.

%package apidocs
Summary:	gnome-autoar API documentation
Summary(pl.UTF-8):	Dokumentacja API bibliotek gnome-autoar
Group:		Documentation

%description apidocs
API documentation for gnome-autoar libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek gnome-autoar.

%prep
%setup -q -n %{name}-%{gitref}
%patch0 -p1

%build
%{__libtoolize}
%{__gtkdocize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgnome-autoar*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%glib_compile_schemas

%postun
/sbin/ldconfig
%glib_compile_schemas

%post	gtk -p /sbin/ldconfig
%postun	gtk -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-autoar.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnome-autoar.so.0
%{_libdir}/girepository-1.0/GnomeAutoar-0.1.typelib
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.archives.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.archives.gschema.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-autoar.so
%{_datadir}/gir-1.0/GnomeAutoar-0.1.gir
%dir %{_includedir}/gnome-autoar
%{_includedir}/gnome-autoar/autoar.h
%{_includedir}/gnome-autoar/autoar-create.h
%{_includedir}/gnome-autoar/autoar-extract.h
%{_includedir}/gnome-autoar/autoar-format-filter.h
%{_includedir}/gnome-autoar/autoar-misc.h
%{_includedir}/gnome-autoar/autoar-pref.h
%{_pkgconfigdir}/gnome-autoar.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgnome-autoar.a
%endif

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-autoar-gtk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnome-autoar-gtk.so.0
%{_libdir}/girepository-1.0/GnomeAutoarGtk-0.1.typelib

%files gtk-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-autoar-gtk.so
%{_datadir}/gir-1.0/GnomeAutoarGtk-0.1.gir
%{_includedir}/gnome-autoar/autoar-gtk.h
%{_includedir}/gnome-autoar/autoar-gtk-chooser.h
%{_pkgconfigdir}/gnome-autoar-gtk.pc

%if %{with static_libs}
%files gtk-static
%defattr(644,root,root,755)
%{_libdir}/libgnome-autoar-gtk.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gnome-autoar
