Name:       qt5-qtx11extras
Summary:    Cross-platform application and UI framework
Version:    5.2.1
Release:    1%{?dist}
Group:      Qt/Qt
License:    LGPLv2.1 with exception or GPLv3
URL:        http://qt-project.org/
Source0:    %{name}-%{version}.tar.xz
BuildRequires:  qt5-qtcore
BuildRequires:  qt5-qtcore-devel
BuildRequires:  qt5-qtgui
BuildRequires:  qt5-qtgui-devel
BuildRequires:  qt5-qtwidgets
BuildRequires:  qt5-qtwidgets-devel
BuildRequires:  qt5-qtopengl
BuildRequires:  qt5-qtopengl-devel
BuildRequires:  qt5-qtnetwork
BuildRequires:  qt5-qtnetwork-devel
BuildRequires:  qt5-qmake
BuildRequires:  qt5-tools
BuildRequires:  pkgconfig(xcb) pkgconfig(xcb-glx) pkgconfig(xcb-icccm) pkgconfig(xcb-image) pkgconfig(xcb-keysyms) pkgconfig(xcb-renderutil)
BuildRequires:  fdupes gcc-c++

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

The X11 Extras module provides features specific to platforms using X11, e.g.
Linux and UNIX-like systems including embedded Linux systems that use the X
Window System.


%package devel
Summary:    Development files for QtX11Extras
Group:      Qt/Qt
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains the files necessary to develop
applications that use QtX11Extras,


%prep
%setup -q -n %{name}-%{version}/upstream


%build
cat > src/src.pro <<EOF
TEMPLATE = subdirs
SUBDIRS += x11extras
EOF

export QTDIR=/usr/share/qt5
touch .git
%qmake5
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
%qmake5_install
# Remove unneeded .la files
rm -f %{buildroot}/%{_libdir}/*.la
# We don't need qt5/Qt/
rm -rf %{buildroot}/%{_includedir}/qt5/Qt

# Fix wrong path in pkgconfig files
find %{buildroot}%{_libdir}/pkgconfig -type f -name '*.pc' \
-exec perl -pi -e "s, -L%{_builddir}/?\S+,,g" {} \;
# Fix wrong path in prl files
find %{buildroot}%{_libdir} -type f -name '*.prl' \
-exec sed -i -e "/^QMAKE_PRL_BUILD_DIR/d;s/\(QMAKE_PRL_LIBS =\).*/\1/" {} \;

%fdupes %{buildroot}/%{_includedir}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/libQt5X11Extras.so.5*

%files devel
%defattr(-,root,root,-)
%{_includedir}/qt5/QtX11Extras/
%{_libdir}/libQt5X11Extras.so
%{_libdir}/libQt5X11Extras.prl
%{_libdir}/cmake/
%{_libdir}/pkgconfig/*
%{_datadir}/qt5/mkspecs/modules/qt_lib_x11extras*.pri
