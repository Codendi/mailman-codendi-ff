Summary: Mailman plugin for Codendi
Name: codendi-plugin-mailman
Version: 1.0
Release: 2
License: GPL
Group: Development/Languages
URL: https://github.com/Codendi/mailman-codendi-ff/

Packager: Nicolas Terray <nicolas.terray@xrce.xerox.com>

Source: %{name}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
Requires: mailman = 3:2.1.9-4.codendi 

%description
Mailman plugin for Codendi
This package controls the interaction between Codendi and Mailman.
It provides a single sign on authentication mecanism between the forge and mailman.

%prep
%setup -n %{name}  
%build

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}/%{_datadir}/codendi/plugins/mailman
%{__cp} -ar . %{buildroot}/%{_datadir}/codendi/plugins/mailman

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, codendiadm, codendiadm, 0755)
%{_datadir}/codendi/plugins/mailman

%post
patch -d %{_libdir}/mailman/ -p0 < %{_datadir}/codendi/plugins/mailman/usr/lib/mailman/Mailman/codendi.diff
%{__cp} -a %{_datadir}/codendi/plugins/mailman/var/lib/mailman/lists/extendcodendi.py %{_var}/lib/mailman/lists/extend.py


%changelog
* Tue May 11 2010 Nicolas TERRAY <nicolas.terray@xrce.xerox.com> - 1.0
- Initial package
