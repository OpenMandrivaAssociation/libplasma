%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)

# Renamed in 5.90.0
%define oldlibname %mklibname KF6Plasma
%define olddevname %mklibname KF6Plasma -d

%define libname %mklibname Plasma
%define devname %mklibname Plasma -d
#define git 20240222
%define gitbranch Plasma/6.0
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")

Name: plasma6-libplasma
Version: 6.3.2
Release: %{?git:0.%{git}.}1
%if 0%{?git:1}
Source0: https://invent.kde.org/plasma/libplasma/-/archive/%{gitbranch}/libplasma-%{gitbranchd}.tar.bz2#/libplasma-%{git}.tar.bz2
%else
Source0: http://download.kde.org/%{stable}/plasma/%{version}/libplasma-%{version}.tar.xz
%endif
Summary: Foundational libraries, components, and tools of the Plasma workspaces
URL: https://invent.kde.org/frameworks/libplasma
License: CC0-1.0 LGPL-2.0+ LGPL-2.1 LGPL-3.0
Group: System/Libraries
BuildRequires: cmake
BuildRequires: cmake(ECM)
BuildRequires: python
BuildRequires: cmake(Qt6DBusTools)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6QmlTools)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(Qt6GuiTools)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: cmake(Qt6DBusTools)
BuildRequires: cmake(Qt6WaylandClient)
BuildRequires: pkgconfig(wayland-egl)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: gettext
BuildRequires: doxygen
BuildRequires: cmake(Qt6ToolsTools)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: cmake(Qt6QuickControls2)
BuildRequires: cmake(KF6Kirigami2)
BuildRequires: cmake(PlasmaActivities)
BuildRequires: cmake(KF6Archive)
BuildRequires: cmake(KF6Config)
BuildRequires: cmake(KF6ConfigWidgets)
BuildRequires: cmake(KF6CoreAddons)
BuildRequires: cmake(KF6GlobalAccel)
BuildRequires: cmake(KF6GuiAddons)
BuildRequires: cmake(KF6I18n)
BuildRequires: cmake(KF6IconThemes)
BuildRequires: cmake(KF6KIO)
BuildRequires: cmake(KF6WindowSystem)
BuildRequires: cmake(KF6XmlGui)
BuildRequires: cmake(KF6Notifications)
BuildRequires: cmake(KF6Package)
BuildRequires: cmake(KF6KCMUtils)
BuildRequires: cmake(KWayland)
BuildRequires: cmake(KF6Svg)
BuildRequires: cmake(PlasmaWaylandProtocols)
Requires: %{libname} = %{EVRD}
Requires: plasma-framework-common = %{EVRD}
%rename kf6-plasma-framework

#patchlist

%description
Foundational libraries, components, and tools of the Plasma workspaces

%package -n %{libname}
Summary: Foundational libraries, components, and tools of the Plasma workspaces
Group: System/Libraries
Requires: %{name} = %{EVRD}
%rename %{oldlibname}

%description -n %{libname}
Foundational libraries, components, and tools of the Plasma workspaces

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}
%rename %{olddevname}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

Foundational libraries, components, and tools of the Plasma workspaces

# This should be merged back into the main package once we drop KF5
%package -n plasma-framework-common
Summary: Plasma Framework data files common to Plasma 5 and 6
Group: System/Libraries

%description -n plasma-framework-common
Plasma Framework data files common to Plasma 5 and 6

%prep
%autosetup -p1 -n libplasma-%{?git:%{gitbranchd}}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

%find_lang %{name} --all-name --with-qt --with-html

find %{buildroot}%{_datadir}/locale -name "*.js" |while read r; do
    L=$(echo $r |rev |cut -d/ -f4 |rev)
    echo "%%lang($L) %%{_datadir}/locale/$L/LC_SCRIPTS/libplasma6/$(basename $r)" >>%{name}.lang
done


%files -f %{name}.lang
%{_datadir}/qlogging-categories6/plasma-framework.categories
%{_datadir}/qlogging-categories6/plasma-framework.renamecategories

%files -n %{devname}
%{_includedir}/Plasma
%{_includedir}/PlasmaQuick
%{_libdir}/cmake/Plasma
%{_libdir}/cmake/PlasmaQuick
%{_datadir}/kdevappwizard/templates/*
%doc %{_qtdir}/doc/Plasma.*

%files -n %{libname}
%{_libdir}/libPlasma.so*
%{_libdir}/libPlasmaQuick.so*
# FIXME owning the whole /org namespace here
# may be a bit excessive, but there's probably
# no better place
%dir %{_qtdir}/qml/org
%{_qtdir}/qml/org/kde
%{_qtdir}/plugins/kf6/kirigami
%{_qtdir}/plugins/kf6/packagestructure

%files -n plasma-framework-common
%dir %{_datadir}/plasma
%{_datadir}/plasma/desktoptheme
