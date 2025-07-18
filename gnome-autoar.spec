#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries

Summary:	Automatic archives creating and extracting library
Summary(pl.UTF-8):	Biblioteka do automatycznego tworzenia i rozpakowywania archiwów
Name:		gnome-autoar
Version:	0.4.5
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/gnome-autoar/0.4/%{name}-%{version}.tar.xz
# Source0-md5:	c8028c4df62c059418d4bdcde345cbe2
Patch0:		%{name}-pc.patch
URL:		https://github.com/GNOME/gnome-autoar/
BuildRequires:	glib2-devel >= 1:2.36
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gtk+3-devel >= 3.2
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.14}
BuildRequires:	libarchive-devel >= 3.4.0
BuildRequires:	meson >= 0.58.0
BuildRequires:	pkgconfig
BuildRequires:	ninja >= 1.5
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.22.0
BuildRequires:	xz
Requires(post,postun):	/sbin/ldconfig
Requires:	glib2 >= 1:2.36
Requires:	libarchive >= 3.4.0
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
Requires:	libarchive-devel >= 3.4.0

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

%package -n vala-gnome-autoar
Summary:	gnome-autoar API for Vala language
Summary(pl.UTF-8):	API gnome-autoar dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.22.0
BuildArch:	noarch

%description -n vala-gnome-autoar
gnome-autoar API for Vala language.

%description -n vala-gnome-autoar -l pl.UTF-8
API gnome-autoar dla języka Vala.

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

%package -n vala-gnome-autoar-gtk
Summary:	gnome-autoar-gtk API for Vala language
Summary(pl.UTF-8):	API gnome-autoar-gtk dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-gtk-devel = %{version}-%{release}
Requires:	vala-gnome-autoar = %{version}-%{release}
BuildArch:	noarch

%description -n vala-gnome-autoar-gtk
gnome-autoar-gtk API for Vala language.

%description -n vala-gnome-autoar-gtk -l pl.UTF-8
API gnome-autoar-gtk dla języka Vala.

%package apidocs
Summary:	gnome-autoar API documentation
Summary(pl.UTF-8):	Dokumentacja API bibliotek gnome-autoar
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for gnome-autoar libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek gnome-autoar.

%prep
%setup -q
%patch -P0 -p1

%if %{with static_libs}
%{__sed} -i -e '/^libgnome_autoar\(_gtk\)\? =/ s/shared_library/library/' gnome-autoar/meson.build
%endif

%build
%meson \
	%{?with_apidocs:-Dgtk_doc=true} \
	-Dvapi=true

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post	gtk -p /sbin/ldconfig
%postun	gtk -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-autoar-0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnome-autoar-0.so.0
%{_libdir}/girepository-1.0/GnomeAutoar-0.1.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-autoar-0.so
%{_datadir}/gir-1.0/GnomeAutoar-0.1.gir
%dir %{_includedir}/gnome-autoar-0
%dir %{_includedir}/gnome-autoar-0/gnome-autoar
%{_includedir}/gnome-autoar-0/gnome-autoar/autoar-compressor.h
%{_includedir}/gnome-autoar-0/gnome-autoar/autoar-enum-types.h
%{_includedir}/gnome-autoar-0/gnome-autoar/autoar-extractor.h
%{_includedir}/gnome-autoar-0/gnome-autoar/autoar-mime-types.h
%{_includedir}/gnome-autoar-0/gnome-autoar/autoar-format-filter.h
%{_includedir}/gnome-autoar-0/gnome-autoar/autoar-misc.h
%{_includedir}/gnome-autoar-0/gnome-autoar/gnome-autoar.h
%{_pkgconfigdir}/gnome-autoar-0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgnome-autoar-0.a
%endif

%files -n vala-gnome-autoar
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gnome-autoar-0.deps
%{_datadir}/vala/vapi/gnome-autoar-0.vapi

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-autoar-gtk-0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnome-autoar-gtk-0.so.0
%{_libdir}/girepository-1.0/GnomeAutoarGtk-0.1.typelib

%files gtk-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-autoar-gtk-0.so
%{_datadir}/gir-1.0/GnomeAutoarGtk-0.1.gir
%{_includedir}/gnome-autoar-0/gnome-autoar/autoar-gtk.h
%{_includedir}/gnome-autoar-0/gnome-autoar/autoar-gtk-chooser.h
%{_pkgconfigdir}/gnome-autoar-gtk-0.pc

%if %{with static_libs}
%files gtk-static
%defattr(644,root,root,755)
%{_libdir}/libgnome-autoar-gtk-0.a
%endif

%files -n vala-gnome-autoar-gtk
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gnome-autoar-gtk-0.deps
%{_datadir}/vala/vapi/gnome-autoar-gtk-0.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gnome-autoar
%endif
