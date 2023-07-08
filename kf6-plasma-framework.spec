%define libname %mklibname KF6Plasma
%define devname %mklibname KF6Plasma -d
%define git 20230707

Name: kf6-plasma-framework
Version: 5.240.0
Release: %{?git:0.%{git}.}1
Source0: https://invent.kde.org/frameworks/plasma-framework/-/archive/master/plasma-framework-master.tar.bz2#/plasma-framework-%{git}.tar.bz2
Summary: Foundational libraries, components, and tools of the Plasma workspaces
URL: https://invent.kde.org/frameworks/plasma-framework
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
BuildRequires: doxygen
BuildRequires: cmake(Qt6ToolsTools)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: cmake(Qt6QuickControls2)
BuildRequires: cmake(KF6Kirigami2)
BuildRequires: cmake(KF6Activities)
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
BuildRequires: cmake(KF6Wayland)
BuildRequires: cmake(KF6Svg)
# Just to make sure we don't pull in the KF5 version
BuildRequires: plasma6-xdg-desktop-portal-kde
Requires: %{libname} = %{EVRD}

%description
Foundational libraries, components, and tools of the Plasma workspaces

%package -n %{libname}
Summary: Foundational libraries, components, and tools of the Plasma workspaces
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{libname}
Foundational libraries, components, and tools of the Plasma workspaces

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

Foundational libraries, components, and tools of the Plasma workspaces

%prep
%autosetup -p1 -n plasma-framework-%{?git:master}%{!?git:%{version}}
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
%{_datadir}/qlogging-categories6/plasma-framework.*
%{_datadir}/plasma

%files -n %{devname}
%{_includedir}/KF6/Plasma
%{_includedir}/KF6/PlasmaQuick
%{_libdir}/cmake/KF6Plasma
%{_libdir}/cmake/KF6PlasmaQuick
%{_datadir}/kdevappwizard/templates/*
%doc %{_qtdir}/doc/KF6Plasma.*

%files -n %{libname}
%{_libdir}/libKF6Plasma.so*
%{_libdir}/libKF6PlasmaQuick.so*
%{_qtdir}/qml/org/kde
%{_qtdir}/plugins/kf6/kirigami
%{_qtdir}/plugins/kf6/packagestructure
