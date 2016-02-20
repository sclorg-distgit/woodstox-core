%global pkg_name woodstox-core
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global base_name woodstox
%global core_name %{base_name}-core
%global stax2_ver  3.1.1

Name:             %{?scl_prefix}%{pkg_name}
Version:          4.1.2
Release:          8.10%{?dist}
Summary:          High-performance XML processor
License:          ASL 2.0 or LGPLv2+
URL:              http://%{base_name}.codehaus.org/

Source0:          http://%{base_name}.codehaus.org/%{version}/%{core_name}-src-%{version}.tar.gz

Patch0:           %{pkg_name}-unbundling.patch
Patch1:           %{pkg_name}-fsf-address.patch

BuildArch:        noarch

BuildRequires:    maven30-felix-osgi-core
BuildRequires:    %{?scl_prefix_java_common}relaxngDatatype
BuildRequires:    %{?scl_prefix_java_common}msv-xsdlib
BuildRequires:    %{?scl_prefix_java_common}msv-msv
BuildRequires:    maven30-stax2-api
BuildRequires:    %{?scl_prefix_java_common}maven-local
BuildRequires:    %{?scl_prefix_java_common}javapackages-tools


%description
Woodstox is a high-performance validating namespace-aware StAX-compliant
(JSR-173) Open Source XML-processor written in Java.
XML processor means that it handles both input (== parsing)
and output (== writing, serialization)), as well as supporting tasks
such as validation.

%package javadoc
Summary:          API documentation for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n %{base_name}-%{version}
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x

cp src/maven/%{pkg_name}-asl.pom pom.xml
cp src/maven/%{pkg_name}-lgpl.pom pom-lgpl.xml

%patch0 -p1
%patch1 -p1

sed -i "s/@VERSION@/%{version}/g" pom.xml pom-lgpl.xml
sed -i "s/@REQ_STAX2_VERSION@/%{stax2_ver}/g" pom.xml pom-lgpl.xml

# removing bundled stuff
rm -rf lib
rm -rf src/maven
rm -rf src/resources
rm -rf src/samples
rm -rf src/java/org
rm -rf src/test/org
rm -rf src/test/stax2

# fixing incomplete source directory structure
mkdir src/main
mv -f src/java src/main/
mkdir src/test/java
mv -f src/test/wstxtest src/test/java/

# provided by JDK
%pom_remove_dep javax.xml.stream:stax-api

%mvn_file : %{pkg_name} %{pkg_name}-asl
%mvn_alias {org.codehaus.woodstox}:%{pkg_name}-asl @1:%{pkg_name}-lgpl
%{?scl:EOF}

%build
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
# stax2 missing -> cannot compile tests -> tests skipped
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
%mvn_install

# install also LGPL version of POM
install -Dpm 644 pom-lgpl.xml %{buildroot}%{_mavenpomdir}/JPP-%{pkg_name}-lgpl.pom
%{?scl:EOF}

%files -f .mfiles
%doc release-notes/asl/ASL2.0 release-notes/lgpl/LGPL2.1 release-notes/asl/NOTICE
%{_mavenpomdir}/JPP-%{pkg_name}-lgpl.pom

%files javadoc -f .mfiles-javadoc
%doc release-notes/asl/ASL2.0 release-notes/lgpl/LGPL2.1

%changelog
* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 4.1.2-8.10
- maven33 rebuild

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 4.1.2-8.9
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 4.1.2-8.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.1.2-8.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.1.2-8.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.1.2-8.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.1.2-8.4
- Remove requires on java

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 4.1.2-8.3
- SCL-ize BR

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.1.2-8.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.1.2-8.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 4.1.2-8
- Mass rebuild 2013-12-27

* Thu Aug 15 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.1.2-7
- Migrate away from mvn-rpmbuild (#997432)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.1.2-6
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 4.1.2-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 13 2011 Jaromir Capik <jcapik@redhat.com> - 4.1.2-1
- Initial version
